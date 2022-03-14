# https://simpleisbetterthancomplex.com/tutorial/2018/08/27/how-to-create-custom-django-management-commands.html

import os

from django.apps import apps
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.core.management import call_command
from django.core.management.base import BaseCommand
from account.choice import SystemDefaultGroup


class Command(BaseCommand):
    help = "Seeding a database is a process in which an initial set of data is provided to a database when it is being installed."

    def __init__(self):
        self.user_class = get_user_model()

        super(Command, self).__init__()

    def handle(self, *args, **options):
        self.all_apps_make_migration()
        self.migrate()
        self.create_super_user()
        self.create_group()
        self.dump_data()

    def create_super_user(self):
        if not os.getenv("ADMIN_USER_NAME") or not os.getenv("ADMIN_PASSWORD"):
            self.stdout.write(
                self.style.HTTP_BAD_REQUEST("Environment variable is not set.")
            )
            return False

        if self.user_class.objects.filter(
            username=os.getenv("ADMIN_USER_NAME")
        ).exists():
            self.stdout.write(self.style.HTTP_INFO("Admin : Already created."))
            return False

        self.user_class.objects.create_superuser(
            username=os.getenv("ADMIN_USER_NAME"),
            password=os.getenv("ADMIN_PASSWORD"),
        )

        self.stdout.write(
            self.style.SUCCESS(
                "Created {} admin account.".format(os.getenv("ADMIN_USER_NAME"))
            )
        )

    def create_group(self):
        for group in SystemDefaultGroup.choices:
            Group.objects.get_or_create(name=group[0])
        self.stdout.write(self.style.SUCCESS("Created default group."))

    def assign_permission_to_group(self):
        GROUPS = [""]
        MODELS = [""]
        PERMISSIONS = [
            "view",
        ]  # For now only view permission by default for all, others include add, delete, change

        for group in GROUPS:
            new_group, created = Group.objects.get_or_create(name=group)
            for model in MODELS:
                for permission in PERMISSIONS:
                    name = "Can {} {}".format(permission, model)
                    self.stdout.write(self.style.HTTP_INFO("Creating {}".format(name)))
                    try:
                        model_add_perm = Permission.objects.get(name=name)
                    except Permission.DoesNotExist:
                        self.stdout.write(
                            self.style.WARNING(
                                "Permission not found with name '{}'.".format(name)
                            )
                        )
                        continue
                    new_group.permissions.add(model_add_perm)

        self.stdout.write(self.style.SUCCESS("Created default group and permissions."))

    def all_apps_make_migration(self):
        for app in apps.get_app_configs():
            call_command("makemigrations", app.label)
            self.stdout.write("Created {} migration.".format(app.label))

    def migrate(self):
        call_command("migrate")

    def dump_data(self):
        call_command("loaddata", "fixtures/group_type.json")
