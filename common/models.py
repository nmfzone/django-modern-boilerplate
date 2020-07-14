from common.db import models as common_models
from common.managers import UserManager
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from model_utils.fields import AutoCreatedField, AutoLastModifiedField


class IndexedTimeStampedModel(models.Model):
    created_at = AutoCreatedField(db_index=True)
    updated_at = AutoLastModifiedField(db_index=True)

    class Meta:
        abstract = True


class User(AbstractBaseUser, IndexedTimeStampedModel):
    id = common_models.PositiveBigAutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name='ID'
    )
    email = models.EmailField(
        max_length=255,
        unique=True,
    )
    name = models.CharField(
        max_length=255,
    )
    username = models.CharField(
        max_length=30,
        unique=True,
    )
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    AUTH_FIELDS = ['email', 'username']
    REQUIRED_FIELDS = ['email', 'name', 'password']

    def natural_key(self):
        return self.email, self.username

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    def __str__(self):
        return self.email
