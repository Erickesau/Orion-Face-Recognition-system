# class to list all profiles v1.0.9 code by erick esau martinez

import os
import PIL
import json
import random
from PIL import Image, ImageTk
from tkinter import Button, Tk, Frame, Label, PhotoImage

class widget:
    def __init__(self):
        self.index = 0
        self.wanted = []
        self.path = []

    def list_profiles(self, filter_values=False):
        """
this method list all the profiles you can send a dictionary to filter values
example list_profiles(filter_values={'name':'erick', 'country':'sv', 'gender':'m'})
the keys must be available in the data_base/profile.json  file.
"""
        # set vars to default
        self.index = 0
        self.wanted = []
        self.path = []
        # list all profiles path
        self.list = os.walk(top="data_base")
        # get files only
        for a,folders,files in self.list:
            for folder in folders:
                try:
                    # read profile json file
                    if os.path.isfile(f"./data_base/{folder}/profile.json"):
                        with open(f"./data_base/{folder}/profile.json", "r") as f:
                            profile = json.load(f)

                        # filter by values this code is executed if filter_values contain something.
                        # you can change  "not in" by "!=" the diference is
                        # "not in" will search the value in the profile info, "!=" will compare if the value absolut math.
                        if filter_values:
                            mach = True
                            for key in filter_values.keys():
                                if filter_values[key] != "":
                                    if filter_values[key].lower() not in str(profile[key]).lower():
                                        mach = False
                                        break
                            if not mach:
                                # if current profile values not math continue with next profile
                                continue

                        # append the the picture path to list
                        if profile["alert"]:
                            self.wanted.append(True)
                        else:
                            self.wanted.append(False)
                        self.path.append(f"data_base/{folder}")
                        
                except:
                    print(f"error./data_base/{folder}/profile.json")
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
        self.tab = Frame(parent, bg="black", relief="ridge", borderwidth=5)
        

        row=0
        col=0
        for a in range(len(self.path[self.index:])):

            # create a button to show the picture.
            if self.wanted[a]:
                color = "red"
            else:
                color = "black"
            boton = Button(self.tab, bd=1, bg=color)
            boton.grid(row=row,column=col)
            # configure the current profile picture to show in tkinter button.
            # add button command to call function to show the current profile info linked to ths button
            # the funcion will receive the profile path and wanted_aler=false so not play alert when we click
            # the button if the person is wanted.
            boton.im = PhotoImage(file='./'+self.path[self.index + a] + "/thumbnail card.png")
            boton.configure(image=boton.im, command=lambda x=a: fun(self.path[self.index + x], wanted_alert=False))

            
            
            col+=1
            # if there is already 4 column pass to next line
            if col==4:
                    col=0
                    row+=1
            # if there is already 4 lines break
            if row == 3:
                    break
        return self.tab

    def next_page(self, fun, parent=""):
        """
if the profiles list of too big use this method to show next page.
"""
        # show next 12 profiles in an new frame.
        if not (self.index+12) >= len(self.path):
            self.index +=12
            return self.get_profiles(fun, parent)
        else:
            return self.get_profiles(fun, parent)
        
    def previous_page(self,fun, parent=""):
        """
if the profiles list of too big use this method to show previous page.
"""
        # show previus 12 profiles in an new frame.
        if not self.index == 0:
            self.index -=12
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

                
