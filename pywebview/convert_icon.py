from PIL import Image
import os
filename = os.path.join(__file__, '..', 'src', 'assets', 'icon.png')
img = Image.open(filename, 'r')
img.save('favicon.ico', sizes=[(32, 32)])