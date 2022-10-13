# quick face extractor v1.0
# script to extract multiple faces from pictures with opencv
# recomended to extract manny faces from multiple files because it work fast.
# add extra espace on all face sides (if enabled)

import os
import cv2

class extractor:
    
    def __init__(self, output="output-faces"):
        self.extra_space = False
        self.output = output

    def extract(self, images=['image.jpg']):
        
        """
images : list of image path
    it will extract all the faces from the image
    in a folder and will retun the amount of faces extracted
"""

        try:
            os.mkdir(self.output)
        except:
            None

        count=0
        for image in images:
            
            # Read the input image 
            image = cv2.imread(image)
            # Convert into grayscale 
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            # Load the cascade classifier, it come included in opencv
            faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
            # Detect faces
            faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.3,
                minNeighbors=3,
                minSize=(30, 30)
            )

            print("[INFO] Found {0} Faces.".format(len(faces)))

            
            for (x, y, w, h) in faces:
                # Draw rectangle around the current face
                #cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                
                if not self.extra_space:
                    # next line get the original small face area detected by opencv
                    roi_color = image[y:y + h, x:x + w]
                else:
                    # --------- next code get face with extra space on the sides ------------
                    # get image size
                    height, width , channels = image.shape
                    # variable to add extra space to all the sides of the face so dont get cut to small
                    top = y - ( h // 3 )
                    down = y + h + ( h // 3 )
                    left = x - ( w // 4 )
                    right = x + w + ( w // 4 )
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
                    roi_color = image[top: down, left: right]
                    # --------------------------------------------
                
                # make a name for the image
                filename = f'{self.output}/Face'+str(count)+'.jpg'
                # save the image to file
                cv2.imwrite(filename, roi_color)
                count+=1
        return count



if __name__ == "__main__":
    e = extractor()
    print(e.extract(image=['image.jpg']))



