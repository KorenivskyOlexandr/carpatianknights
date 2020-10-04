from django.db import models
from django.conf import settings
from django.core.validators import *
from django.utils.text import slugify
from django.urls import reverse
import datetime
from django.contrib.auth.models import User
from carpatianknights.front_end.models import Photo
from carpatianknights.front_end.services import compress_image


class Route(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    short_description = models.TextField(max_length=2000)
    slug = models.SlugField(max_length=250, unique=True)
    complexity = models.IntegerField(
        validators=[MaxValueValidator(limit_value=10, message='Складність не має бути вище 10'),
                    MinValueValidator(limit_value=1, message='Складність не має бути нижче 1')])
    title_img = models.ImageField(upload_to='route_img/', null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('route:detail', args=[self.id, self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        if self.title_img:
            self.title_img = compress_image(self.title_img, (1200, 720))
        super(Route, self).save(*args, **kwargs)


class ActiveRoute(models.Model):
    routes_id = models.ForeignKey(Route, on_delete=models.CASCADE)
    start_day = models.DateField()
    stop_day = models.DateField()
    leader = models.CharField(max_length=256)
    status = models.BooleanField(default=False)
    is_full = models.BooleanField(default=False)
    free_places = models.IntegerField(default=0)

    def add_user(self):
        if self.free_places > 0:
            self.free_places -= 1
            self.save()
        else:
            raise ValidationError(
                "Похід немає вільних місць")

    def remove_user(self):
        self.free_places += 1
        self.save()

    def save(self, *args, **kwargs):
        if (self.start_day >= self.stop_day or self.start_day < datetime.date.today()) and self.status:
            raise ValidationError(
                "Дата початку має бути меншою за дату кінця, тако ж більшою або рівною сьогоднішній")
        if self.free_places == 0:
            self.is_full = True
        else:
            self.is_full = False
        super(ActiveRoute, self).save(*args, **kwargs)

    def __str__(self):
        return self.routes_id.name


class PhotoToRoutes(Photo):
    routes_id = models.ForeignKey(
        Route, on_delete=models.CASCADE, related_name='photos')


class Tour(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    active_route_id = models.ForeignKey(ActiveRoute, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)

    class Meta:
        unique_together = ("user_id", "active_route_id")

    def __str__(self):
        return "Відчайдуха - {}; Похід - {}. Початок - {}. Кінець - {}; Статус - {}".format(
            self.user_id.get_full_name(), self.active_route_id, self.active_route_id.start_day,
            self.active_route_id.stop_day, 'Підтверджено на похід' if self.status else 'Потребує підтвердження')
