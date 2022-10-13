# face crop v1.0 hight accuracy but slow.
# script to extract profile face from pictures with pillow and face recognition
# face recognition detect face location is slower than opencv but never mistake.
# recomended to extract one face.
# add extra espace on all face sides (if enabled)

import os
import face_recognition
from PIL import Image

class Crop:
    
    def __init__(self):
        self.extra_space = True


    def crop(self, image='image.jpg'):
        
        """
image : image path
    it will crop the first face detected at index 0
    and save to file
"""

        # read image with face recgonition
        im = face_recognition.load_image_file(image)
        # detect faces location with face recognition and save coordinates
        faces_location = face_recognition.face_locations(im)

        # read image with pil
        img = Image.open(image)
        # use the first image 0
        for y, w, h, x in [faces_location[0]]:
            if not self.extra_space:
                # next line get the original small face area detected by opencv
                # extact face with opencv using the coordinates
                img = img.crop((x,y,w,h))
            else:
                # --------- next code get face with extra space on the sides ------------
                # get image size
                width, height = img.size

                # variable to add extra space to all the sides of the face so dont get cut to small
                top = y - (h - y) // 2.5
                down = h + (h - y) // 2.5
                left = x - (w - x) // 3
                right = w + (w - x) // 3
                # make sure the extra area is not bigger than image size
                if top < 0:
                    top = 0
                if left < 0:
                    left = 0

                if down > height:
                    down = height
                if right > width:
                    right = width
                
                # get the current face with extra espace on the sides
                img = img.crop((left,top,right,down))
                # --------------------------------------------

        try:
            os.mkdir("output-faces")
        except:
            None
        # save the image to file
        img.save("./output-faces/temp_image01.png")
        # return image path
        return "./output-faces/temp_image01.png"



if __name__ == "__main__":
    e = Crop()
    print(e.crop(image='img.jpg'))



