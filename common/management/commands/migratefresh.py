from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Delete all tables and run all migrations'

    def add_arguments(self, parser):
        parser.add_argument('--seed', nargs='*', help='Run the DB seeders.')

    def handle(self, *app_labels, **options):
        tables = connection.introspection.table_names()

        if len(tables) > 0:
            connection.disable_constraint_checking()

            schema_editor = connection.schema_editor()
            schema_editor.execute(schema_editor.sql_delete_table % {
                'table': ','.join(tables)
            })

            connection.enable_constraint_checking()

        call_command('migrate')

        if options['seed'] is not None:
            if len(options['seed']) == 0:
                call_command('seed')
            else:
                call_command('seed', *options['seed'])
