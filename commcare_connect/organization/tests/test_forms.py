import pytest
from django.test import Client
from django.urls import reverse

from commcare_connect.organization.models import Organization
from commcare_connect.users.tests.factories import UserFactory


class TestAddMembersView:
    @pytest.fixture(autouse=True)
    def setup(self, organization: Organization, client: Client):
        self.url = reverse("organization:add_members", kwargs={"org_slug": organization.slug})
        self.user = organization.memberships.filter(role="admin").first().user
        self.client = client
        client.force_login(self.user)

    @pytest.mark.django_db
    @pytest.mark.parametrize(
        "email_or_username, role, expected_status_code, create_user, expected_role, should_exist",
        [
            ("testformember@example.com", "member", 302, True, "member", True),
            ("testforadmin@example.com", "admin", 302, True, "admin", True),
            ("testforusername", "member", 302, True, "member", True),
            ("testforusername", "admin", 302, True, "admin", True),
            ("nonexistent@example.com", "member", 302, False, None, False),
            ("existing@example.com", "admin", 302, True, "member", True),
        ],
    )
    def test_add_member(
        self,
        email_or_username,
        role,
        expected_status_code,
        create_user,
        expected_role,
        should_exist,
        organization,
    ):
        if create_user:
            user = UserFactory(
                email=email_or_username if "@" in email_or_username else None,
                username=email_or_username if "@" not in email_or_username else None,
            )

            if email_or_username == "existing@example.com":
                organization.members.add(user, through_defaults={"role": expected_role})

        data = {"email_or_username": email_or_username, "role": role}
        response = self.client.post(self.url, data)

        membership_filter = (
            {"user__email": email_or_username} if "@" in email_or_username else {"user__username": email_or_username}
        )

        assert response.status_code == expected_status_code
        membership_exists = organization.memberships.filter(**membership_filter).exists()
        assert membership_exists == should_exist

        if should_exist and expected_role:
            membership = organization.memberships.get(**membership_filter)
            assert membership.role == expected_role
