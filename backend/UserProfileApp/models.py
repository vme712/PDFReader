import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if username is None:
            raise TypeError('Username обязательное поле.')
        if email is None:
            raise TypeError('Email обязательное поле.')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):
        if username is None:
            raise TypeError('Username обязательное поле.')
        if email is None:
            raise TypeError('Email обязательное поле.')
        if password is None:
            raise TypeError('Пароль обязательное поле.')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField('Дата регистрации', auto_now_add=True)
    updated_at = models.DateTimeField('Дата последнего изменения', auto_now=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', ]

    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        db_table = 'Users'

    def __str__(self):
        return f'{self.username}'

    @property
    def token(self):
        return self._generate_jwt_token()

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def _generate_jwt_token(self):
        return jwt.encode({'user_data': {'id': self.pk, 'username': self.username,
                                         'created_date': str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))},
                           'exp': datetime.now() + timedelta(days=60),
                           'iat': datetime.now(),
                           }, settings.SECRET_KEY, algorithm='HS256')
