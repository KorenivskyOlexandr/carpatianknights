from django.db import models
from django.conf import settings
from django.core.validators import *
import datetime


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    phone_number = models.IntegerField(unique=True)
    date_of_birth = models.DateField()
    date_of_registration = models.DateField(default=datetime.date.today())
    user_rang = models.IntegerField(default=0)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)

    def save(self, *args, **kwargs):
        self.clean()
        super(Profile, self).save(*args, **kwargs)

    def clean(self):
        date_16 = datetime.timedelta(days=5840)
        if (datetime.date.today() - self.date_of_birth) < date_16:
            raise ValidationError(
                "16+, або супровід батьків")

    def __str__(self):
        return self.user.get_full_name()
