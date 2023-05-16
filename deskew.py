from wand.image import Image
from wand.display import display
import os
from os import listdir
 
"""# get the path/directory
folder_dir = "datasets/"

for images in os.listdir(folder_dir):
    with Image(filename=folder_dir+images) as img:
        img.deskew(0.4*img.quantum_range)
        img.save(filename='deskewed/'+ images)"""

with Image("image0.jpg") as img:
    img.deskew(0.4*img.quantum_range)
    img.save(filename='deskewed.jpg')

