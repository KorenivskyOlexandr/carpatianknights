from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys


def compress_image(image, size=False):
    image_temp = Image.open(image)
    if image_temp.mode in ("RGBA", "P"):
        image_temp = image_temp.convert("RGB")
    output_io_stream = BytesIO()
    if size:
        image_temp_resized = image_temp.resize(size)
    else:
        image_temp_resized = image_temp.resize((1920, 1080))
    image_temp_resized.save(output_io_stream, format='JPEG', quality=50)
    output_io_stream.seek(0)
    uploaded_image = InMemoryUploadedFile(output_io_stream, 'ImageField', "%s.jpg" % image.name.split('.')[0],
                                          'image/jpeg', sys.getsizeof(output_io_stream), None)
    return uploaded_image
