# -*- coding: latin-1 -*-
# Face_Recognition_System v1.5.3 by erick esau martinez
# thanks to Glare y Transductor for tutorial
#I edited the code and created a class with aditional features, am begingner is very dificult for me.

import os
import cv2
import time
import json
import numpy as np
from PIL import Image
import face_recognition
from threading import Thread


        
class scanner:
    """

    args for class scanner:
    camera=0 is an int number to select the camera that it will be used default is 0
    .
    Example of use:
    .
    import cv2
    import time
    from Face_Recognition_System import scanner
    # create an objets
    myscan = scanner(camera=0)
    # add new image to the data base
    myscan.encode_image('path to your picture.jpg', user_info="write user info in dictionary format")
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
        # it will show the frame from array
        cv2.imshow('hi', myscan.get_frame())
        # myscan.person_found() this method return False if not person is recognized. If a person is recognized will return the folder path where is the numpy array matched
        # in the same folder is the image and user info json file.
        # once you call person_found() method the data is set to false until new person is recognized. so if you call this method 2 times
        # the second time will return false unless a person is recognized again.
        found = myscan.person_found()
        if found:
            print(found)
            myscan.stop() # stop the process
    .
    .
    # you can recognize persons from file too.
    result = myscan.scan_file("path to your file.jpg")
    print(result)
    

"""
    def __init__(self, camera=0, tolerance=0.6):
        
        #======================  generate the variables  ================================
        self.camera = camera
        self.encodings_conocidos = []
        self.nombres_conocidos = []
        self.encoding_image = False
        self.loading_data = False
        self.var_tolerance = float(tolerance)
        #definimos 3 variables self.frame contiene los frames self.vdetected la ruta de la imagen que coincidio
        # si self.vstop es true el scanner se cierra,if vstop true quit
        self.vdetected = False
        self.vstop = False
        # cargamos una imagen para que self.frame no este vacia mientras carga la camara y no nos de error
        # al intentar mostrarla con cv2 o procesarlo con pillow en el gui
        #load an image so we can show it if the camera is not ready yet

        try:
            # try to open file, if not exist will get error and execute the except bloc code.
            # because cv2.imread will not give any exception and we get empty image
            with open('media/camera.png',"r") as f:
                None
            self.frame = cv2.imread('media/camera.png')
        except:
            # if image its not available create black blank image
            self.frame = np.zeros(shape=[512, 512, 3], dtype=np.uint8)
        try:
            os.mkdir("./data_base")
        except:
            None






    def encode_image(self, foto, user_info={"name":"test", "lname":"test", "job":"test"}):
        """
encode new image and save to the data base. encode_image(path to your photo.jpg or png, user_info={"key":"value"})
the user info is a dictionary with all the user info example:
user_info={"name":"erick", "lname":"martinez", "job":"test", "country":"usa", "phone":"1234567"}
this process take a lot of cpu maybe the GUI will look a litle slow while encoding you shoul run this method on  a separated Thread.
when its done will return profile path if the image was procesed correct or False if some error ocurred.
"""
        
        self.encoding_image = True
        try:
            
            #Extraer los 'encodings' que caracterizan el rostro, usamos un bloque de try por si no se detectan rostros
            imagen_personal = face_recognition.load_image_file(foto)
            personal_encodings = face_recognition.face_encodings(imagen_personal)[0]
            # create a unique folder name using time, to save the foto and encoding array
            folder_name = time.strftime("%Y%m%d%H%M%S")

            # becarefull we can not create a folder and subfolder at the same time,
            # the data_base folder need to be created before create folder_name, i was getting errors.
            os.mkdir(f"./data_base/{folder_name}/")

            # open image
            img = Image.open(foto)
            
            img.save(f"./data_base/{folder_name}/"+"image.png")
            # save user info with json
            res = json.dumps(user_info)
            with open(f"./data_base/{folder_name}/"+"profile.json", "w") as f:
                f.write(res)
            # save encoding with numpy
            np.save(f"./data_base/{folder_name}/"+"encoding.npy",personal_encodings)
            # append the encodes to the current loaded data so we can start using now
            self.encodings_conocidos.append(personal_encodings)
            self.nombres_conocidos.append("./data_base"+"/"+folder_name)
            # if the process was correct return the profile path
            self.encoding_image = False
            return f"./data_base/{folder_name}"
        except:
            print("some error ocurred the image was not encoded")
            return False
            raise
        finally:
            self.encoding_image = False



        




    def load_data(self):
        """
call this method to load the data, after this you can recognize from camera or files.
after data is loaded you can call the method scan_camera to recognize peoples.
"""
        #==============  load face encoding and folder paths =============
        
        def subprocess():
            self.loading_data = True
            while self.encoding_image:
                time.sleep(1)
            self.encodings_conocidos = []
            self.nombres_conocidos = []
            #cargamos la lista de los encoding
            # get list of encoded images in numpy arrays and load
            w = os.walk(top="data_base")
            for a,b,c in w:
                for file in c:
                    try:
                        if file[-4:] == ".npy":
                            a = (a.replace("\\","/"))
                            # get the encoding one by one and append to the list, note when you save the encoding
                            # make sure you save the pure encoding dont save a list of encoding because when we read the files
                            # here we append the encoding to a list.  if the encoding is already inside a list
                            # entead of use self.encodings_conocidos.append use self.encodings_conocidos = (np.load(a+"/"+file))
                            self.encodings_conocidos.append(np.load(a+"/"+file))
                             # append the current folder path to the other list
                            self.nombres_conocidos.append(a)
                    except:
                        print("error maybe there is not .npy files to load please encode_images firt.")
            if not self.nombres_conocidos:
                print("there is not .npy files to load, please encode_images first, encode_image(path to photo.jpg, user_info='test')")
            self.loading_data = False
        p = Thread(target=subprocess)
        p.start()




    

    def system_ready(self):
        """
return a boolean to lets the user know if the system already have encodes loaded.
if the system is busy encoding images or loading data or there is not data available return False.
if not busy and there is at least one encode available return True
"""
        if not self.loading_data and not self.encoding_image and self.nombres_conocidos:
            return True
        else:
            return False






    
    def scan_camera(self,camera=0):
        """
open the camera and search for faces and recognize. you can use argument camera=0 to use the especified camera.
by default it will use camera=0
after you start the camera you can get info with the next methods.
use get_frame method to get one frame from the camera, it will return the frame
use person_found method to check if the person in the front of camera is recognized,it will be false if not recognised.
use stop method to stop the camera recognicion.
"""
        if not self.encodings_conocidos and not self.nombres_conocidos:
            print("there is not data loaded, use load_data method to load the data")
        # iniciamos la funcion _scan_ en un proceso paralelo ya que se crea un bucle while y pausaria nuestro codigo
        self.camera = camera
        self.vstop = False
        self.vdetected = False
        process = Thread(target=self._scan_)
        process.start()

    
    def get_frame(self):
        """
return current frame from the camera in an numpy array
"""
        return self.frame

    
    
    def person_found(self):
        """
this method return the path of the picture that matched with the last person recognized from the camera.
once you call this method the value is set to False until new person is recognized.
.
if the last person in the front of camera was not recognized return False. 
"""
        # return the path to the person info and clear the data.
        person = (self.vdetected)
        self.vdetected = False
        return person


    
    def stop(self):
        """
stop the recognizer and release camera
"""
        self.vstop = True
        self.vdetected = False


    def tolerance(self, tolerance):
        """
tolerance float lower number make the recognition more strict.
"""
        self.var_tolerance = float(tolerance)



    def scan_file(self, file, quickscan=True):
        """
open a photo and recognize faces, and return the path of picture that matched from data base.
this is very easy just send the image path scan_file("path_to_image.jpg") it will return the
folder path that contain the numpy array that matched.
quickscan: if set to True will return a string with the first match path (default),
if set to False will return all result that match it will be a tuple with 2 list ([names], [distances])
names list contain the profiles paths that match while distances contain the similarity distances.
"""
        if not self.encodings_conocidos and not self.nombres_conocidos:
            print("there is not data loaded, use load_data method to load the data")
            
        loaded_file = face_recognition.load_image_file(file)
        try:
            encoding = face_recognition.face_encodings(loaded_file)[0]
        except:
            print(
                "[INFO] no faces detected in: ",file,)
            return None
        
        if quickscan:
            
            # find if there is some similarity that match any know enoding
            coincidencias = face_recognition.compare_faces(self.encodings_conocidos, encoding, tolerance=self.var_tolerance)        
            #El array 'coincidencias' es ahora un array de booleanos. Si contiene algun 'True', es que ha habido alguna coincidencia:
            if True in coincidencias:
                # return profile name
                return self.nombres_conocidos[coincidencias.index(True)]
            else:
                return False
    
        else:
            
            # search the full data base and compare the match distance of faces
            all_distances = face_recognition.face_distance(self.encodings_conocidos, encoding)
            # make a list because is a numpy array
            all_distances = list(all_distances)
            names = []
            distances = []
            index = 0
            for d in all_distances:
                # take faces only if distance is lower than tolerance
                if d <= self.var_tolerance:
                    # get name from the list of names
                    name = self.nombres_conocidos[index]
                    names.append(name)
                    distances.append(d)
                index += 1
            # if a result found return a list of names and a list of distances.
            if names:       
                return names, distances
            else:
                return False
            
                
            




    def _scan_(self):
        """
    Código 2.2 - Reconocimiento facial con webcam
    Este código identifica nuestro rostro en un vídeo capturado con una webcam.
 
    Escrito por Glare y Transductor
    programacion adicional por erick esau
    www.robologs.net 
"""
        

         
        #Iniciar la webcam:
        webcam = cv2.VideoCapture(self.camera)
        # NOTA: Si no funciona puedes cambiar el índice '0' por otro, o cambiarlo por la dirección de tu webcam.
         
         
        #Cargar una fuente de texto:
        font = cv2.FONT_HERSHEY_COMPLEX 
         
         
        # Identificar rostros es un proceso costoso. Para poder hacerlo en tiempo real sin que haya retardo
        # vamos a reducir el tamaño de la imagen de la webcam. Esta variable 'reduccion' indica cuanto se va a reducir:
        reduccion = 5 #Con un 5, la imagen se reducirá a 1/5 del tamaño original



        
        while 1:
            #Definimos algunos arrays y variables:
            loc_rostros = [] #Localizacion de los rostros en la imagen
            encodings_rostros = [] #Encodings de los rostros
            nombres_rostros = [] #Nombre de la persona de cada rostro
            nombre = "" #Variable para almacenar el nombre
         
            #Capturamos una imagen con la webcam:
            valido, img = webcam.read()
         
            #Si la imagen es válida (es decir, si se ha capturado correctamente), continuamos:
            if valido:
         
                #La imagen está en el espacio de color BGR, habitual de OpenCV. Hay que convertirla a RGB:
                img_rgb = img[:, :, ::-1] 
         
                #Reducimos el tamaño de la imagen para que sea más rápida de procesar:
                img_rgb = cv2.resize(img_rgb, (0, 0), fx=1.0/reduccion, fy=1.0/reduccion)
         
                #Localizamos cada rostro de la imagen y extraemos sus encodings:
                loc_rostros = face_recognition.face_locations(img_rgb)
                encodings_rostros = face_recognition.face_encodings(img_rgb, loc_rostros)
         
                #Recorremos el array de encodings que hemos encontrado:
                for encoding in encodings_rostros:
         
                    #Buscamos si hay alguna coincidencia con algún encoding conocido:
                    coincidencias = face_recognition.compare_faces(self.encodings_conocidos, encoding, tolerance=self.var_tolerance)
         
                    #El array 'coincidencias' es ahora un array de booleanos. Si contiene algun 'True', es que ha habido alguna coincidencia:
                    if True in coincidencias:
                        nombre = self.nombres_conocidos[coincidencias.index(True)]
                        self.vdetected = nombre

         
                    #Si no hay ningún 'True' en el array 'coincidencias', no se ha podido identificar el rostro:
                    else:
                        nombre = "???"
                        self.vdetected = False
         
                    #Añadir el nombre de la persona identificada en el array de nombres:
                    nombres_rostros.append(nombre)
         
                #Dibujamos un recuadro rojo alrededor de los rostros desconocidos, y uno verde alrededor de los conocidos:
                for (top, right, bottom, left), nombre in zip(loc_rostros, nombres_rostros):
                     
                    #Deshacemos la reducción de tamaño para tener las coordenadas de la imagen original:
                    top = top*reduccion
                    right = right*reduccion
                    bottom = bottom*reduccion
                    left = left*reduccion
         
                    #Cambiar de color según si se ha identificado el rostro:
                    if nombre != "???":
                        color = (0,255,0)
                    else:
                        color = (0,0,255)
         
                    #Dibujar un rectángulo alrededor de cada rostro identificado, y escribir el nombre:
                    cv2.rectangle(img, (left, top), (right, bottom), color, 2)
                    cv2.rectangle(img, (left, bottom - 20), (right, bottom), color, -1)
                    cv2.putText(img, nombre, (left, bottom - 6), font, 0.6, (0,0,0), 1)
         
                #Mostrar el resultado en una ventana:
                #cv2.imshow('Output', img)
                # editado en ves de mostarlo la variable self.frame toma el resultado 
                self.frame = img
                


            #Salir con 'ESC' o si la variable completado es true
            k = cv2.waitKey(5) & 0xFF
            if k == 27 or self.vstop == True:
                cv2.destroyAllWindows()
                break
                
        webcam.release()








#-------------------------------------test example--------------------
if __name__ == "__main__":
    import time
    from tkinter import Frame,Tk,Label,filedialog,Button
    from PIL import ImageTk, Image
    import cv2

    # here we define the root for tkinter mainloop
    root = Tk()
    #create objet myscan and use the camera at indext 0
    myscan = scanner(camera=0)
    """ # i comment this part because if we encode a image it will save to the data base and user info will not be complete.
    # open file dialog with tkinter, code must be inside the tkinter mainloop or will get some error.
    f = filedialog.askopenfile()
    # send the image to encode and save the encoded info and sent the user info to save in the same folder.
    # it will take about 8 seconds
    print("encoding image")
    a = myscan.encode_image(f.name, user_info="write user info list dic or text")
    if a == 0:
        print("encoded correct")
    else:
        print("error encoding")
        """
    # now load the data it will take 1 or 2 second
    myscan.load_data()
    # check if data is already loaded
    while not myscan.system_ready():
        print("system not ready")
        time.sleep(1)


    # pickup an image to recognize it will return the path where is the encode that matched.
    f = filedialog.askopenfile()
    a = myscan.scan_file(f.name)
    print("the user info path is: ", a)
    print("if returned False is because the user is not in the data base")
    # lets try to recognize from the camera
    myscan.scan_camera()
    # Create a frame
    app = Frame(root, bg="white")
    app.grid()
    # Create a label inside the frame
    lmain = Label(app)
    lmain.grid()
    # Create a button inside the frame and a funtion to exit
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
        # convert the array into image
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






