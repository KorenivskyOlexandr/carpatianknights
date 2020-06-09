from django.shortcuts import render
import datetime
from .models import Photo
import git
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from carpatianknights.settings import BASE_DIR


def main_page(request):
    year = datetime.datetime.now()
    images_list = Photo.objects.filter(
        title__startswith="gallery")  # в слайдер попадають стиснені фотографігі які починаються на "gallery"
    return render(request, 'main.html', {"year": year, "images": images_list})


@csrf_exempt
def update(request):
    if request.method == "POST":

        repo = git.Repo(BASE_DIR)
        origin = repo.remotes.origin

        origin.pull()

        return HttpResponse("Updated code on server")
    else:
        return HttpResponse("Couldn't update the code on server")
        # test comment
