from http import HTTPStatus

import pytest
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.test import Client
from django.urls import reverse

from commcare_connect.opportunity.tests.factories import DeliveryTypeFactory
from commcare_connect.organization.models import Organization
from commcare_connect.program.models import ManagedOpportunityApplication, ManagedOpportunityApplicationStatus, Program
from commcare_connect.program.tests.factories import (
    ManagedOpportunityApplicationFactory,
    ManagedOpportunityFactory,
    ProgramFactory,
)
from commcare_connect.users.models import User


class BaseProgramTest:
    @pytest.fixture(autouse=True)
    def base_setup(self, program_manager_org: Organization, program_manager_org_user_admin: User, client: Client):
        self.organization = program_manager_org
        self.user = program_manager_org_user_admin
        self.client = client
        client.force_login(self.user)
        self.list_url = reverse("program:list", kwargs={"org_slug": self.organization.slug})


@pytest.mark.django_db
class TestProgramListView(BaseProgramTest):
    @pytest.fixture(autouse=True)
    def test_setup(self):
        self.list_url = reverse("program:list", kwargs={"org_slug": self.organization.slug})
        self.programs = ProgramFactory.create_batch(15, organization=self.organization)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(self.list_url)
        assert response.status_code == HTTPStatus.OK

    def test_pagination_is_ten(self):
        response = self.client.get(self.list_url)
        assert response.status_code == HTTPStatus.OK
        programs = response.context["page_obj"].object_list
        assert len(programs) == 10

    def test_pagination_next_page(self):
        response = self.client.get(f"{self.list_url}?page=2")
        assert response.status_code == HTTPStatus.OK
        programs = response.context["page_obj"].object_list
        assert len(programs) == 5

    def test_default_ordering(self, client):
        response = self.client.get(self.list_url)
        assert response.status_code == HTTPStatus.OK
        page_obj = response.context["page_obj"]
        programs = page_obj.object_list
        expected_programs = sorted(self.programs, key=lambda p: p.name)
        self.check_order(programs, expected_programs[:10])

    def test_ordering_by_start_date(self, client):
        response = self.client.get(f"{self.list_url}?sort=start_date")
        assert response.status_code == HTTPStatus.OK
        page_obj = response.context["page_obj"]
        programs = page_obj.object_list
        expected_programs = sorted(self.programs, key=lambda p: p.start_date)
        self.check_order(programs, expected_programs[:10])

    def test_ordering_by_end_date(self, client):
        response = self.client.get(f"{self.list_url}?sort=end_date")
        assert response.status_code == HTTPStatus.OK
        page_obj = response.context["page_obj"]
        programs = page_obj.object_list
        expected_programs = sorted(self.programs, key=lambda p: p.end_date)
        self.check_order(programs, expected_programs[:10])

    def test_ordering_by_invalid_field(self, client):
        response = self.client.get(f"{self.list_url}?sort=invalid")
        assert response.status_code == HTTPStatus.OK
        page_obj = response.context["page_obj"]
        programs = page_obj.object_list
        expected_programs = sorted(self.programs, key=lambda p: p.name)
        self.check_order(programs, expected_programs[:10])

    @staticmethod
    def check_order(programs, expected_programs):
        for program, expected_program in zip(programs, expected_programs):  # Adjust for pagination
            assert program.name == expected_program.name


@pytest.mark.django_db
class TestProgramCreateOrUpdateView(BaseProgramTest):
    @pytest.fixture(autouse=True)
    def test_setup(self):
        self.program = ProgramFactory.create(organization=self.organization)
        self.delivery_type = DeliveryTypeFactory.create()
        self.init_url = reverse("program:init", kwargs={"org_slug": self.organization.slug})
        self.edit_url = reverse("program:edit", kwargs={"org_slug": self.organization.slug, "pk": self.program.pk})

    def test_create_view(self):
        response = self.client.get(self.init_url)
        assert response.status_code == HTTPStatus.OK
        assert "program/program_add.html" in response.templates[0].name

    def test_create_program(self):
        data = {
            "name": "New Program",
            "description": "A description for the new program",
            "delivery_type": self.delivery_type.id,
            "budget": 10000,
            "currency": "USD",
            "start_date": "2024-01-01",
            "end_date": "2024-12-31",
        }
        response = self.client.post(self.init_url, data)
        assert response.status_code == HTTPStatus.FOUND
        new_program = Program.objects.get(name="New Program")
        assert new_program.name == "New Program"
        assert new_program.organization.slug == self.organization.slug
        assert "Program 'New Program' created successfully." in [
            msg.message for msg in messages.get_messages(response.wsgi_request)
        ]
        assert response.url == self.list_url

    def test_update_view(self):
        response = self.client.get(self.edit_url)
        assert response.status_code == HTTPStatus.OK
        assert "program/program_edit.html" in response.templates[0].name

    def test_update_program(self):
        data = {
            "name": "Updated Program Name",
            "description": "Updated description",
            "delivery_type": self.delivery_type.id,
            "organization": self.organization.id,
            "budget": 15000,
            "currency": "EUR",
            "start_date": "2024-02-01",
            "end_date": "2024-11-30",
        }
        response = self.client.post(self.edit_url, data)
        assert response.status_code == HTTPStatus.FOUND
        old_org = self.program.organization.slug
        self.program.refresh_from_db()
        assert self.program.name == "Updated Program Name"
        assert self.program.organization.slug == old_org
        assert "Program 'Updated Program Name' updated successfully." in [
            msg.message for msg in messages.get_messages(response.wsgi_request)
        ]
        assert response.url == self.list_url


@pytest.mark.django_db
class TestInviteOrganizationView(BaseProgramTest):
    @pytest.fixture(autouse=True)
    def test_setup(self, organization: Organization):
        self.invite_organization = organization
        self.managed_opportunity = ManagedOpportunityFactory.create(organization=self.organization)
        self.valid_url = reverse(
            "program:invite_organization",
            kwargs={
                "org_slug": self.organization.slug,
                "pk": self.managed_opportunity.program.pk,
                "opp_id": self.managed_opportunity.pk,
            },
        )

    def test_successful_invitation(self):
        data = {
            "organization": self.invite_organization.slug,
        }
        response = self.client.post(self.valid_url, data)
        assert response.status_code == HttpResponseRedirect.status_code
        assert ManagedOpportunityApplication.objects.filter(
            managed_opportunity=self.managed_opportunity,
            organization=self.invite_organization,
            status=ManagedOpportunityApplicationStatus.INVITED,
        ).exists()
        assert "Organization invited successfully!" in [
            msg.message for msg in messages.get_messages(response.wsgi_request)
        ]

    def test_invalid_organization_slug(self):
        data = {
            "organization": "invalid_slug",
        }
        response = self.client.post(self.valid_url, data)
        assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.django_db
class TestManagedOpportunityApplicationListView(BaseProgramTest):
    @pytest.fixture(autouse=True)
    def test_setup(self, organization: Organization):
        self.managed_opportunity = ManagedOpportunityFactory.create(organization=self.organization)
        self.apllications = ManagedOpportunityApplicationFactory.create_batch(
            20, managed_opportunity=self.managed_opportunity
        )
        self.list_url = reverse(
            "program:opportunity_application_list",
            kwargs={
                "org_slug": self.organization.slug,
                "pk": self.managed_opportunity.program.pk,
                "opp_id": self.managed_opportunity.pk,
            },
        )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(self.list_url)
        assert response.status_code == HTTPStatus.OK
        assert "program/managed_opportunity_application_list.html" in response.templates[0].name
        context = response.context_data
        assert "object_list" in context
        assert "pk" in context
        assert "opportunity" in context
        assert "organizations" in context
        assert context["pk"] == self.managed_opportunity.program.pk
        assert context["opportunity"].pk == self.managed_opportunity.pk

    def test_list_applications(self):
        response = self.client.get(self.list_url)
        assert response.status_code == HTTPStatus.OK
        applications = response.context_data["object_list"]
        assert len(applications) == 15

    def test_pagination(self):
        response = self.client.get(f"{self.list_url}?page=2")
        assert response.status_code == HTTPStatus.OK
        assert len(response.context_data["object_list"]) == 5


@pytest.mark.django_db
class TestManageApplicationView(BaseProgramTest):
    @pytest.fixture(autouse=True)
    def test_setup(self):
        self.managed_opportunity = ManagedOpportunityFactory.create(organization=self.organization)
        self.application = ManagedOpportunityApplicationFactory.create(managed_opportunity=self.managed_opportunity)
        self.application_list_url = reverse(
            "program:opportunity_application_list",
            kwargs={
                "org_slug": self.organization.slug,
                "pk": self.managed_opportunity.program.id,
                "opp_id": self.managed_opportunity.id,
            },
        )

    def test_accept_application(self):
        url = reverse(
            "program:manage_application",
            kwargs={
                "org_slug": self.organization.slug,
                "application_id": self.application.id,
                "action": "accept",
            },
        )
        response = self.client.post(url)
        assert response.status_code == HTTPStatus.FOUND
        assert response.url == self.application_list_url
        self.application.refresh_from_db()
        assert self.application.status == ManagedOpportunityApplicationStatus.ACCEPTED
        assert "Application has been accepted successfully." in [
            msg.message for msg in messages.get_messages(response.wsgi_request)
        ]

    def test_reject_application(self):
        url = reverse(
            "program:manage_application",
            kwargs={
                "org_slug": self.organization.slug,
                "application_id": self.application.id,
                "action": "reject",
            },
        )
        response = self.client.post(url)
        assert response.status_code == HTTPStatus.FOUND
        assert response.url == self.application_list_url
        self.application.refresh_from_db()
        assert self.application.status == ManagedOpportunityApplicationStatus.REJECTED
        assert "Application has been rejected successfully." in [
            msg.message for msg in messages.get_messages(response.wsgi_request)
        ]

    def test_invalid_action(self):
        url = reverse(
            "program:manage_application",
            kwargs={
                "org_slug": self.organization.slug,
                "application_id": self.application.id,
                "action": "invite",
            },
        )
        response = self.client.post(url)
        assert response.status_code == HTTPStatus.FOUND
        assert self.application.status == ManagedOpportunityApplicationStatus.INVITED
        assert "Action not allowed." in [msg.message for msg in messages.get_messages(response.wsgi_request)]
