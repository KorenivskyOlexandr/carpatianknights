from django.db import models
from .services import compress_image


class Photo(models.Model):
    image = models.ImageField()
    title = models.CharField(max_length=100)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.image = compress_image(self.image)
        super(Photo, self).save(*args, **kwargs)
