from copy import deepcopy
from unittest import TestCase

from dateutil.parser import parse
from djconnectwise.models import Company, CompanyStatus
from djconnectwise.models import ConnectWiseBoard
from djconnectwise.models import BoardStatus
from djconnectwise.models import Location
from djconnectwise.models import Team
from djconnectwise.models import Project
from djconnectwise.models import Ticket
from djconnectwise.models import TicketPriority
from djconnectwise.models import Member
from djconnectwise.models import SyncJob

from . import fixtures
from . import fixture_utils
from . import mocks
from .. import sync


def assert_sync_job(model_class):
    qset = SyncJob.objects.filter(entity_name=model_class.__name__)
    assert qset.exists()


class SynchronizerTestMixin:
    synchronizer_class = None
    model_class = None
    fixture = None

    def call_api(self, return_data):
        raise NotImplementedError

    def _assert_fields(self, instance, json_data):
        raise NotImplementedError

    def _sync(self, return_data):
        _, get_patch = self.call_api(return_data)
        self.synchronizer = self.synchronizer_class()
        self.synchronizer.sync()
        return _, get_patch

    def test_sync(self):
        self._sync(self.fixture)
        instance_dict = {c['id']: c for c in self.fixture}

        for instance in self.model_class.objects.all():
            json_data = instance_dict[instance.id]
            self._assert_fields(instance, json_data)

        assert_sync_job(self.model_class)

    def test_sync_update(self):
        self._sync(self.fixture)

        json_data = self.fixture[0]

        instance_id = json_data['id']
        original = self.model_class.objects \
            .get(id=instance_id)

        name = 'Some New Name'
        new_json = deepcopy(self.fixture[0])
        new_json['name'] = name
        new_json_list = [new_json]

        self._sync(new_json_list)

        changed = self.model_class.objects.get(id=instance_id)
        self.assertNotEqual(original.name,
                            name)
        self._assert_fields(changed, new_json)


class TestCompanySynchronizer(TestCase, SynchronizerTestMixin):
    synchronizer_class = sync.CompanySynchronizer
    model_class = Company
    fixture = fixtures.API_COMPANY_LIST

    def setUp(self):
        mocks.company_api_get_company_statuses_call(
            fixtures.API_COMPANY_STATUS_LIST)
        sync.CompanyStatusSynchronizer().sync()

    def call_api(self, return_data):
        return mocks.company_api_get_call(return_data)

    def _assert_fields(self, company, api_company):
        self.assertEqual(company.name, api_company['name'])
        self.assertEqual(company.identifier, api_company['identifier'])
        self.assertEqual(company.phone_number, api_company['phoneNumber'])
        self.assertEqual(company.fax_number, api_company['faxNumber'])
        self.assertEqual(company.address_line1, api_company['addressLine1'])
        self.assertEqual(company.address_line2, api_company['addressLine1'])
        self.assertEqual(company.city, api_company['city'])
        self.assertEqual(company.state_identifier, api_company['state'])
        self.assertEqual(company.zip, api_company['zip'])
        self.assertEqual(company.status.id, api_company['status']['id'])


class TestProjectSynchronizer(TestCase, SynchronizerTestMixin):
    synchronizer_class = sync.ProjectSynchronizer
    model_class = Project
    fixture = fixtures.API_PROJECT_LIST

    def call_api(self, return_data):
        return mocks.project_api_get_projects_call(return_data)

    def _assert_fields(self, instance, json_data):
        assert instance.name == json_data['name']
        assert instance.id == json_data['id']


class TestTeamSynchronizer(TestCase, SynchronizerTestMixin):
    synchronizer_class = sync.TeamSynchronizer
    model_class = Team
    fixture = fixtures.API_SERVICE_TEAM_LIST

    def call_api(self, return_data):
        return mocks.service_api_get_teams_call(return_data)

    def setUp(self):
        fixture_utils.init_boards()

    def _assert_fields(self, team, team_json):
        ids = set([t.id for t in team.members.all()])
        self.assertEqual(team.id, team_json['id'])
        self.assertEqual(team.name, team_json['name'])
        self.assertEqual(team.board.id, team_json['boardId'])
        self.assertTrue(ids < set(team_json['members']))


class TestPrioritySynchronizer(TestCase, SynchronizerTestMixin):
    synchronizer_class = sync.PrioritySynchronizer
    model_class = TicketPriority
    fixture = fixtures.API_SERVICE_PRIORITY_LIST

    def _assert_fields(self, priority, api_priority):
        assert priority.name == api_priority['name']
        assert priority.id == api_priority['id']
        if 'color' in api_priority.keys():
            assert priority.color == api_priority['color']
        else:
            assert priority.color in self.valid_prio_colors
        if 'sortOrder' in api_priority.keys():
            assert priority.sort == api_priority['sortOrder']
        else:
            assert priority.sort is None

    def setUp(self):
        self.synchronizer = sync.PrioritySynchronizer()
        self.valid_prio_colors = \
            list(TicketPriority.DEFAULT_COLORS.values()) + \
            [TicketPriority.DEFAULT_COLOR]

    def call_api(self, return_data):
        return mocks.service_api_get_priorities_call(return_data)


class TestCompanyStatusSynchronizer(TestCase, SynchronizerTestMixin):
    synchronizer_class = sync.CompanyStatusSynchronizer
    model_class = CompanyStatus
    fixture = fixtures.API_COMPANY_STATUS_LIST

    def call_api(self, return_data):
        return mocks.company_api_get_company_statuses_call(return_data)

    def _assert_fields(self, instance, json_data):
        self.assertEqual(instance.name, json_data['name'])
        self.assertEqual(instance.default_flag, json_data['defaultFlag'])
        self.assertEqual(instance.inactive_flag, json_data['inactiveFlag'])
        self.assertEqual(instance.notify_flag, json_data['notifyFlag'])
        self.assertEqual(instance.dissalow_saving_flag,
                         json_data['disallowSavingFlag'])
        self.assertEqual(instance.notification_message,
                         json_data['notificationMessage'])
        self.assertEqual(instance.custom_note_flag,
                         json_data['customNoteFlag'])
        self.assertEqual(instance.cancel_open_tracks_flag,
                         json_data['cancelOpenTracksFlag'])


class TestLocationSynchronizer(TestCase, SynchronizerTestMixin):
    synchronizer_class = sync.LocationSynchronizer
    model_class = Location
    fixture = fixtures.API_SERVICE_LOCATION_LIST

    def _assert_fields(self, location, api_location):
        self.assertEqual(location.name, api_location['name'])
        self.assertEqual(location.id, api_location['id'])
        self.assertEqual(location.where, api_location['where'])

    def setUp(self):
        self.synchronizer = sync.LocationSynchronizer()

    def call_api(self, return_data):
        return mocks.service_api_get_locations_call(return_data)


class TestBoardSynchronizer(TestCase, SynchronizerTestMixin):
    synchronizer_class = sync.BoardSynchronizer
    model_class = ConnectWiseBoard
    fixture = fixtures.API_BOARD_LIST

    def call_api(self, return_data):
        return mocks.service_api_get_boards_call(return_data)

    def _assert_fields(self, instance, json_data):
        self.assertEqual(instance.name, json_data['name'])
        self.assertEqual(instance.inactive, json_data['inactive'])


class TestBoardStatusSynchronizer(TestCase, SynchronizerTestMixin):
    synchronizer_class = sync.BoardStatusSynchronizer
    model_class = BoardStatus
    fixture = fixtures.API_BOARD_STATUS_LIST

    def _assert_fields(self, instance, json_data):
        self.assertEqual(instance.name, json_data['name'])
        self.assertEqual(instance.sort_order, json_data['sortOrder'])
        self.assertEqual(instance.display_on_board,
                         json_data['displayOnBoard'])
        self.assertEqual(instance.inactive, json_data['inactive'])
        self.assertEqual(instance.closed_status, json_data['closedStatus'])

    def setUp(self):
        fixture_utils.init_boards()

    def call_api(self, return_data):
        return mocks.service_api_get_statuses_call(return_data)


class TestMemberSynchronization(TestCase):

    def setUp(self):
        self.identifier = 'User1'
        self.synchronizer = sync.MemberSynchronizer()
        mocks.system_api_get_members_call([fixtures.API_MEMBER])
        mocks.system_api_get_member_image_by_identifier_call(
            (mocks.CW_MEMBER_IMAGE_FILENAME, mocks.get_member_avatar()))

    def _assert_member_fields(self, local_member, api_member):
        self.assertEqual(local_member.first_name, api_member['firstName'])
        self.assertEqual(local_member.last_name, api_member['lastName'])
        self.assertEqual(local_member.office_email, api_member['officeEmail'])

    def _clear_members(self):
        Member.objects.all().delete()

    def test_sync_member_update(self):
        self._clear_members()
        member = Member()
        member.id = 176
        member.identifier = self.identifier
        member.first_name = 'some stale first name'
        member.last_name = 'some stale last name'
        member.office_email = 'some@stale.com'
        member.save()

        self.synchronizer.sync()
        local_member = Member.objects.get(identifier=self.identifier)
        api_member = fixtures.API_MEMBER
        self._assert_member_fields(local_member, api_member)

    def test_sync_member_create(self):
        self._clear_members()
        self.synchronizer.sync()
        local_member = Member.objects.all().first()
        api_member = fixtures.API_MEMBER
        self._assert_member_fields(local_member, api_member)
        assert_sync_job(Member)


class TestTicketSynchronizer(TestCase):

    def setUp(self):
        super().setUp()
        mocks.system_api_get_members_call(fixtures.API_MEMBER_LIST)
        mocks.system_api_get_member_image_by_identifier_call(
            (mocks.CW_MEMBER_IMAGE_FILENAME, mocks.get_member_avatar()))
        mocks.service_api_tickets_call()

        self._init_data()

    def _clean(self):
        Ticket.objects.all().delete()

    def _init_data(self):
        self._clean()

        fixture_utils.init_boards()
        fixture_utils.init_board_statuses()
        fixture_utils.init_teams()
        fixture_utils.init_members()
        fixture_utils.init_companies()
        fixture_utils.init_priorities()
        fixture_utils.init_projects()
        fixture_utils.init_locations()

    def _assert_sync(self, instance, json_data):
        self.assertEqual(instance.summary, json_data['summary'])
        self.assertEqual(instance.closed_flag, json_data.get('closedFlag'))
        self.assertEqual(instance.type, json_data.get('type'))
        self.assertEqual(instance.entered_date_utc,
                         parse(json_data.get('dateEntered')))
        self.assertEqual(instance.last_updated_utc,
                         parse(json_data.get('_info').get('lastUpdated')))
        self.assertEqual(instance.required_date_utc,
                         parse(json_data.get('requiredDate')))
        self.assertEqual(instance.resources, json_data.get('resources'))
        self.assertEqual(instance.budget_hours, json_data.get('budgetHours'))
        self.assertEqual(instance.actual_hours, json_data.get('actualHours'))
        self.assertEqual(instance.record_type, json_data.get('recordType'))
        self.assertEqual(instance.parent_ticket_id,
                         json_data.get('parentTicketId'))
        self.assertEqual(instance.has_child_ticket,
                         json_data.get('hasChildTicket'))

        self.assertEqual(instance.has_child_ticket,
                         json_data.get('hasChildTicket'))
        resource_names = set(json_data.get('resources').split(','))

        # verify members
        member_qset = instance.members.all()
        member_names = set(member_qset.values_list('identifier', flat=True))
        self.assertEqual(resource_names, member_names)

        # verify assigned team
        self.assertEqual(instance.team_id, json_data['team']['id'])

        # verify assigned board
        self.assertEqual(instance.board_id, json_data['board']['id'])

        # verify assigned company
        self.assertEqual(instance.company_id, json_data['company']['id'])

        # verify assigned priority
        self.assertEqual(instance.priority_id, json_data['priority']['id'])

        # verify assigned location
        self.assertEqual(instance.location_id,
                         json_data['serviceLocation']['id'])

        # verify assigned project
        self.assertEqual(instance.project_id,
                         json_data['project']['id'])

        # verify assigned status
        self.assertEqual(instance.status_id,
                         json_data['status']['id'])

    def test_sync_ticket(self):
        """Test to ensure ticket synchronizer saves an
        CW Ticket instance locally"""
        synchronizer = sync.TicketSynchronizer()
        synchronizer.sync()
        self.assertGreater(Ticket.objects.all().count(), 0)

        json_data = fixtures.API_SERVICE_TICKET
        instance = Ticket.objects.get(id=json_data['id'])
        self._assert_sync(instance, json_data)
        assert_sync_job(Ticket)

    def test_sync_updated(self):
        self._init_data()
        fixture_utils.init_tickets()
        updated_ticket_fixture = deepcopy(fixtures.API_SERVICE_TICKET)
        updated_ticket_fixture['summary'] = 'A new kind of summary'
        fixture_list = [updated_ticket_fixture]

        method_name = 'djconnectwise.api.ServiceAPIClient.get_tickets'
        mock_call, _patch = mocks.create_mock_call(method_name, fixture_list)
        synchronizer = sync.TicketSynchronizer()
        synchronizer.sync()
        created_count, updated_count, _ = synchronizer.sync()

        self.assertEqual(created_count, 0)
        self.assertEqual(updated_count, len(fixture_list))

        instance = Ticket.objects.get(id=updated_ticket_fixture['id'])
        self._assert_sync(instance, updated_ticket_fixture)

    def test_delete_stale_tickets(self):
        """Local ticket should be deleted if omitted from sync"""
        fixture_utils.init_tickets()

        ticket_id = fixtures.API_SERVICE_TICKET['id']
        ticket_qset = Ticket.objects.filter(id=ticket_id)
        self.assertEqual(ticket_qset.count(), 1)

        method_name = 'djconnectwise.api.ServiceAPIClient.get_tickets'
        mock_call, _patch = mocks.create_mock_call(method_name, [])
        synchronizer = sync.TicketSynchronizer()
        synchronizer.sync(reset=True)
        self.assertEqual(ticket_qset.count(), 0)
        _patch.stop()
