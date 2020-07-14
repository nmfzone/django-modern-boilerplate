import factory
import pydash
from django.apps import apps
from django.apps.config import AppConfig
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from importlib import import_module


class Command(BaseCommand):
    help = 'Run Database seeders'

    args = "[appname ...]"

    missing_args_message = None

    def add_arguments(self, parser):
        parser.add_argument('args', default=[], metavar='app_label', nargs='*', help='One or more application label.')

    @factory.Faker.override_default_locale(getattr(settings, 'FAKER_LOCALE', 'en_US'))
    def handle(self, *app_labels, **options):
        try:
            if app_labels and len(app_labels) > 0:
                app_configs = [apps.get_app_config(app_label) for app_label in app_labels]
            else:
                app_configs = [AppConfig.create(app_label) for app_label in settings.INSTALLED_APPS]
        except (LookupError, ImportError) as e:
            raise CommandError("%s. Are you sure your INSTALLED_APPS setting is correct?" % e)

        seeders = []
        for app_config in app_configs:
            try:
                module_seeders = import_module('%s.%s' % (app_config.name, 'seeders'))
            except ImportError:
                continue

            if callable(getattr(module_seeders, 'handle', None)):
                seeders.append({
                    'order': getattr(module_seeders, 'order', 0),
                    'handle': module_seeders.handle
                })
            else:
                raise AttributeError("You should define 'handle' method in %s." % (app_config.name + '.seeders'))

        seeders = pydash.sort(seeders, key=lambda item: item['order'])

        for seeder in seeders:
            seeder['handle'](self)

        self.stdout.write(self.style.SUCCESS('Database seeding completed successfully.'))
