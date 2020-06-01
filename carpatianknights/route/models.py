from django.db import models
from django.conf import settings
from django.db.models import signals
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.core.validators import *
from django.utils.text import slugify
from django.urls import reverse
import datetime
from django.contrib.auth.models import User
from carpatianknights.front_end.models import Photo, compress_image


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
        return "%s %s %s %s %s" % (self.routes_id, self.start_day,
                                   self.stop_day, self.leader, self.status)


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
        return "%s %s %s" % (self.user_id, self.active_route_id, self.status)


@receiver(signals.post_save, sender=Tour)
def notify_admin(instance, created, **kwargs):
    """Сповіщення адмінів про реєстрацію користувача на похід"""
    if created:
        user = instance.user_id
        active_route = instance.active_route_id
        html_message = render_to_string('admin.html', {'route': active_route.routes_id,
                                                       'start_day': active_route.start_day,
                                                       'stop_day': active_route.stop_day,
                                                       'leader': active_route.leader,
                                                       'full_name': user.get_full_name(),
                                                       'phone': user.profile.phone_number,
                                                       'age': user.profile.date_of_birth,
                                                       'email': user.email,
                                                       'url': settings.SERVER,
                                                       'tour_id': instance.id
                                                       })
        plain_message = strip_tags(html_message)
        send_mail(
            subject='Карпатські Відчайдухи',
            message=plain_message,
            from_email='carpatianknights@gmail.com',
            recipient_list=['carpatianknights@ukr.net', 's5a5s5h5a5@ukr.net'],
            html_message=html_message,
            fail_silently=False,
        )


@receiver(signals.pre_save, sender=Tour)
def notify_users(instance, **kwargs):
    """Сповіщення юзера про те що його прийнято в похід,
        а також збільшення/зменшення кількості вільних місць в поході"""
    status = False
    try:
        tour = Tour.objects.get(id=instance.id)
        status = tour.status
    except Exception:
        pass
    if instance.status != status:
        if instance.status:
            user = instance.user_id
            active_route = instance.active_route_id
            if active_route.is_full:
                raise ValidationError(
                    "Похід немає вільних місць")
            else:
                active_route.add_user()
                sent_user_mail(user, active_route)
        else:
            instance.active_route_id.remove_user()


@receiver(signals.post_delete, sender=Tour)
def remove_user(instance, **kwargs):
    instance.active_route_id.remove_user()


def sent_user_mail(user, active_route):
    html_message = render_to_string('mail.html', {'route': active_route.routes_id,
                                                  'start_day': active_route.start_day,
                                                  'stop_day': active_route.stop_day,
                                                  'leader': active_route.leader,
                                                  'url': 'https://carpatianknights.ml'  # ! change url !
                                                  })
    plain_message = strip_tags(html_message)
    send_mail(
        subject='Карпатські Відчайдухи',
        message=plain_message,
        from_email='carpatianknights@gmail.com',
        recipient_list=[user.email],
        html_message=html_message,
        fail_silently=False,
    )
