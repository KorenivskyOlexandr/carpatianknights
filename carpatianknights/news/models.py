import sys
import datetime
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager
from django.core.validators import *


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

    def __str__(self):
        return '{}/media/{}'.format(server, self.image)

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


class Routes(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=4096)
    complexity = models.IntegerField(
        validators=[MaxValueValidator(limit_value=10, message='Складність не має бути вище 10'),
                    MinValueValidator(limit_value=1, message='Складність не має бути нижче 1')])

    def __str__(self):
        return self.name


class ActiveRoutes(models.Model):
    routes_id = models.ForeignKey(Routes, on_delete=models.CASCADE)
    start_day = models.DateField()
    stop_day = models.DateField()
    leader = models.CharField(max_length=256)
    status = models.BooleanField(default=False)
    is_full = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.start_day >= self.stop_day or self.start_day < datetime.date.today():
            raise ValidationError(
                "Дата початку має бути меншою за дату кінця, тако ж більшою або рівною сьогоднішній")
        super(ActiveRoutes, self).save(*args, **kwargs)

    def __str__(self):
        return "%s %s %s %s %s" % (self.routes_id, self.start_day,
                                   self.stop_day, self.leader, self.status)


class PhotoToPost(Photo):
    post_id = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='photos')


class PhotoToRoutes(Photo):
    routes_id = models.ForeignKey(
        Routes, on_delete=models.CASCADE, related_name='photos')
