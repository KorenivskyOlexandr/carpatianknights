from django.shortcuts import render
import datetime
from .models import Photo
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from carpatianknights.settings import BASE_DIR
import subprocess


def main_page(request):
    year = datetime.datetime.now()
    images_list = Photo.objects.filter(
        title__startswith="gallery")  # в слайдер попадають стиснені фотографігі які починаються на "gallery"
    return render(request, 'main.html', {"year": year, "images": images_list})


@csrf_exempt
def update(request):
    if request.method == "POST":

        rc = subprocess.call("{}/prod_git_pull_fetch.sh".format(BASE_DIR))

        return HttpResponse("Updated code on server")
    else:
        return HttpResponse("Couldn't update the code on server")
        # test comment

