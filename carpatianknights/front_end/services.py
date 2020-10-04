from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys


def compress_image(image, size=False):
    image_temproary = Image.open(image)
    outputIoStream = BytesIO()
    if size:
        imageTemproaryResized = image_temproary.resize(size)
    else:
        imageTemproaryResized = image_temproary.resize((1920, 1080))
    imageTemproaryResized.save(outputIoStream, format='JPEG', quality=50)
    outputIoStream.seek(0)
    uploaded_image = InMemoryUploadedFile(outputIoStream, 'ImageField', "%s.jpg" % image.name.split('.')[0],
                                          'image/jpeg', sys.getsizeof(outputIoStream), None)
    return uploaded_image