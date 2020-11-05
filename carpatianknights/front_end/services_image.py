from .models import Photo


def get_gallery_image_list():
    return Photo.objects.filter(
        title__startswith="gallery")  # в слайдер попадають стиснені фотографігі які починаються на "gallery"
