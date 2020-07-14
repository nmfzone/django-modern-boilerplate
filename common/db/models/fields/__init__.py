from django.db.models import fields
from django.utils.translation import gettext_lazy as _

__all__ = [
    'PositiveAutoField', 'PositiveBigAutoField', 'PositiveBigIntegerField',
]


class PositiveAutoField(fields.AutoField):
    default_error_messages = {
        'invalid': _("'%(value)s' value must be a positive integer."),
    }

    def db_type(self, connection):
        if 'mysql' in connection.__class__.__module__:
            return 'int unsigned AUTO_INCREMENT'

        return super().db_type(connection)

    def rel_db_type(self, connection):
        return fields.PositiveIntegerField().db_type(connection=connection)


class PositiveBigAutoField(PositiveAutoField):
    def db_type(self, connection):
        if 'mysql' in connection.__class__.__module__:
            return 'bigint unsigned AUTO_INCREMENT'

        return super().db_type(connection)

    def rel_db_type(self, connection):
        return PositiveBigIntegerField().db_type(connection=connection)


class PositiveBigIntegerField(fields.BigIntegerField):
    def db_type(self, connection):
        if 'mysql' in connection.__class__.__module__:
            return 'bigint unsigned'

        return super().db_type(connection)

    def db_check(self, connection):
        data = self.db_type_parameters(connection)

        if 'oracle' in connection.__class__.__module__:
            return '%(qn_column)s >= 0' % data
        elif 'postgresql' in connection.__class__.__module__:
            return '"%(column)s" >= 0' % data
        elif 'sqlite3' in connection.__class__.__module__:
            return '"%(column)s" >= 0' % data

        return super().db_check(connection)

    def formfield(self, **kwargs):
        return super().formfield(**{
            'min_value': 0,
            **kwargs,
        })
