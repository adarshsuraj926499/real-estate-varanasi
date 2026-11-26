import os

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Create or repair the one-time Render admin from temporary environment variables."

    username_variable = "RENDER_BOOTSTRAP_ADMIN_USERNAME"
    password_variable = "RENDER_BOOTSTRAP_ADMIN_PASSWORD"

    def handle(self, *args, **options):
        username = os.environ.get(self.username_variable, "").strip()
        password = os.environ.get(self.password_variable, "")

        if not username and not password:
            self.stdout.write("No temporary Render admin credentials configured; skipping.")
            return
        if not username or not password:
            raise CommandError(
                f"Set both {self.username_variable} and {self.password_variable}, "
                "or remove both."
            )

        user_model = get_user_model()
        user, created = user_model.objects.get_or_create(username=username)

        if user.is_superuser and user.is_active and user.check_password(password):
            self.stdout.write(f"Render admin '{username}' is already configured.")
            return

        try:
            validate_password(password, user)
        except ValidationError as exc:
            raise CommandError("Choose a stronger password that passes Django validation.") from exc

        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save(
            update_fields=("password", "is_active", "is_staff", "is_superuser")
        )

        action = "Created" if created else "Updated"
        self.stdout.write(f"{action} Render superuser '{username}'.")
