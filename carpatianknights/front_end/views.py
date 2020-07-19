from django.shortcuts import render
import datetime
from .models import Photo


def main_page(request):
    year = datetime.datetime.now()
    images_list = Photo.objects.filter(
        title__startswith="gallery")  # в слайдер попадають стиснені фотографігі які починаються на "gallery"
    return render(request, 'main.html', {"year": year, "images": images_list})
