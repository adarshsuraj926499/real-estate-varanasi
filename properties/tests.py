import os
from io import StringIO
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase


class BootstrapRenderAdminCommandTests(TestCase):
    username = "reena"
    password = "Fresh-Unique-Test-Password-482!"

    def run_bootstrap(self, username=None, password=None):
        variables = {
            "RENDER_BOOTSTRAP_ADMIN_USERNAME": username or "",
            "RENDER_BOOTSTRAP_ADMIN_PASSWORD": password or "",
        }
        with patch.dict(os.environ, variables, clear=False):
            output = StringIO()
            call_command("bootstrap_render_admin", stdout=output)
        return output.getvalue()

    def test_creates_superuser_from_temporary_environment(self):
        output = self.run_bootstrap(self.username, self.password)

        user = get_user_model().objects.get(username=self.username)
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.check_password(self.password))
        self.assertNotIn(self.password, output)

    def test_repairs_existing_user_and_is_idempotent(self):
        user = get_user_model().objects.create_user(
            username=self.username,
            password="Old-Unique-Test-Password-593!",
            is_active=False,
            is_staff=False,
        )

        self.run_bootstrap(self.username, self.password)
        user.refresh_from_db()
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.check_password(self.password))

        output = self.run_bootstrap(self.username, self.password)
        self.assertIn("already configured", output)
        self.assertEqual(get_user_model().objects.count(), 1)

    def test_skips_when_temporary_credentials_are_absent(self):
        output = self.run_bootstrap()
        self.assertIn("skipping", output)
        self.assertFalse(get_user_model().objects.exists())

    def test_rejects_partial_temporary_credentials(self):
        with self.assertRaises(CommandError):
            self.run_bootstrap(self.username)
        self.assertFalse(get_user_model().objects.exists())
