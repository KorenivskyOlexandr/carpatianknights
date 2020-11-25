from django.shortcuts import render
from .services_image import get_gallery_image_list


def main_page(request):
    return render(request, 'main.html', {"images": get_gallery_image_list()})
