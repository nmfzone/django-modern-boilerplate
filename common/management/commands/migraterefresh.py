from django.apps import apps
from django.apps.config import AppConfig
from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Reset and re-run all migrations'

    def add_arguments(self, parser):
        parser.add_argument('--seed', nargs='*', help='Run the DB seeders.')

    def handle(self, *app_labels, **options):
        try:
            if app_labels and len(app_labels) > 0:
                app_configs = [apps.get_app_config(app_label) for app_label in app_labels]
            else:
                app_configs = [AppConfig.create(app_label) for app_label in settings.INSTALLED_APPS]
        except (LookupError, ImportError) as e:
            raise CommandError("%s. Are you sure your INSTALLED_APPS setting is correct?" % e)

        for app_config in app_configs:
            try:
                call_command('migrate', app_config.name.split('.')[-1], 'zero')
            except CommandError:
                continue

        call_command('migrate')

        if options['seed'] is not None:
            if len(options['seed']) == 0:
                call_command('seed')
            else:
                call_command('seed', *options['seed'])
