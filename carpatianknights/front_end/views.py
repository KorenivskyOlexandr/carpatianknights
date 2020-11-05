from django.shortcuts import render
import datetime
from .services import get_gallery_image_list


def main_page(request):
    year = datetime.datetime.now()
    return render(request, 'main.html', {"year": year, "images": get_gallery_image_list()})
