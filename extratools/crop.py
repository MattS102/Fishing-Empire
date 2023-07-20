import os
from PIL import Image

for root, subdirs, files in os.walk("~ Your Image Path ~):
    print(root, subdirs, files)
    for file in files:
        if file.endswith('.png'):
            path = os.path.join(root, file)
            with Image.open(path) as image:
                new_image = image.crop(image.getbbox())
                new_image.save(path)



