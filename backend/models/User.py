from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from datetime import datetime


class UserManager(BaseUserManager):

    def create_user(self, **kwargs):

        user = self.model(username=kwargs["username"])

        user.save(using=self._db)
        return user

    def create_superuser(self, **kwargs):

        user = self.model(
            username=kwargs["username"],
            is_admin=True,
            is_active=True,
        )

        user.save(using=self._db)
        return user


class User(PermissionsMixin, AbstractBaseUser):
    username = models.CharField(max_length=20, unique=True, db_index=True)
    date_joined = models.DateTimeField(default=datetime.utcnow, blank=True)

    is_active = models.BooleanField(default=True, blank=True)
    is_admin = models.BooleanField(default=False, blank=True)

    email = models.CharField(max_length=100, unique=True, blank=True, default=None, null=True)

    current_room = models.ForeignKey('backend.Room', blank=True, null=True, default=None)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_profile(self):
        return "/users/" + str(self.pk)

    def get_short_name(self):
        return self.username

    def has_perm(self, perm, obj=None):
        # handle certain permissions
        return True

    def has_module_perms(self, app_label):
        # has permission to view particular "app_label"
        return True

    def __unicode__(self):
        return self.username

    class Meta:
        app_label = "backend"
        db_table = "user"
