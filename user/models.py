from django.db import models

# Create your models here.
USER_TYPE = (
    (1, 'User'),
    (2, 'Admin'),
)


class Users(models.Model):
    username = models.CharField('Username', max_length=100)
    password1 = models.CharField('Password', max_length=12)
    password2 = models.CharField('Password', max_length=12)
    name = models.CharField('Name', max_length=100)
    is_active = models.BooleanField('Active', default=False)
    user_type = models.BigIntegerField('User Type', choices=USER_TYPE, default=1)

    def save(self, *args, **kwargs):
        self.is_active = True
        super(Users, self).save(*args, **kwargs)


