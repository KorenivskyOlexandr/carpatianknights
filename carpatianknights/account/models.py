from django.db import models
from django.conf import settings
from django.core.validators import *


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    phone_number = models.IntegerField(unique=True)
    age = models.IntegerField(validators=[MinValueValidator(
        limit_value=16, message='16+, або супровід батьків')])
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)

    def __str__(self):
        return self.user.get_full_name()

# def save(self, *args, **kwargs):
        # if self.start_day >= self.stop_day or self.start_day < datetime.date.today():
        #     raise ValidationError("Дата початку має бути меншою за дату кінця, тако ж більшою або рівною сьогоднішній")
        # super(ActiveRoutes, self).save(*args, **kwargs)
