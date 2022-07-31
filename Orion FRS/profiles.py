# class to list all profiles v1.0.6 code by erick esau martinez

import os
import PIL
import json
import random
from PIL import Image, ImageTk
from tkinter import Button, Tk, Frame, Label

class widget:
    def __init__(self):
        self.index = 0
        self.data = []
        self.path = []

    def list_profiles(self, filter_values=False):
        """
this method list all the profiles you can send a dictionary to filter values
example list_profiles(filter_values={'name':'erick', 'country':'sv', 'gender':'m'})
the keys must be available in the data_base/profile.json  file.
"""
        # set vars to default
        self.index = 0
        self.data = []
        self.path = []
        # list all profiles path
        self.list = os.walk(top="data_base")
        # get files only
        for a,b,c in self.list:
            for file in c:
                try:
                    # read profile json file
                    if file[-5:] == ".json":
                        a = (a.replace("\\","/"))
                        with open(a+"/"+file, "r") as f:
                            i = json.load(f)

                        # filter by values this code is executed if filter_values contain something.
                        # you can change  "not in" by "!=" the diference is
                        # "not in" will search the value in the profile info, "!=" will compare if the value absolut math.
                        if filter_values:
                            mach = True
                            for key in filter_values.keys():
                                if filter_values[key] != "":
                                    if filter_values[key].lower() not in str(i[key]).lower():
                                        mach = False
                                        break
                            if not mach:
                                # if current profile values not math continue with next profile
                                continue

                        
                        # extract some of the profile info from json file and save to 'info var'
                        info = ""
                        if i["wanted"][0] or i["wanted"][1]: info += "!!! Wanted !!!" + "\n"
                        info += str(i["name"]) + " " + str(i["lname"]) + "\n"
                        info += "DOB: " + str(i["day"]) +"/"+ str(i["month"]) +"/"+ str(i["year"]) + "\n"
                        info += "Loc: " + str(i["country"]) +" / "+ str(i["city"]) + "\n"
                        info += "Id #: " + str(i["id"])+ "\n"
                        info += "Gender:" + str(i["gender"]) + "\n"
                        info += "Job: " + str(i["job"]) + "\n"
                        info += "Adr: " + str(i["address1"]) + "\n"
                        info += "Phone #: " + str(i["phone1"])+ "\n"
                        info += "Mail: " + str(i["mail"])
                        # delete some text if the line is too long to fix in the label
                        for line in info.split("\n"):
                            if len(line) >= 25:
                                info = info.replace(line,line[0:25])
                        # append the profile info var in one list and the picture path into another list
                        # both at the same index
                        self.data.append(info)
                        self.path.append(a)
                        
                except:
                    print("error in "+a+"/"+file)
                    raise


    # receive a funcion to call when a button is pressed, the profile path its will be send to the funcion.
    # and opcionally inherate from parent widget to show the content inside example parent=myframe it will show
    # the content inside of myframe widget
    def get_profiles(self, fun, parent=""):
        """
after you use the list_profiles method use this method to get a frame with all the profiles listed.
you have to specifi a funcion that will be linked to each button so when user click the button the profile path its send to the funtion.
also you can specifi a parent widget so the frame will apear inside of these widget.
"""

        # create a frame to show all the profiles
        try:
            self.tab.destroy()
        except:
            None
        self.tab = Frame(parent, bg="#00bbbb", relief="ridge", borderwidth=5)
        
        profile=Frame()
        boton=Button()
        row=0
        col=0
        for a in range(len(self.data[self.index:])):
            # create a frame to show profile picture and profile info togueter .
            if "!!! Wanted !!!" in self.data[self.index + a]:
                bg = "red"
            else:
                bg = "#0066ff"
            profile.a = Frame(self.tab, bg=bg, relief="ridge", borderwidth=5)
            profile.a.grid(row=row,column=col)
            # create a button to show the picture.
            boton.a = Button(profile.a)
            boton.a.grid(row=0,column=0)
            # create a label to show the info inside of the previus frame togueter with the button.
            Label(profile.a, text=self.data[a+self.index], width=25,justify="left", font=("Arial", 8), bg="light gray").grid(row=0,column=1, sticky="nsew")
            
            # read and resize the picture from the specified index.
            img = Image.open(self.path[self.index + a] + "/"+"image.jpeg")
            img = img.resize((115, 138))
            # make picture compatible with tkinter
            imgtk = ImageTk.PhotoImage(image=img)
            # configure the current profile picture to show in tkinter button.
            # add button command to call function to show the current profile info linked to ths button
            # the funcion will receive the profile path and wanted_aler=false so not play alert when we click
            # the button if the person is wanted.
            boton.a.imgtk = imgtk
            boton.a.configure(image=imgtk, command=lambda x=a: fun(self.path[self.index + x], wanted_alert=False))

            
            
            col+=1
            # if there is already 4 column pass to next line
            if col==4:
                    col=0
                    row+=1
            # if there is already 4 lines break
            if row == 4:
                    break
        return self.tab

    def next_page(self, fun, parent=""):
        """
if the profiles list of too big use this method to show next page.
"""
        # show next 16 profiles in an new frame.
        if not (self.index+16) >= len(self.data):
            self.index +=16
            return self.get_profiles(fun, parent)
        else:
            return self.get_profiles(fun, parent)
        
    def previous_page(self,fun, parent=""):
        """
if the profiles list of too big use this method to show previous page.
"""
        # show previus 16 profiles in an new frame.
        if not self.index == 0:
            self.index -=16
            return self.get_profiles(fun, parent)
        else:
            return self.get_profiles(fun, parent)




if __name__ == "__main__":
    
    
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
            # list_profiles method list all the profiles you can send a dictionary to filter values
            self.page.list_profiles()
            
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

                
