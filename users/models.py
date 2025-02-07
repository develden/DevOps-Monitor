from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Определяем роли: администратор и обычный пользователь
    ROLE_CHOICES = (
        ('admin', 'Администратор'),
        ('user', 'Пользователь'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

    def __str__(self):
        return self.username 