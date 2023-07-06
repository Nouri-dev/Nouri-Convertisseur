import os
from PIL import Image


class ImageProcessor:

    @staticmethod
    def image_reduce_convert(path, size, quality, folder):
        image = Image.open(path)
        width, height = image.size
        new_width = round(width * size)
        new_height = round(height * size)
        resized_image = image.resize((new_width, new_height), Image.LANCZOS)
        parent_dir = os.path.dirname(path)
        reduced_path = os.path.join(parent_dir, folder, os.path.basename(path))

        if not os.path.exists(parent_dir):
            os.makedirs(parent_dir)

        resized_image.save(reduced_path, optimize=True, quality=quality)
        return os.path.exists(reduced_path)
