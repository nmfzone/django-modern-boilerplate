from django.contrib.auth.models import BaseUserManager
from django.db.models import Q
from functools import reduce


class UserManager(BaseUserManager):

    def create_user(self, email, password, name, username):
        user = self.model(
            email=self.normalize_email(email),
            name=name,
            username=username
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, name, username):
        user = self.model(
            email=self.normalize_email(email),
            name=name,
            username=username
        )
        user.set_password(password)
        user.is_admin = True
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, username):
        return self.get(reduce(lambda x, y: x | y, [Q(**{item: username}) for item in self.model.AUTH_FIELDS]))
