SOURCE CODE 
Orion Face Recognition System
Its a software that provides features for facial recognition using AI (Artificial Inteligency).
if you like please contribute with a small donation.
_______________________________________________

FUNCTION AVAILABLE IN THE LAST RELEASE
--------------------------------------
> Add new person profile to the data base.
> List all person profiles that are in data base.
> Find profiles with the filter feature.
> Edit Delete and update profiles.
> Recognize persons from pictures.
> Recognize persons using the webcam.
> Mark person as wanted to play alarm when its recognized.
> Mark person as wanted to open a custom file  when its recognized.
> Log of previous recognized persons.
> Futuristic design with Visual effects and sound effects.
_________________________________________________

License: MIT
Copyright (c) 2021-2022 Erick Esau Martinez
Programing Language: Python3
Platform: Windows, linux
https://www.paypal.com/paypalme/erickesau0
Email: martinezesau90@gmail.com
Projet blog www.erickesau.wordpress.com
https://github.com/Erickesau
Personal spanish blog Outdated www.erickesau.blogspot.com

Other platform:
macos has not been tested yet but may work, 
if not work is because of the path separator that window use is "\\" but I replaced with "/" to make compatible with other platform that use "/" , on window work too.
_________________________________________________

REQUIREMENTS:
    OpenCV
    pillow
    numpy
    dlib
    Face Recognition
    Playsound version 1.2.2 recomended because newer version show error and need extra dependences


Open your terminal and type:
    pip install opencv-python
    pip install pillow
    pip install numpy
    pip install dlib
    pip install face_recognition
    pip install playsound==1.2.2

face_recognition require dlib it will get automaticli installed before of face_recognition.
Pillow and numpy will get automaticli intstalled too and the rest of dependencies.
_________________________________________________

HOW TO USE:
    Open 'Orion FRS.py' to run the programm.


SETTING:
torelance
    if you are getting wron match it might be that the people in your photo look very similar and a lower
    tolerance value is needed to make face comparisons more strict i recomend set bar to 55
quickscan
    quickscan return the first result found.

    in one file search :
    if quickscan is disabled if a result is found will continue searching the full database and show a list with all result.
    if quickscan enabled will show the first result found.

    in multifile search :
    *if quickscan is disabled if a result is found continue searching the full database for more results 
    and show only the result with lowes tolerance for each face search.
    *if quickscan is enabled return the first result found for each face search.(faster)
DONE.  ENJOY

______________________________________________


You can use face_recognition_system.py module to create your own face recognition projets you can run the module to see some funtions working
see example at the bottom of this document
this programm is powered by face_recognition_system.py that have all the funcion to search and add persons to the data base and search from camera.


the module profiles.py is just to list profiles it will return a frame with all the profiles listed with picture and info.
you can run the module to to see how it work or see example at the bottom of this document.


_________________________________________________
Inspired by science fiction movies:
    Oblivion
    Prometheus
    Matrix
Inspired by:
    Elon Musk
    SpaceX
    Nasa



Tools used:
    Miniconda3-4.3.31-Windows-x86_64 with python 3.6
    Windows 10 64.bit
    Photoshop
    Wavepad audio editor
    Images source: Oblivion, Polaris face recognition.
    Audio source: Oblivion, Youtube.
_________________________________________________


  ------------------------------------------------------------------------------
//CREATE YOUR OWN FACE RECOGNITION PROJETS WITH FACE RECOGNITION SYSTEM.PY MODULE  \\
  ------------------------------------------------------------------------------
  
-------------------- example 1 -------------------------------


import cv2
import time
from Face_Recognition_System import scanner
# create an objets camera=0 is an int number to select the camera that it will be used default is 0
myscan = scanner(camera=0)
# add new image to the data base set the picture path and user info is recomended to use a dictionary with all the info.
myscan.encode_image('path to your picture.jpg', user_info={"key":"value", "key":"value"})
# now load the data it will take 1 or 2 second.
# if the system is encoding some image it will wait until is done to start loading data.
myscan.load_data()

# before you start to recognize, check the progress if already loaded using system_ready() method,
# if data is not loaded will not recognize.
while not myscan.system_ready():
    time.sleep(1)
    
# start the camera and search for persons.
myscan.scan_camera()
while True:
    # it will show the frame from array using opencv
    cv2.imshow('title', myscan.get_frame())
    # myscan.person_found() this method return False if not person is recognized. If a person is recognized will return the folder path where is the numpy array matched
    # in the same folder is the image and user info json file.
    # once you call person_found() method the data is set to false until new person is recognized. so if you call this method 2 times
    # the second time will return false unless a person is recognized again.
    found = myscan.person_found()
    if found:
        # show the path for the encoding that math, you can read the profile info file with json is in the same folder.
        print(found)
        myscan.stop() # stop the process

# you can recognize persons from file too.
result = myscan.scan_file("path to your file.jpg")
print(result)


-------------------- end ----------------------------------


-------------------- example 2 show result on tkinter----------------------------


import cv2
import time
from PIL import ImageTk, Image
from Face_Recognition_System import scanner
from tkinter import Frame,Tk,Label,filedialog,Button


# here we define the root for tkinter mainloop
root = Tk()
#create objet myscan and use the camera at indext 0
myscan = scanner(camera=0)
# open file dialog with tkinter, code must be inside of tkinter mainloop if not you will get some error.
f = filedialog.askopenfile()
# send the image to encode and save the encoded info and sent the user info dict to save in the same folder.
# it will take about 8 seconds
print("encoding image")
a = myscan.encode_image(f.name, user_info={"key":"value", "key":"value"})
if a == 0:
    print("encoded correct")
else:
    print("error encoding")
    
# now load the data it will take 1 or 2 second
myscan.load_data()
# check if data is already loaded
while not myscan.system_ready():
    print("system not ready")
    time.sleep(1)


# now we can pickup an image to recognize it will return the path where is the encode that matched.
f = filedialog.askopenfile()
a = myscan.scan_file(f.name)
# show the path for the encoding that math you ca read the profile info file with json is in the same folder.
print("the user info path is: ", a)
# lets try to recognize from the camera
myscan.scan_camera()
# Create a frame
app = Frame(root, bg="white")
app.grid()
# Create a label inside the frame
lmain = Label(app)
lmain.grid()
# Create a button inside the frame adna funtion to exit
def x():
    myscan.stop()
    root.destroy()
Button(app, text="exit", bg="red", command=x).grid()
# function for video streaming
def video_stream():
    # we can show image in a single line using opencv, next line is disabled.
    #cv2.imshow('title',myscan.get_frame())
    
    # convert array the image BGR to RGBA, blue green red to red green blue.
    cv2image = cv2.cvtColor(myscan.get_frame(), cv2.COLOR_BGR2RGBA)
    # convert the array into image using pillow
    img = Image.fromarray(cv2image)
    # make the image compatible with tkinter using pillow
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    # finally configure the label image
    lmain.configure(image=imgtk)
    # call the funcion every 10 milisecons to update the frame.
    lmain.after(10, video_stream)
video_stream()

root.title("show video in tkinter window")
root.mainloop()

-------------------- end ---------------------------------



  ----------------------------------------------------------------
// LEARN TO LIST PROFILES FROM DATA BASE WITH PROFILES.PY MODULE  \\
  ----------------------------------------------------------------



# it will search the user info in the profile.json with the keys that was created with orion you can edit the profiles.py module and change these keys.
# list of keys that this module will use in the files profile.json created with orion:
# name,lname,day,month,year,country,id,gender,job,address1,phone1,mail, wanted[boolean,boolean,"file path"]
# the wanted key contain a list with 2 boolean and a string, the string is the file path to open if wanted person is detected.


# exmaple the next code will show only elon musk because we send the filter values.
from tkinter import Button,Label,Frame,Tk
from profiles import widget


class root(Tk):
    def __init__(self):
        # when working with class and tk use the super() funcion other wise you will get error maximun recursion.
        super().__init__()
        # create bottons
        self.label = Label(bg="yellow", width=300, height=100)
        self.label.pack()
        b1 = Button(text="close", command=self.close)
        b1.place(x=310,y=0)
        b2 = Button(text="next", command=self.nex)
        b2.place(x=510,y=0)
        b3 = Button(text="prev", command=self.prev)
        b3.place(x=410,y=0)

        self.page = widget()
        # list_profiles method list all the profiles you can send a dictionary to filter values, skip empty values.
        # when you regsiter a new profile with face recognition system and add the profile info using a dictionary these values its the one you can
        # filter here in this emample am searching the keys created with Orion FRS.py.
        self.page.list_profiles(filter_values={"name":"elon", "lname":"musk"})
        
        # get_profiles method will return a frame with all the profiles as buttons.
        # each button is configured to send the profile path to  self.show_person_info funcion.
        # we can specifi a perent exampla: in this case the frame will be inside of self.label 
        self.frame = self.page.get_profiles(self.show_person_info, parent=self.label)
        self.frame.place(x=110,y=20)
        
    def show_person_info(self, person, wanted_alert=False):
        print(person)

    def prev(self):
        self.frame.destroy()
        self.frame = self.page.previous_page(self.show_person_info, parent=self.label)
        self.frame.place(x=110,y=20)

    def nex(self):
        self.frame.destroy()
        self.frame = self.page.next_page(self.show_person_info, parent=self.label)
        self.frame.place(x=110,y=20)
        
    def close(self):
        self.frame.destroy()
    
window = root()
window.geometry("1280x768+10+10")
window.mainloop()





Copyright (c) 2021 Erick Esau Martinez
martinezesau90@gmail.com
https://www.paypal.com/paypalme/erickesau0
