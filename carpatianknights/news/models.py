import sys
import datetime
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from taggit.managers import TaggableManager
from django.core.validators import *
from django.conf import settings
from django.db.models import signals
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.utils.html import strip_tags

# server = 'https://carpatianapi.herokuapp.com'
server = 'http://127.0.0.1:8000'


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='news_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='draft')

    objects = models.Manager()  # Менеджер по умолчанию.
    published = PublishedManager()  # Наш новый менеджер.
    tags = TaggableManager()

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news:post_detail', args=[self.publish.year,
                                                 self.publish.month, self.publish.day, self.slug])


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)


class Photo(models.Model):
    image = models.ImageField()
    title = models.CharField(max_length=100)

    class Meta:
        ordering = ['title']

    def get_url(self):
        return '{}/media/{}'.format(server, self.image)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.image = self.compress_image(self.image)
        super(Photo, self).save(*args, **kwargs)

    def compress_image(self, image):
        image_temproary = Image.open(image)
        outputIoStream = BytesIO()
        image_temproary.resize((1920, 1080))
        image_temproary.save(outputIoStream, format='JPEG', quality=50)
        outputIoStream.seek(0)
        uploaded_image = InMemoryUploadedFile(outputIoStream, 'ImageField', "%s.jpg" % image.name.split('.')[0],
                                              'image/jpeg', sys.getsizeof(outputIoStream), None)
        return uploaded_image


class Route(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=4096)
    short_description = models.TextField(max_length=1000)
    slug = models.SlugField(max_length=250, unique=True)
    complexity = models.IntegerField(
        validators=[MaxValueValidator(limit_value=10, message='Складність не має бути вище 10'),
                    MinValueValidator(limit_value=1, message='Складність не має бути нижче 1')])

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('route:detail', args=[self.id, self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
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
        if self.start_day >= self.stop_day or self.start_day < datetime.date.today():
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


class PhotoToPost(Photo):
    post_id = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='photos')


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
                                                       'url': server,
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
