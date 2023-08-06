import logging

from dateutil.parser import parse

from djconnectwise import api
from djconnectwise import models
from djconnectwise.utils import get_hash, get_filename_extension

from django.core.files.base import ContentFile
from django.utils import timezone
from django.conf import settings


DEFAULT_AVATAR_EXTENSION = 'jpg'

logger = logging.getLogger(__name__)


class Synchronizer:
    lookup_key = 'id'
    api_conditions = ''

    def __init__(self, *args, **kwargs):
        self.instance_map = {}
        self.client = self.client_class()
        self.load_instance_map()

    def load_instance_map(self):
        qset = self.get_queryset()
        self.instance_map = {
            getattr(i, self.lookup_key): i for i in qset
        }

    def get_queryset(self):
        return self.model_class.objects.all()

    def get(self):
        """Buffer and return all pages of results."""
        records = []
        page = 1
        while True:
            logger.info(
                'Fetching {} records, batch {}'.format(self.model_class, page)
            )
            page_records = self.get_page(
                page=page, page_size=settings.DJCONNECTWISE_API_BATCH_LIMIT
            )
            records += page_records
            page += 1
            if len(page_records) < settings.DJCONNECTWISE_API_BATCH_LIMIT:
                # This page wasn't full, so there's no more records after
                # this page.
                break
        return records

    def get_page(self, *args, **kwargs):
        raise NotImplementedError

    def fetch_sync_by_id(self, *args, **kwargs):
        raise NotImplementedError

    def fetch_delete_by_id(self, *args, **kwargs):
        raise NotImplementedError

    def get_or_create_instance(self, api_instance):
        lookup_key = api_instance[self.lookup_key]
        instance = self.instance_map.get(lookup_key)

        created = False

        if not instance:
            instance = self.model_class()
            self._assign_field_data(instance, api_instance)
            instance.save()
            created = True
            self.instance_map[lookup_key] = instance

        return instance, created

    def prune_stale_records(self, synced_ids):
        stale_ids = set(self.instance_map.keys()) - synced_ids
        deleted_count = 0
        if stale_ids:
            delete_qset = self.model_class.objects.filter(pk__in=stale_ids)
            deleted_count = delete_qset.count()
            msg = 'Removing {} stale records for model: {}'.format(
                len(stale_ids), self.model_class,
            )
            logger.info(msg)
            delete_qset.delete()

        return deleted_count

    def update_or_create_instance(self, api_instance):
        """
        Creates and returns an instance if it does not already exist.
        """
        instance, created = self.get_or_create_instance(
            api_instance)

        action = 'Created' if created else 'Updated'
        if not created:
            self._assign_field_data(instance, api_instance)
            instance.save()

        self.instance_map[instance.id] = instance

        msg = ' {}: {} {}'
        logger.info(msg.format(action, self.model_class.__name__, instance))

        return instance, created

    def sync(self, reset=False):
        created_count = 0
        updated_count = 0
        deleted_count = 0

        synced_ids = set()
        for record in self.get():
            _, created = self.update_or_create_instance(record)

            if created:
                created_count += 1
            else:
                updated_count += 1

            synced_ids.add(record['id'])

        stale_ids = set(self.instance_map.keys()) - synced_ids
        if stale_ids and reset:
            deleted_count = len(stale_ids)
            msg = 'Removing {} stale records for model: {}'.format(
                len(stale_ids), self.model_class,
            )
            logger.info(msg)
            self.model_class.objects.filter(pk__in=stale_ids).delete()

        return created_count, updated_count, deleted_count


class BoardSynchronizer(Synchronizer):
    client_class = api.ServiceAPIClient
    model_class = models.ConnectWiseBoard

    def _assign_field_data(self, instance, json_data):
        instance.id = json_data['id']
        instance.name = json_data['name']
        instance.inactive = json_data.get('inactive')
        return instance

    def get_page(self, *args, **kwargs):
        return self.client.get_boards(*args, **kwargs)

    def get_queryset(self):
        return self.model_class.objects.all()


class BoardChildSynchronizer(Synchronizer):

    def _assign_field_data(self, instance, json_data):
        instance.id = json_data['id']
        instance.name = json_data['name']
        instance.board = models.ConnectWiseBoard.objects.get(
            id=json_data['boardId'])
        return instance

    def client_call(self, board_id):
        raise NotImplementedError

    def get_page(self, *args, **kwargs):
        records = []
        board_qs = models.ConnectWiseBoard.objects.all()

        for board_id in board_qs.values_list('id', flat=True):
            records += self.client_call(board_id, *args, **kwargs)

        return records


class BoardStatusSynchronizer(BoardChildSynchronizer):
    client_class = api.ServiceAPIClient
    model_class = models.BoardStatus

    def _assign_field_data(self, instance, json_data):
        instance = super(BoardStatusSynchronizer, self)._assign_field_data(
            instance, json_data)

        instance.sort_order = json_data.get('sortOrder')
        instance.display_on_board = json_data.get('displayOnBoard')
        instance.inactive = json_data.get('inactive')
        instance.closed_status = json_data.get('closedStatus')

        return instance

    def client_call(self, board_id, *args, **kwargs):
        return self.client.get_statuses(board_id, *args, **kwargs)

    def get_queryset(self):
        return self.model_class.objects.all()


class TeamSynchronizer(BoardChildSynchronizer):
    client_class = api.ServiceAPIClient
    model_class = models.Team

    def _assign_field_data(self, instance, json_data):
        instance = super(TeamSynchronizer, self)._assign_field_data(
            instance, json_data)

        members = []
        if json_data['members']:
            members = list(models.Member.objects.filter(
                id__in=json_data['members']))

        instance.save()

        instance.members.clear()
        instance.members.add(*members)
        return instance

    def client_call(self, board_id, *args, **kwargs):
        return self.client.get_teams(board_id, *args, **kwargs)


class CompanySynchronizer(Synchronizer):
    """
    Coordinates retrieval and demarshalling of ConnectWise JSON
    Company instances.
    """
    client_class = api.CompanyAPIClient
    model_class = models.Company
    api_conditions = 'deletedFlag=False'

    def _assign_field_data(self, company, company_json):
        """
        Assigns field data from an company_json instance
        to a local Company model instance
        """
        company.id = company_json['id']
        company.name = company_json['name']
        company.identifier = company_json['identifier']

        # Fields below aren't included when the company is created as a
        # side-effect of creating/updating a ticket or other type of object,
        # so use .get().
        company.phone_number = company_json.get('phoneNumber')
        company.fax_number = company_json.get('faxNumber')
        company.address_line1 = company_json.get('addressLine1')
        company.address_line2 = company_json.get('addressLine2')
        company.city = company_json.get('city')
        company.state_identifier = company_json.get('state')
        company.zip = company_json.get('zip')
        company.created = timezone.now()
        company.deleted_flag = company_json.get('deletedFlag', False)

        status_json = company_json.get('status')
        if status_json:
            try:
                status = models.CompanyStatus.objects.get(pk=status_json['id'])
                company.status = status
            except models.CompanyStatus.DoesNotExist:
                logger.warning(
                    'Failed to find CompanyStatus: {}'.format(
                        status_json['id']
                    ))
        company.save()
        return company

    def get_page(self, *args, **kwargs):
        kwargs['conditions'] = self.api_conditions
        return self.client.get_companies(*args, **kwargs)

    def get_queryset(self):
        return self.model_class.objects.all()

    def fetch_sync_by_id(self, company_id):
        company = self.client.by_id(company_id)
        self.update_or_create_instance(company)

    def fetch_delete_by_id(self, company_id):
        # Companies are deleted by setting deleted_flag = True, so
        # just treat this as a normal sync.
        self.fetch_sync_by_id(company_id)


class CompanyStatusSynchronizer(Synchronizer):
    """
    Coordinates retrieval and demarshalling of ConnectWise JSON
    CompanyStatus instances.
    """
    client_class = api.CompanyAPIClient
    model_class = models.CompanyStatus

    def _assign_field_data(self, instance, json_data):
        instance.id = json_data['id']
        instance.name = json_data['name']
        instance.default_flag = json_data.get('defaultFlag')
        instance.inactive_flag = json_data.get('inactiveFlag')
        instance.notify_flag = json_data.get('notifyFlag')
        instance.dissalow_saving_flag = json_data.get('disallowSavingFlag')
        instance.notification_message = json_data.get('notificationMessage')
        instance.custom_note_flag = json_data.get('customNoteFlag')
        instance.cancel_open_tracks_flag = json_data.get(
            'cancelOpenTracksFlag'
        )

        if json_data.get('track'):
            instance.track_id = json_data['track']['id']

        return instance

    def get_page(self, *args, **kwargs):
        return self.client.get_company_statuses(*args, **kwargs)


class LocationSynchronizer(Synchronizer):
    """
    Coordinates retrieval and demarshalling of ConnectWise JSON
    Location instances.
    """
    client_class = api.ServiceAPIClient
    model_class = models.Location

    def _assign_field_data(self, location, location_json):
        """
        Assigns field data from an company_json instance
        to a local Company model instance
        """
        location.id = location_json['id']
        location.name = location_json['name']
        location.where = location_json.get('where')
        return location

    def get_page(self, *args, **kwargs):
        return self.client.get_locations(*args, **kwargs)


class PrioritySynchronizer(Synchronizer):
    client_class = api.ServiceAPIClient
    model_class = models.TicketPriority

    def _assign_field_data(self, ticket_priority, api_priority):
        ticket_priority.id = api_priority['id']
        ticket_priority.name = api_priority['name']
        ticket_priority.color = api_priority.get('color')

        # work around due to api data inconsistencies
        sort_value = api_priority.get('sort') or api_priority.get('sortOrder')
        if sort_value:
            ticket_priority.sort = sort_value

        return ticket_priority

    def get_page(self, *args, **kwargs):
        return self.client.get_priorities(*args, **kwargs)


class ProjectSynchronizer(Synchronizer):
    client_class = api.ProjectAPIClient
    model_class = models.Project

    def _assign_field_data(self, instance, json_data):
        instance.id = json_data['id']
        instance.name = json_data['name']
        instance.status_name = json_data['status']['name']
        return instance

    def get_page(self, *args, **kwargs):
        return self.client.get_projects(*args, **kwargs)

    def get_queryset(self):
        return self.model_class.objects.all()

    def fetch_sync_by_id(self, project_id):
        project = self.client.get_project(project_id)
        self.update_or_create_instance(project)
        logger.info('Updated project {}'.format(project))

    def fetch_delete_by_id(self, project_id):
        try:
            self.client.get_project(project_id)
        except api.ConnectWiseRecordNotFoundError:
            # This is what we expect to happen. Since it's gone in CW, we
            # are safe to delete it from here.
            models.Project.objects.filter(id=project_id).delete()
            logger.info(
                'Deleted project {} (if it existed).'.format(project_id)
            )


class MemberSynchronizer(Synchronizer):
    client_class = api.SystemAPIClient
    model_class = models.Member

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = self.client_class()
        self.last_sync_job = None

        sync_job_qset = models.SyncJob.objects.all()

        if sync_job_qset.exists():
            self.last_sync_job = sync_job_qset.last()

    def _assign_field_data(self, instance, json_data):
        instance.id = json_data['id']
        instance.first_name = json_data.get('firstName')
        instance.last_name = json_data.get('lastName')
        instance.identifier = json_data.get('identifier')
        instance.office_email = json_data.get('officeEmail')
        instance.license_class = json_data.get('licenseClass')
        instance.inactive = json_data.get('inactiveFlag')
        return instance

    def _save_avatar(self, member, avatar, attachment_filename):
        """
        The Django ImageField (and ThumbnailerImageField) field adjusts our
        filename if the file already exists- it adds some random characters at
        the end of the name. This means if we just save a new image when the
        old one still exists, we'll get a new image for each save, resulting
        in lots of unnecessary images. So we'll delete the old image first,
        and then the save will use the exact name we give it.

        Well, except in the case where two or more members share the same
        image, because we're using content hashes as names, and ConnectWise
        gives users a common default avatar. In that case, the first save
        will use the expected name, while subsequent saves for other members
        will have some random characters added to the filename.

        This method tells Django not to call save() on the given model,
        so the caller must be sure to do that itself.
        """
        extension = get_filename_extension(attachment_filename)
        filename = '{}.{}'.format(
            get_hash(avatar), extension or DEFAULT_AVATAR_EXTENSION)
        avatar_file = ContentFile(avatar)
        member.avatar.delete(save=False)
        member.avatar.save(filename, avatar_file, save=False)
        logger.info("Saved member '{}' avatar to {}.".format(
            member.identifier, member.avatar.name))

    def get(self):
        records = []
        page = 1
        while True:
            logger.info(
                'Fetching member records, batch {}'.format(page)
            )
            page_records = self.get_page(
                page=page, page_size=settings.DJCONNECTWISE_API_BATCH_LIMIT
            )
            records += page_records
            page += 1
            if len(page_records) < settings.DJCONNECTWISE_API_BATCH_LIMIT:
                # No more records
                break
        return records

    def get_page(self, *args, **kwargs):
        return self.client.get_members(*args, **kwargs)

    def sync(self, reset=False):
        members_json = self.get()

        updated_count = 0
        created_count = 0
        deleted_count = 0
        synced_ids = set()

        for api_member in members_json:
            member_id = api_member['id']
            username = api_member['identifier']

            try:
                member = models.Member.objects.get(id=member_id)
                self._assign_field_data(member, api_member)
                member.save()
                updated_count += 1
                logger.info('Updated member: {0}'.format(member.identifier))
            except models.Member.DoesNotExist:
                # Member with that ID wasn't found, so let's make one.
                member = models.Member()
                self._assign_field_data(member, api_member)
                member.save()
                created_count += 1
                logger.info('Created member: {0}'.format(member.identifier))

            # Only update the avatar if the member profile
            # was updated since last sync.
            member_last_updated = parse(api_member['_info']['lastUpdated'])
            logger.debug(
                'Member {} last updated: {}'.format(
                    member.identifier,
                    member_last_updated
                )
            )
            member_stale = False
            if self.last_sync_job:
                member_stale = member_last_updated > \
                    self.last_sync_job.start_time

            if not self.last_sync_job or member_stale:
                logger.debug(
                    'Fetching avatar for member {}.'.format(member.identifier)
                )
                (attachment_filename, avatar) = self.client \
                    .get_member_image_by_identifier(username)
                if attachment_filename and avatar:
                    self._save_avatar(member, avatar, attachment_filename)

            member.save()
            synced_ids.add(api_member['id'])

        if reset:
            deleted_count = self.prune_stale_records(synced_ids)

        return created_count, updated_count, deleted_count


class TicketSynchronizer:
    """
    Coordinates retrieval and demarshalling of ConnectWise JSON
    objects to the local counterparts.
    """

    def __init__(self, reset=False):
        self.company_synchronizer = CompanySynchronizer()
        self.status_synchronizer = BoardStatusSynchronizer()
        self.priority_synchronizer = PrioritySynchronizer()
        self.location_synchronizer = LocationSynchronizer()

        self.reset = reset
        self.last_sync_job = None
        extra_conditions = ''
        sync_job_qset = models.SyncJob.objects.all()

        if sync_job_qset.exists() and not self.reset:
            self.last_sync_job = sync_job_qset.last()
            last_sync_job_time = self.last_sync_job.start_time.isoformat()
            extra_conditions = "lastUpdated > [{0}]".format(last_sync_job_time)

            log_msg = 'Preparing sync job for objects updated since {}.'
            logger.info(log_msg.format(last_sync_job_time))
            logger.info(
                'Ticket extra conditions: {0}'.format(extra_conditions))
        else:
            logger.info('Preparing full ticket sync job.')
            # absence of a sync job indicates that this is an initial/full
            # sync, in which case we do not want to retrieve closed tickets
            extra_conditions = 'closedFlag = False'

        self.service_client = api.ServiceAPIClient(
            extra_conditions=extra_conditions)

        self.system_client = api.SystemAPIClient()

        # We need to remove the underscores to ensure an accurate
        # lookup of the normalized api fieldnames
        self.local_ticket_fields = self._create_field_lookup(
            models.Ticket
        )
        self.local_company_fields = self._create_field_lookup(models.Company)

        self.members_map = {
            m.identifier: m for m in models.Member.objects.all()
        }
        self.project_map = {p.id: p for p in models.Project.objects.all()}

        self.exclude_fields = ('priority', 'status', 'company')

    def _create_field_lookup(self, clazz):
        field_map = [
            (f.name, f.name.replace('_', '')) for
            f in clazz._meta.get_fields(
                include_parents=False, include_hidden=True)
        ]
        return dict(field_map)

    def get_or_create_project(self, api_project):
        if api_project:
            project = self.project_map.get(api_project['id'])
            if not project:
                project = models.Project()
                project.id = api_project['id']
                project.name = api_project['name']
                project.project_id = api_project['id']
                project.save()
                self.project_map[project.id] = project
                logger.info('Project created: %s' % project.name)
            return project

    def sync_ticket(self, json_data):
        """
        Creates a new local instance of the supplied ConnectWise
        Ticket instance.
        """
        json_data_id = json_data['id']
        logger.info('Syncing ticket {}'.format(json_data_id))
        ticket, created = models.Ticket.objects \
            .get_or_create(pk=json_data_id)

        ticket.api_text = str(json_data)

        # If the status results in a move to a different column
        original_status = not created and ticket.status or None

        ticket.summary = json_data['summary']
        ticket.closed_flag = json_data.get('closedFlag')
        ticket.type = json_data.get('type')
        ticket.entered_date_utc = json_data.get('dateEntered')
        ticket.last_updated_utc = json_data.get('_info').get('lastUpdated')
        ticket.required_date_utc = json_data.get('requiredDate')
        ticket.resources = json_data.get('resources')
        ticket.budget_hours = json_data.get('budgetHours')
        ticket.actual_hours = json_data.get('actualHours')
        ticket.record_type = json_data.get('recordType')
        ticket.parent_ticket_id = json_data.get('parentTicketId')
        ticket.has_child_ticket = json_data.get('hasChildTicket')
        ticket.customer_updated = json_data.get('customerUpdatedFlag')

        if 'team' in json_data:
            team = json_data['team']
            try:
                if team:
                    ticket.team = models.Team.objects.get(
                        pk=team['id'])
            except models.Team.DoesNotExist:
                logger.warning(
                    'Failed to find team {} for ticket {}.'.format(
                        team['id'],
                        json_data_id
                    )
                )

        try:
            ticket.board = models.ConnectWiseBoard.objects.get(
                pk=json_data['board']['id'])
        except models.ConnectWiseBoard.DoesNotExist:
            logger.warning(
                'Failed to find board {} for ticket {}.'.format(
                    json_data['board']['id'],
                    json_data_id
                )
            )

        if 'owner' in json_data:
            owner = json_data['owner']
            try:
                if owner:
                    ticket.owner = models.Member.objects.get(
                        pk=owner['id'])
                    logger.info('Assigned owner: %s' % owner)

            except models.Member.DoesNotExist:
                logger.warning(
                    'Failed to find member {} for ticket {}.'.format(
                        owner['id'],
                        json_data_id
                    )
                )

        ticket.company, _ = self.company_synchronizer \
            .get_or_create_instance(json_data['company'])

        priority, _ = self.priority_synchronizer \
            .get_or_create_instance(json_data['priority'])

        ticket.priority = priority

        if 'serviceLocation' in json_data and json_data['serviceLocation']:
            location_id = json_data['serviceLocation']['id']
            try:
                ticket.location = models.Location.objects.get(id=location_id)
            except models.Location.DoesNotExist:
                logger.warning(
                    'Failed to find location {} for ticket {}.'.format(
                        location_id,
                        json_data_id
                    )
                )

        new_ticket_status = None
        try:
            # TODO - Discuss - Do we assume that the status exists
            # or do we want to do a roundtrip and retrieve from the server?
            new_ticket_status = models.BoardStatus.objects.get(
                pk=json_data['status']['id'])
        except models.BoardStatus.DoesNotExist:
            logger.warning(
                'Failed to find board status {} for ticket {}.'.format(
                    json_data['status']['id'],
                    json_data_id
                )
            )

        ticket.status = new_ticket_status

        if 'project' in json_data:
            ticket.project = self.get_or_create_project(json_data['project'])

        ticket.save()
        action = created and 'Created' or 'Updated'

        status_changed = ''
        if original_status != new_ticket_status:
            status_changed = '; status changed from ' \
                         '{} to {}'.format(original_status, new_ticket_status)

        log_info = '{} ticket {}{}'.format(
            action, ticket.id, status_changed
        )
        logger.info(log_info)

        self._manage_member_assignments(ticket)
        return ticket, created

    def _manage_member_assignments(self, ticket):
        if not ticket.resources:
            return

        ticket_assignments = {}
        usernames = [
            u.strip() for u in ticket.resources.split(',')
        ]
        # Reset board/ticket assignment in case the assigned resources
        # have changed since last sync.
        models.TicketAssignment.objects.filter(
            ticket=ticket).delete()
        for username in usernames:
            member = self.members_map.get(username)

            if member:
                assignment = models.TicketAssignment()
                assignment.member = member
                assignment.ticket = ticket
                ticket_assignments[(username, ticket.id,)] = \
                    assignment
                msg = 'Member ticket assignment: ' \
                      'ticket {}, member {}'.format(ticket.id, username)
                logger.info(msg)
            else:
                logger.warning(
                    'Failed to locate member with username {} for ticket '
                    '{} assignment.'.format(username, ticket.id)
                )

        if ticket_assignments:
            logger.info(
                'Saving {} ticket assignments'.format(
                    len(ticket_assignments)
                )
            )
            models.TicketAssignment.objects.bulk_create(
                list(ticket_assignments.values())
            )

    def prune_stale_records(self, synced_ids):
        # first pass, delete closed tickets
        logger.info('Deleting closed tickets')
        delete_qset = models.Ticket.objects.filter(closed_flag=True)
        deleted_count = delete_qset.count()
        delete_qset.delete()

        local_ids = set(self.instance_map.keys())
        stale_ids = local_ids - synced_ids
        if stale_ids and local_ids:
            delete_qset = models.Ticket.objects.filter(pk__in=stale_ids)
            deleted_count += delete_qset.count()
            msg = 'Removing {} stale records for model: Ticket'.format(
                len(stale_ids)
            )
            logger.info(msg)
            delete_qset.delete()

        return deleted_count

    def fetch_sync_by_id(self, ticket_id):
        ticket = self.service_client.get_ticket(ticket_id)
        self.sync_ticket(ticket)
        logger.info('Updated ticket {}'.format(ticket_id))

    def fetch_delete_by_id(self, ticket_id):
        try:
            self.service_client.get_ticket(ticket_id)
        except api.ConnectWiseRecordNotFoundError:
            # This is what we expect to happen. Since it's gone in CW, we
            # are safe to delete it from here.
            models.Ticket.objects.filter(id=ticket_id).delete()
            logger.info(
                'Deleted ticket {} (if it existed).'.format(ticket_id)
            )

    def sync(self, reset=False):
        """
        Synchronizes tickets between the ConnectWise server and the
        local database. Synchronization is performed in batches
        specified in the DJCONNECTWISE_API_BATCH_LIMIT setting
        """

        self.instance_map = self.instance_map = {
            i.id: i for i in models.Ticket.objects.all()
        }

        sync_job = models.SyncJob.objects.create()
        page = 1  # Page is 1-indexed

        created_count = 0
        updated_count = 0
        synced_ids = set()

        while True:
            logger.info('Processing ticket batch {}'.format(page))
            tickets = self.service_client.get_tickets(
                page=page,
                page_size=settings.DJCONNECTWISE_API_BATCH_LIMIT
            )
            num_tickets = len(tickets)

            for ticket in tickets:
                ticket, created = self.sync_ticket(ticket)
                if created:
                    created_count += 1
                else:
                    updated_count += 1

                synced_ids.add(ticket.id)

            page += 1
            if num_tickets < settings.DJCONNECTWISE_API_BATCH_LIMIT:
                break

        delete_count = self.prune_stale_records(synced_ids)

        sync_job.end_time = timezone.now()
        sync_job.save()

        return created_count, updated_count, delete_count
