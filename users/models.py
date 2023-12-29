from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import EmailValidator
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True, validators=[EmailValidator()])

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
