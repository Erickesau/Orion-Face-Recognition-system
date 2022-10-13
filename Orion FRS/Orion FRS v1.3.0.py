# Orion Face Recognition System.   GUI v1.3.0  
# Copyright 2022 erick esau martinez
# martinezesau90@gmail.com
# www.erickesau.wordpress.com
# https://github.com/Erickesau
# https://www.paypal.com/paypalme/erickesau0

import os
import re
import cv2
import time
import json
import PIL
import webbrowser
from PIL import Image,ImageTk
from profiles import widget
from threading import Thread
from playsound import playsound
from Face_Recognition_System import scanner
from tkinter import Label,Frame,Entry,INSERT,Canvas,Scrollbar,Checkbutton,Spinbox,Button,PhotoImage,Tk,filedialog,Toplevel,ttk,scrolledtext,BooleanVar,IntVar,Listbox,StringVar,DoubleVar,Scale
from quick_face_extractor import extractor

ex = extractor()
myscan = scanner()
myscan.load_data()




class Root(Tk):
    def __init__(self):
        super().__init__()
        
        ### define some vars, load setting from json file if exist 
        try:
            with open("setting.json", "r") as f:
                sett = json.load(f)
            self.setting_sound = sett["sound"]
            self.setting_auto_off_camera = sett["auto_off_camera"]
            self.setting_video_source = sett["video_source"]
            self.show_camera_hud = sett["show_camera_hud"]
            self.quickscan = sett["quickscan"]
            self.tolerance = float(sett["tolerance"])
        except:
            self.setting_sound = True
            self.setting_auto_off_camera = True
            self.setting_video_source = 0
            self.show_camera_hud = True
            self.quickscan=True
            self.tolerance=0.55
            
        # define other vars
        self.new_picture_path = ""
        self.alarm_file_path = ""
        self.last_person_detected = ""
        self.delete_previus_profile = False
        self.stop_alarm = False
        self.profile_list = Frame()
        self.log_var = StringVar()
        myscan.tolerance(self.tolerance)



        
        ### load images for widgets
        self.bg_img = PhotoImage(file='media/hud_.png')
        self.img1 = PhotoImage(file='media/img1.png')
        self.img2 = PhotoImage(file='media/img2.png')
        self.camera_img = PhotoImage(file='media/opencamera.PNG')
        self.camera_img2 = PhotoImage(file='media/opencamera2.PNG')
        self.file_img = PhotoImage(file='media/openfile.png')
        self.file_img2 = PhotoImage(file='media/openfile2.png')
        self.add_img = PhotoImage(file='media/add.png')
        self.add_img2 = PhotoImage(file='media/add2.png')
        self.clear_img = PhotoImage(file='media/clear.png')
        self.clear_img2 = PhotoImage(file='media/clear2.png')
        self.close_img =  PhotoImage(file='media/close.png')
        self.close_img2 =  PhotoImage(file='media/close2.png')
        self.multifile_img = PhotoImage(file='media/multifile.png')
        self.multifile_img2 = PhotoImage(file='media/multifile2.png')
        
        
        
        
        ### ------------  create 3 tabs frames  -------------------------
        self.list_frame = Frame(width=1260, height=720, bg="#00ffff", relief="ridge", borderwidth=10)
        self.search_frame = Frame(width=1260, height=720, bg="#00ffff", relief="ridge", borderwidth=10)
        self.add_frame = Frame(width=1260, height=720, bg="#00ffff", relief="ridge", borderwidth=10)
        self.add_frame.place(x=0, y=27)
        
        ### -------------  background labels --------------------------
        Label(self.list_frame, image=self.bg_img, width=1260, height=680).grid(column=0, row=0)
        Label(self.search_frame, image=self.bg_img, width=1260, height=680).grid(column=0, row=0)
        Label(self.add_frame, image=self.bg_img, width=1260, height=680).grid(column=0, row=0)



        ### ======================  TOP BAR BUTTONS  =========================
        self.bar_menu = Frame(bg="black", width=1280,height=35, relief="raised",borderwidth=5)
        self.bar_menu.place(x=0, y=-2)

        b1 = Button(self.bar_menu, text="LIST FACES", command=self.list_faces, bg="#005588", fg="white",font=("Verdana",11), activebackground="#00ccff")
        b2 = Button(self.bar_menu, text="SEARCH FOR FACES", command=self.search, bg="#005588" ,fg="white", font=("Verdana",11), activebackground="#00ccff")
        b3 = Button(self.bar_menu, text="ADD FACES", command=self.add, bg="#005588",fg="white",font=("Verdana",11), activebackground="#00ccff")
        b4 = Button(self.bar_menu, text="SETTINGS", command=self.settings, bg="#005588", fg="white",font=("Verdana",11), activebackground="#00ccff")
        b5 = Button(self.bar_menu, text="About", command=self.about, bg="#005588", fg="white",font=("Verdana",11), activebackground="#00ccff")
        b1.place(x = 20, y = 0)
        b2.place(x = 140, y = 0)
        b3.place(x = 330, y = 0)
        b4.place(x = 580, y = 0)
        b5.place(x = 680, y = 0)
        # visual effects for bar buttons
        b1.bind("<Enter>", lambda x: b1.configure(bg="#008888"))
        b1.bind("<Leave>", lambda x: b1.configure(bg="#005588"))
        b2.bind("<Enter>", lambda x: b2.configure(bg="#008888"))
        b2.bind("<Leave>", lambda x: b2.configure(bg="#005588"))
        b3.bind("<Enter>", lambda x: b3.configure(bg="#008888"))
        b3.bind("<Leave>", lambda x: b3.configure(bg="#005588"))
        b4.bind("<Enter>", lambda x: b4.configure(bg="#008888"))
        b4.bind("<Leave>", lambda x: b4.configure(bg="#005588"))
        b5.bind("<Enter>", lambda x: b5.configure(bg="#008888"))
        b5.bind("<Leave>", lambda x: b5.configure(bg="#005588"))
           
        

        
        ### =================   SCREEN LIST FACES BUTTON  ============================

        Button(self.list_frame, text="List All",command=self.list_all, bg="#005588", fg="yellow", font="verdana 12", width=8, activebackground="#00aaff").place(x=480,y=0)
        Button(self.list_frame, text="Filter",command=self.filter_profiles, bg="#005588", fg="yellow", font="verdana 12", width=8, activebackground="#00aaff").place(x=570,y=0)
        Button(self.list_frame, text="Previous",command=self.func_prev_page, bg="#005588", fg="yellow", font="verdana 12", width=8, activebackground="#00aaff").place(x=680,y=0)
        Button(self.list_frame, text="Next",command=self.func_next_page, bg="#005588", fg="yellow", font="verdana 12", width=8, activebackground="#00aaff").place(x=770,y=0)
        Button(self.list_frame, text="Close", command=self.close_profile_list, bg="#005588", fg="yellow", font="verdana 12",  width=8, activebackground="orange").place(x=880,y=0)
        



        
        ### ================== SCREEN SEARCH FOR FACES BUTTONS ==================

        #buttton scan camera
        self.bt_open_camera = Button(self.search_frame, image=(self.camera_img), command=self.camera, borderwidth=0,bg="#002222",activebackground="#002222")
        self.bt_open_camera.place(x=98, y=227)
        #button scan file
        self.bt_open_file = Button(self.search_frame, image=self.file_img,command=self.file, borderwidth=0,bg="#002222", activebackground="#002222")
        self.bt_open_file.place(x=360, y=200)
        # button scan muti files
        self.bt_multifiles = Button(self.search_frame, image=self.multifile_img, command=self.multi_files , bd=0,bg="#002222", activebackground="#002222")
        self.bt_multifiles.place(x=360, y=380)
        #button close hided
        self.bt_close = Button(self.search_frame, image=self.close_img,command=self.close,bg="#002222", activebackground="#002222",borderwidth=0)
        #button clear
        self.bt_clear = Button(self.search_frame,image=self.clear_img, command=self.clear,bg="#002222",borderwidth=0, activebackground="#002222")
        self.bt_clear.place(x=595, y=560)
        # create 2 frame with colored border.
        self.info_frame1 = Frame(self.search_frame, bg='#007777', relief="ridge", borderwidth=18)
        self.info_frame1.place(x=750,y=15)
        self.info_frame2 = Frame(self.search_frame, bg='#007777', relief="ridge", borderwidth=18)
        self.info_frame2.place(x=750,y=340)
        # create 2 label to show the recognized person info and image inside of the 2 previous frame.
        self.info = Label(self.info_frame1, text="NO IMAGE\n AVAILABLE", font="arial 20", width=26, height=9,bg='#000011', fg="#00ffff")
        self.info.pack()
        self.info2 = Label(self.info_frame2, text="NO INFO\n AVAILABLE", font="arial 20", wraplength=400, width=26,height=9, bg='#000011', fg="#00ff00")
        self.info2.pack()
        # label to show video
        self.lvideo = Label(self.search_frame, relief="ridge", borderwidth=22, bg="#007777")
        # label to show photo
        self.lphoto = Label(self.search_frame, relief="ridge", borderwidth=22, bg="#007777")
        #buttons delete profile and button edit profile
        self.bt_edit_profile = Button(self.search_frame, text=" Edit profile ", bg="#00aaff", command=self.edit_profile, activebackground="#00aaff")
        self.bt_delete_profile = Button(self.search_frame, text="Delete profile", bg="#00aaff", command=self.delete_profile, activebackground="red")
        # button and lisbox to show the log of persons recognized in current session.
        log_bt = Button(
            self.search_frame, text="      Log      ",
            command=lambda x=None:(self.log_frame.place(x=83, y=15),self.soundeffect("click")),
            bg="#00aaff",
            activebackground="#00ffff",
            fg="white",
            )
        log_bt.place(x=940,y=330)
        self.log_frame = Frame(self.search_frame, bg='#007777', relief="ridge", borderwidth=18)
        self.log_list = Listbox(self.log_frame, listvariable=self.log_var, width=70, height=10, bg="#000000",fg="#00ff00")
        self.log_list.pack()

        #------- create a scrollable widget -------
        def myfunction(event):
            canvas.configure(scrollregion=canvas.bbox("all"), width = 675, height = 600)
            
        self.multi_result_container = Frame(self.search_frame, relief="groove", width=50, height=100, bd=5, bg="#00ffff")
        #self.multi_result_container.place(x=20,y=20)
        
        canvas = Canvas(self.multi_result_container, width=675, height=600, bg="#000000")
        self.multi_result = Frame(canvas, bg="gray")
        scroll = Scrollbar(self.multi_result_container, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right",fill="y")
        canvas.pack(side="left")
        canvas.create_window((0,0), window=self.multi_result, anchor='nw')
        self.multi_result.bind("<Configure>",myfunction)
        # ----------------------------------------
        # create a button and funtion to hide or show scrollable widget 
        def f():
            if self.multi_result_container.winfo_ismapped():
                self.multi_result_container.place_forget()
            else:
                self.multi_result_container.place(x=20,y=20)
        self.bt_allresult = Button(self.search_frame, text="<", command=f, height=42, bg="#00aaff", activebackground="#00aaff")
        


        

        # ------- visual effect for buttons ---------
        self.bt_edit_profile.bind("<Enter>", lambda x: self.bt_edit_profile.configure(bg="#00ffff"))
        self.bt_edit_profile.bind("<Leave>", lambda x: self.bt_edit_profile.configure(bg="#00aaff"))
        self.bt_delete_profile.bind("<Enter>", lambda x: self.bt_delete_profile.configure(bg="#00ffff"))
        self.bt_delete_profile.bind("<Leave>", lambda x: self.bt_delete_profile.configure(bg="#00aaff"))
        log_bt.bind("<Enter>", lambda x: log_bt.configure(bg="#00ffff"))
        log_bt.bind("<Leave>", lambda x: log_bt.configure(bg="#00aaff"))
        self.bt_allresult.bind("<Enter>", lambda x: self.bt_allresult.configure(bg="#00ffff"))
        self.bt_allresult.bind("<Leave>", lambda x: self.bt_allresult.configure(bg="#00aaff"))
        

        #-------bind--------- to change button image when mouse is over.
        self.bt_open_camera.bind("<Enter>", lambda event: self.bind_button(event, self.bt_open_camera, self.camera_img2))
        self.bt_open_camera.bind("<Leave>", lambda event: self.bind_button(event, self.bt_open_camera, self.camera_img))
        self.bt_open_file.bind("<Enter>", lambda event: self.bind_button(event, self.bt_open_file, self.file_img2))
        self.bt_open_file.bind("<Leave>", lambda event: self.bind_button(event, self.bt_open_file, self.file_img))
        self.bt_multifiles.bind("<Enter>", lambda event: self.bind_button(event, self.bt_multifiles, self.multifile_img2))
        self.bt_multifiles.bind("<Leave>", lambda event: self.bind_button(event, self.bt_multifiles, self.multifile_img))
        self.bt_clear.bind("<Enter>", lambda event: self.bind_button(event, self.bt_clear, self.clear_img2))
        self.bt_clear.bind("<Leave>", lambda event: self.bind_button(event, self.bt_clear, self.clear_img))
        self.bt_close.bind("<Enter>", lambda event: self.bind_button(event, self.bt_close, self.close_img2))
        self.bt_close.bind("<Leave>", lambda event: self.bind_button(event, self.bt_close, self.close_img))
        # hide listbox when leave and show person info when clic
        self.log_frame.bind("<Leave>",lambda x=None: (window.focus(), self.log_frame.place_forget()))
        self.log_list.bind("<ButtonRelease-1>",self.log_funtion)
        








        # ================= SCREEN ADD FACES BUTTONS ========================

        # place 2 labels to show the titles
        Label(self.add_frame, image=self.img1, borderwidth=0).place(x=118, y=20)
        Label(self.add_frame, image=self.img2, borderwidth=0).place(x=818, y=20)
        
        # 3 buttons add image, add person and clear
        self.bt_addimage = Button(self.add_frame, image=self.file_img, command=self.addimage, bg="#002222", borderwidth=0, activebackground="#002222")
        self.bt_addimage.place(x=50,y=75)
        self.bt_addperson = Button(self.add_frame, image=self.add_img,command=self.addperson,bg="#002222",borderwidth=0, activebackground="#002222")
        self.bt_addperson.place(x=595,y=500)
        self.bt_clear_entry = Button(self.add_frame, image=self.clear_img,command=self.clear_entry,bg="#002222",borderwidth=0, activebackground="#002222")
        self.bt_clear_entry.place(x=595, y=560)

        # mark person as wanted checkbox
        box = Frame(self.add_frame, bg="#00ffff", relief="ridge", borderwidth=3)
        box.place(x=300,y=440)
        Label(box, text="If person detected", bg="#00bbbb", fg="yellow", font="arial 14").grid(sticky="NSEW")
        self.var_alarm = BooleanVar()
        self.var_alarm.set(False)
        self.checkbox_wanted = Checkbutton(box, text="Play alarm", bg="#00bbbb", font="arial 14", var=self.var_alarm, relief="raised", borderwidth=5)
        self.checkbox_wanted.grid(sticky="NSEW")
        self.checkbox_wanted.bind("<Button-1>", lambda x=None:self.soundeffect("click"))
        
        self.var_alarm_file = BooleanVar()
        self.var_alarm_file.set(False)
        self.checkbox_wanted2 = Checkbutton(box, text="Open file ",  bg="#00bbbb",font="arial 14", var=self.var_alarm_file, relief="raised", borderwidth=5, activebackground="#00bbbb")
        self.checkbox_wanted2.grid(sticky="NSEW")
        self.checkbox_wanted2.bind("<Button-1>", self.pickup_alarm_file)
        
        # create all entry in add faces tab
        self.firtname = Entry(self.add_frame, width=20,bg="#009999",fg="yellow", font="black 15",relief="sunken",borderwidth=5)
        self.lastname = Entry(self.add_frame, width=20,bg="#009999",fg="yellow", font="arial 15",relief="sunken",borderwidth=5)
        self.day = Entry(self.add_frame, width=12,bg="#009999",fg="yellow", font="arial 15",relief="sunken",borderwidth=5)
        self.month = Entry(self.add_frame, width=12,bg="#009999",fg="yellow", font="arial 15",relief="sunken",borderwidth=5)
        self.year = Entry(self.add_frame, width=12,bg="#009999",fg="yellow", font="black 15",relief="sunken",borderwidth=5)
        self.country = Entry(self.add_frame, width=19,bg="#009999",fg="yellow", font="arial 15",relief="sunken",borderwidth=5)
        self.city = Entry(self.add_frame, width=19,bg="#009999",fg="yellow", font="arial 15",relief="sunken",borderwidth=5)
        self.gender = Entry(self.add_frame, width=20,bg="#009999",fg="yellow", font="arial 15",relief="sunken",borderwidth=5)
        
        self.job = Entry(self.add_frame, width=20,bg="#009999",fg="yellow", font="arial 15",relief="sunken",borderwidth=5)
        self.idnumber = Entry(self.add_frame, width=20,bg="#009999",fg="yellow", font="arial 15",relief="sunken",borderwidth=5)
        self.address1 = Entry(self.add_frame, width=20,bg="#009999",fg="yellow", font="arial 15",relief="sunken",borderwidth=5)
        self.address2 = Entry(self.add_frame, width=20,bg="#009999",fg="yellow", font="arial 15",relief="sunken",borderwidth=5)
        self.phone1 = Entry(self.add_frame, width=20,bg="#009999",fg="yellow", font="arial 15",relief="sunken",borderwidth=5)
        self.phone2 = Entry(self.add_frame, width=20,bg="#009999",fg="yellow", font="arial 15",relief="sunken",borderwidth=5)
        self.mail = Entry(self.add_frame, width=20,bg="#009999",fg="yellow", font="arial 15",relief="sunken",borderwidth=5)
        self.comment = scrolledtext.ScrolledText(self.add_frame, width=40,height=9, bg="#007777",fg="white",relief="sunken",borderwidth=5)
        # place entry
        self.firtname.place(x=250,y=100)
        self.lastname.place(x=250,y=170)
        self.day.place(x=40,y=240)
        self.month.place(x=190,y=240)
        self.year.place(x=340,y=240)
        self.country.place(x=40,y=310)
        self.city.place(x=260,y=310)
        self.gender.place(x=40,y=380)
        self.job.place(x=40,y=450)
        self.idnumber.place(x=40,y=520)
        self.address1.place(x=840,y=100)
        self.address2.place(x=840,y=170)
        self.phone1.place(x=840,y=240)
        self.phone2.place(x=840,y=310)
        self.mail.place(x=840,y=380)
        self.comment.place(x=820,y=450)

        # define vars with placeholder text
        self.firtname_plh = "First name"
        self.lastname_plh = "Last name"
        self.day_plh = "Day"
        self.month_plh = "Month"
        self.year_plh = "Year"
        self.country_plh = "Country"
        self.city_plh = "City"
        self.gender_plh = "Gender"
        self.job_plh = "Job"
        self.idnumber_plh = "ID Number"
        self.address1_plh = "Address 1"
        self.address2_plh = "Address 2"
        self.phone1_plh = "Phone Number 1"
        self.phone2_plh = "Phone Number 2"
        self.mail_plh = "Mail"
        self.comment_plh = "Comment"
        
        # add placeholder text to each entry
        self.firtname.insert(0, self.firtname_plh)
        self.lastname.insert(0, self.lastname_plh)
        self.day.insert(0, self.day_plh)
        self.month.insert(0, self.month_plh)
        self.year.insert(0, self.year_plh)
        self.country.insert(0, self.country_plh)
        self.city.insert(0, self.city_plh)
        self.gender.insert(0, self.gender_plh)
        self.job.insert(0, self.job_plh)
        self.idnumber.insert(0, self.idnumber_plh)
        self.address1.insert(0, self.address1_plh)
        self.address2.insert(0, self.address2_plh)
        self.phone1.insert(0, self.phone1_plh)
        self.phone2.insert(0, self.phone2_plh)
        self.mail.insert(0, self.mail_plh)
        self.comment.insert(1.0, self.comment_plh)
        
        # call bind funtion to add and delete placeholder from the entry
        # we send the entry name to work on it, and send current placeholder to compare if the current text
        # on the entry is the placeholder or the user text, and put placeholder on the entry if user leave empty.
        self.firtname.bind("<Enter>", lambda event: self.bind_entry(event, self.firtname, self.firtname_plh))
        self.firtname.bind("<Leave>", lambda event: self.bind_entry(event, self.firtname, self.firtname_plh))
        self.lastname.bind("<Enter>", lambda event: self.bind_entry(event, self.lastname, self.lastname_plh))
        self.lastname.bind("<Leave>", lambda event: self.bind_entry(event, self.lastname, self.lastname_plh))
        self.day.bind("<Enter>", lambda event: self.bind_entry(event, self.day, self.day_plh))
        self.day.bind("<Leave>", lambda event: self.bind_entry(event, self.day, self.day_plh))
        self.month.bind("<Enter>", lambda event: self.bind_entry(event, self.month, self.month_plh))
        self.month.bind("<Leave>", lambda event: self.bind_entry(event, self.month, self.month_plh))
        self.year.bind("<Enter>", lambda event: self.bind_entry(event, self.year, self.year_plh))
        self.year.bind("<Leave>", lambda event: self.bind_entry(event, self.year, self.year_plh))
        self.country.bind("<Enter>", lambda event: self.bind_entry(event, self.country, self.country_plh))
        self.country.bind("<Leave>", lambda event: self.bind_entry(event, self.country, self.country_plh))
        self.city.bind("<Enter>", lambda event: self.bind_entry(event, self.city, self.city_plh))
        self.city.bind("<Leave>", lambda event: self.bind_entry(event, self.city, self.city_plh))
        self.gender.bind("<Enter>", lambda event: self.bind_entry(event, self.gender, self.gender_plh))
        self.gender.bind("<Leave>", lambda event: self.bind_entry(event, self.gender, self.gender_plh))
        self.job.bind("<Enter>", lambda event: self.bind_entry(event, self.job, self.job_plh))
        self.job.bind("<Leave>", lambda event: self.bind_entry(event, self.job, self.job_plh))
        self.idnumber.bind("<Enter>", lambda event: self.bind_entry(event, self.idnumber, self.idnumber_plh))
        self.idnumber.bind("<Leave>", lambda event: self.bind_entry(event, self.idnumber, self.idnumber_plh))
        self.address1.bind("<Enter>", lambda event: self.bind_entry(event, self.address1, self.address1_plh))
        self.address1.bind("<Leave>", lambda event: self.bind_entry(event, self.address1, self.address1_plh))
        self.address2.bind("<Enter>", lambda event: self.bind_entry(event, self.address2, self.address2_plh))
        self.address2.bind("<Leave>", lambda event: self.bind_entry(event, self.address2, self.address2_plh))
        self.phone1.bind("<Enter>", lambda event: self.bind_entry(event, self.phone1, self.phone1_plh))
        self.phone1.bind("<Leave>", lambda event: self.bind_entry(event, self.phone1, self.phone1_plh))
        self.phone2.bind("<Enter>", lambda event: self.bind_entry(event, self.phone2, self.phone2_plh))
        self.phone2.bind("<Leave>", lambda event: self.bind_entry(event, self.phone2, self.phone2_plh))
        self.mail.bind("<Enter>", lambda event: self.bind_entry(event, self.mail, self.mail_plh))
        self.mail.bind("<Leave>", lambda event: self.bind_entry(event, self.mail, self.mail_plh))


        # bind for buttons (change images when mouse is over)
        self.bt_addimage.bind("<Enter>", lambda event: self.bind_button(event, self.bt_addimage, self.file_img2))
        self.bt_addimage.bind("<Leave>", lambda event: self.bind_button(event, self.bt_addimage, self.file_img))
        self.bt_addperson.bind("<Enter>", lambda event: self.bind_button(event, self.bt_addperson, self.add_img2))
        self.bt_addperson.bind("<Leave>", lambda event: self.bind_button(event, self.bt_addperson, self.add_img))
        self.bt_clear_entry.bind("<Enter>", lambda event: self.bind_button(event, self.bt_clear_entry, self.clear_img2))
        self.bt_clear_entry.bind("<Leave>", lambda event: self.bind_button(event, self.bt_clear_entry, self.clear_img))


        # ___________________________________ END OF INIT ___________________________________________





        
    # ============== TOP BAR BUTTONS FUNCIONS ====================

    
    def list_faces(self):
        self.list_frame.place(x=0, y=27)
        self.search_frame.place_forget()
        self.add_frame.place_forget()
        self.soundeffect("robot")

        
    def search(self):
        self.search_frame.place(x=0, y=27)
        self.add_frame.place_forget()
        self.list_frame.place_forget()
        self.soundeffect("robot")


    def add(self):
        self.add_frame.place(x=0, y=27)
        self.search_frame.place_forget()
        self.list_frame.place_forget()
        self.soundeffect("robot")


    def _exit(self):
        myscan.stop()
        self.destroy()


    def settings(self):
        self.dialogo = Toplevel()
        self.dialogo.geometry("300x350+500+200")
        self.dialogo.wm_attributes("-alpha",0.8)
        self.dialogo.overrideredirect(True)
        self.dialogo.configure(bg="#00bb00")
        #self.dialogo.wm_attributes("-transparentcolor", "white")
        f = Frame(self.dialogo,bg="#004444",width=300,height=350,relief="groove",borderwidth=10)
        f.place(x=0,y=0)

        # create vars for checkbox 
        sound = BooleanVar()
        stop = BooleanVar()
        hud = BooleanVar()
        vid = IntVar()
        vid.set(self.setting_video_source)
        quickscan = BooleanVar()
        tolerance = IntVar()

        # set vars content
        sound.set(self.setting_sound)
        stop.set(self.setting_auto_off_camera)
        hud.set(self.show_camera_hud)
        quickscan.set(self.quickscan)
        # scale widget will modifi tolerance but need integer not float
        if float(self.tolerance) <= 0.09:
            tolerance.set(str(self.tolerance)[3::])
        else:
            tolerance.set(str(self.tolerance)[2::])


        # create check box
        Checkbutton(
            f,
            text="Sound Effects",
            var=sound, anchor="nw",
            bg="#00aaff",
            activebackground="orange",
            width=25,
            relief="raised",
            borderwidth=5,
            ).place(x=20,y=10)
        
        Checkbutton(
            f,
            text="Stop Camera if Person Found",
            var=stop,
            anchor="nw",
            bg="#00aaff",
            activebackground="orange",
            width=25,
            relief="raised",
            borderwidth=5,
            ).place(x=20,y=40)
        
        Checkbutton(
            f,
            text="Show Camera Hud",
            var=hud, anchor="nw",
            bg="#00aaff",
            activebackground="orange",
            width=25,
            relief="raised",
            borderwidth=5,
            ).place(x=20,y=70)
        # video source spinbox
        video = Spinbox(f, from_=0, to=8, textvariable=vid, bg="#00aaff", font="Verdana 12",width=3, relief="raised",borderwidth=5)
        video.place(x=20,y=100)
        Label(f, text="Video Source", bg="#00aaff", font="Verdana 10", width=12, relief="ridge",borderwidth=5).place(x=80,y=100)


        t = Frame(f, bg="#00aaff", relief="raised", borderwidth=5,)
        t.place(x=20,y=130)
        Scale(
            t,
            orient="horizontal",
            from_=0,
            to=99,
            showvalue=True,
            variable=tolerance,
            background="#00aaff",
            activebackground="red",
            troughcolor="#00ff00",
            length=195,
            width=10,
            ).pack()
        Label(t, text="Tolerance", bg="#00aaff").pack()
        
        Checkbutton(
            f,
            text="Quick Scan",
            var=quickscan,
            anchor="nw",
            bg="#00aaff",
            activebackground="orange",
            width=25,
            relief="raised",
            borderwidth=5,
            ).place(x=20,y=200)
        

        # -----

                
                
        def save():
            # save setting, start using it.
            self.soundeffect("click")
            self.setting_sound = sound.get()
            self.setting_auto_off_camera = stop.get()
            self.setting_video_source = vid.get()
            self.show_camera_hud = hud.get()
            self.quickscan = quickscan.get()
            # scale widget return tolerance integer but we need float
            # save tolerance in string because float have bug: 0.10 become 0.1
            if tolerance.get() < 10:
                self.tolerance = ("0.0" + str(tolerance.get()))
            else:
                self.tolerance = ("0." + str(tolerance.get()))
                
            # set setting to the face recognitiom system
            myscan.tolerance(self.tolerance)
            # create dictionari and save the setting to json file
            setting = {
                "sound":sound.get(),
                "auto_off_camera":stop.get(),
                "video_source":vid.get(),
                "show_camera_hud":hud.get(),
                "quickscan":self.quickscan,
                "tolerance":self.tolerance,
                }
            setting = json.dumps(setting)
            with open("setting.json", "w") as f:
                f.write(setting)
            self.dialogo.destroy()
            
        Button(f, text="Ok",command=save, bg="orange",relief="raised",borderwidth=5,activebackground="green").place(x=20,y=270)
        Button(f, text="Cancell",command=lambda x=None:(self.dialogo.destroy(),self.soundeffect("click")), bg="orange", relief="raised",borderwidth=5,activebackground="red").place(x=150,y=270)
        self.soundeffect("other")
        self.dialogo.grab_set()
        #self.wait_window(self.dialogo)
        # ---------  END SETTING  ------------





    def about(self):
        self.dialogo = Toplevel()
        self.dialogo.geometry("300x230+500+200")
        self.dialogo.wm_attributes("-alpha",0.8)
        self.dialogo.overrideredirect(True)
        f = Frame(self.dialogo,bg="#004444",width=300,height=230)
        f.pack()
        Label(f, text="ORION",bg="#004444",fg="orange",font="arial 20").place(x=80,y=10)
        Label(f, text="Orion Face Recognition System",bg="#004444",fg="#00ff00").place(x=10,y=40)
        Label(f, text="Version 1.3.0",bg="#004444",fg="#00ff00").place(x=10,y=60)
        Label(f, text="Author: Erick Esau Martinez",bg="#004444",fg="#00ff00").place(x=10,y=80)
        Label(f, text="Mail: martinezesau90@gmail.com",bg="#004444",fg="#00ff00").place(x=10,y=100)
        Button(f, text="Website: https://erickesau.wordpress.com",command=lambda x=None:webbrowser.open("https://erickesau.wordpress.com"),bg="#004444",fg="#00ff00",activebackground="orange").place(x=10,y=120)
        Button(f, text="Github: https://github.com/Erickesau",command=lambda x=None:webbrowser.open("https://github.com/Erickesau"),bg="#004444",fg="#00ff00",activebackground="orange").place(x=10,y=150)
        Button(f, text="Donate with paypal",command=lambda x=None:webbrowser.open("https://www.paypal.com/paypalme/erickesau0"),bg="#004444",fg="#ffff00",activebackground="orange").place(x=10,y=180)
        Button(f, text="Ok",command=lambda x=None:(self.dialogo.destroy(),self.soundeffect("click")), bg="red",activebackground="orange", relief="raised",borderwidth=5).place(x=260,y=0)
        self.soundeffect("other")
        self.dialogo.grab_set()


        
        

    # ===================== SCREEN SEARCH FOR FACES FUNCIONS =============================



    def camera(self):

        # start camera and send the number of the camera to use default camera=0
        myscan.scan_camera(camera=self.setting_video_source)
        # place the Label to show video
        self.lvideo.place(x=83,y=200)
        self.bt_close.place(x=83, y=565)
        
        def show_frame():
            # resize the frame
            frame = cv2.resize(myscan.get_frame(), (420,320))
            
            # add hud water mark to camera output.
            # ______________________________________
            if self.show_camera_hud:
                try:
                    logo = cv2.imread("./media/camera_hud.png") 
                    top_y = 0
                    bottom_y = 320
                    left_x = 0
                    right_x = 420
                    # adding watermark to the image 
                    destination = frame[top_y:bottom_y, left_x:right_x] 
                    result = cv2.addWeighted(destination, 1, logo, 0.5, 0) 
                    frame[top_y:bottom_y, left_x:right_x] = result
                except:
                    print("./media/camera_hud.png not exit")
            # ______________________________________
            
            #La imagen está en el espacio de color BGR, habitual de OpenCV. Hay que convertirla a RGB:
            frame = frame[:, :, ::-1]
            # convert the array to img with pillow configure the label to use the img
            img = PIL.Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            self.lvideo.imgtk = imgtk
            self.lvideo.configure(image=imgtk)
            # if person found call the self.show_person_info funtion to show person info.
            # myscan.person_found() data is automaticly set to false until new person is recognized.
            found = myscan.person_found()
            if found:
                self.show_person_info(found, add_to_log=True)
                # if the setting is set to auto off camera true, it will stop when a person is found.
                if self.setting_auto_off_camera:
                    myscan.stop()
                    self.lvideo.place_forget()
                    self.bt_close.place_forget()
                    return
            self.lvideo.after(50, show_frame)
        show_frame()
        self.soundeffect("camera")
        
        
    def close(self):
        # stop camera and hide the video and photo labels also hide the close button.
        myscan.stop()
        self.lvideo.place_forget()
        self.lphoto.place_forget()
        self.bt_close.place_forget()
        self.soundeffect("other")


    def file(self):
        # -------- open a picture to scan and recofnize faces
        self.soundeffect("alien")
        filename = filedialog.askopenfile(title="Open image to scan",filetypes=("Images *.jpg","Images *.jpeg","Images *.png"))
        if filename:
            #---------------- show image ------------------
            # place the photo label and button to close.
            self.lphoto.place(x=83,y=200)
            self.bt_close.place(x=83, y=565)
            # to show the image the next code read img with opencv and resize because tk PhotoImage not support jpg.
            foto = cv2.imread(filename.name)
            foto = cv2.resize(foto, (420,320))
            #La imagen está en el espacio de color BGR, habitual de OpenCV. Hay que convertirla a RGB:
            foto = foto[:, :, ::-1]
            # convert the array to img with pillow and configure the label to use the img
            foto = PIL.Image.fromarray(foto)
            foto = ImageTk.PhotoImage(image=foto)
            self.lphoto.foto = foto
            self.lphoto.configure(image=foto)
            self.lphoto.update()
            #----------------------------------
            
            #------------------ recognize face --------------
            def recognize():
                #recognize face if fullscan is true it will return a tuple with names and distances lists
                match = myscan.scan_file(
                    filename.name,
                    quickscan=self.quickscan,
                    )
                
                if match:
                    
                    if not self.quickscan:
                        
                        # unpack tuple (names contain the list of profiles that match)
                        names, distance = match
                        # get the index with lowes distance (low tolerance)
                        index = distance.index(min(distance))
                        # get name from that index.
                        person = names[index]
                        self.show_person_info(person, add_to_log=True)
                        return match
                    else:
                        self.show_person_info(match, add_to_log=True)
                        return False
                        
                elif match == None:
                    self.message(text="Error No Faces Found")
                    self.soundeffect("warning")
                    return False
                else:
                    self.message(text="Not Person Found", bg="orange")
                    self.soundeffect("warning")
                    return False
            match = recognize()
            if match:
                                
                names, distances = match
                # ----- load profile images with pillow
                self.loaded_images = []
                for path in names:
                    img = Image.open(path + "./image.png")
                    img = img.resize((100,120))
                    self.loaded_images.append(ImageTk.PhotoImage(image=img))
                    
                # ---- destroy all existing buttons from the list ----
                for child in self.multi_result.winfo_children():
                    child.destroy()

                # ---- add new profiles buttons to the list -----
                index = 0
                col = 0
                row = 0
                for name,dis in zip(names,distances):
                    Button(
                        self.multi_result,
                        image=self.loaded_images[index],
                        command=lambda x=name:self.show_person_info(x, wanted_alert=False),
                        ).grid(column=col, row=row)
                    
                    index += 1
                    col += 1
                    if col==6:
                        row += 1
                        col = 0
                self.multi_result_container.place(x=20,y=20)
                self.bt_allresult.place(x=730,y=20)
                
            #----------------------------------
                



    #----------------------------------
    #select multifiles
    def multi_files(self):
        def run_on_thread():
            files = filedialog.askopenfiles(title="Open multiple images to scan",filetypes=("Images *.jpg","Images *.jpeg","Images *.png"))
            if not files:
                return
            # convert to list
            image_list = list(map(lambda x: x.name, files))

            #----------------------------------
            # input a list of images return a list of profiles that match with the images faces.
            def recognize(file_list):
                # extract faces and save the number of extracted faces
                num = ex.extract(images=file_list)
                # var porcent
                p = 100 / num
                porcent = 0
                self.message(progressbar=True, bg="orange", text="Loading")
                
                result = []
                for n in range(0, num):
                    porcent += p
                    try:
                        self.progressbar['value'] = porcent
                    except:
                        # bar was destroyed
                        return None

                    #recognize faces
                    match = myscan.scan_file(
                        f"./output-faces/Face{n}.jpg",
                        quickscan=self.quickscan,
                        )
                    
                    if match:
                        if not self.quickscan:
                            # unpack tuple, contain the full database names and distances
                            names, distance = match
                            # get the index with lowes distance (with more similarities)
                            index = distance.index(min(distance))
                            # get name from that index.
                            name = names[index]
                            if not name in result:
                                result.append(name)
                        else:
                            # if fullscan is false, match variable contain the profile path
                            if not match in result:
                                result.append(match)
                return result
            #----------------------------------
            
            match = recognize(image_list)
            if match:
                # ----- load images with pillow
                self.loaded_images = []
                for path in match:
                    img = Image.open(path + "./image.png")
                    img = img.resize((100,120))
                    self.loaded_images.append(ImageTk.PhotoImage(image=img))
                    
                # ----- show all profiles that math ------------
                # ---- destroy all existing buttons from the list ----
                for child in self.multi_result.winfo_children():
                    child.destroy()
                # ---- add new profiles buttons to the list -----
                index = 0
                col = 0
                row = 0
                for name in match:
                    Button(
                        self.multi_result,
                        image=self.loaded_images[index],
                        command=lambda x=name:self.show_person_info(x, wanted_alert=False),
                        ).grid(column=col, row=row)
                    
                    index += 1
                    col += 1
                    if col==6:
                        row += 1
                        col = 0
                self.multi_result_container.place(x=20,y=20)
                self.bt_allresult.place(x=730,y=20)
                
                self.msg.destroy()
                
            elif match == None:
                self.msg.destroy()
                
            else:
                self.msg.destroy()
                self.message(text="Not Person Found", bg="orange")
                self.soundeffect("warning")
                
        th = Thread(target=run_on_thread)
        th.start()
        #----------------------------------
             
                
            

    def clear(self):
        # set search faces tab to default text and buttons
        self.info.configure(text="NO IMAGE\n AVAILABLE", image="",font="arial 20",width=26,height=9)
        self.info2.configure(text="NO INFO\n AVAILABLE",font="arial 20",width=26,height=9, justify="center", anchor="center")
        self.last_person_detected = ""
        self.bt_edit_profile.place_forget()
        self.bt_delete_profile.place_forget()
        self.multi_result_container.place_forget()
        self.soundeffect("sucess3")
        self.bt_allresult.place_forget()



    def show_person_info(self, person, wanted_alert=True, add_to_log=False):
        # we need to show the person picture in one label and put the person info in the other label.
        
        # if the current person is already in the label we dont need to show again until the user Clear the info.
        if self.last_person_detected == person:
            return
        
        # swich to search for faces tab when this funcion is executed
        self.search_frame.place(x=0, y=27)
        self.add_frame.place_forget()
        self.list_frame.place_forget()

        # save the current person detected and place the edit, delete button.
        self.last_person_detected = person
        self.bt_edit_profile.place(x=780,y=330)
        self.bt_delete_profile.place(x=1100,y=330)
        try:
            # we need to show the profile picture
            # open the image with pillow
            img = Image.open(person+"/"+"image.png")
            # get image size
            width, height = img.size
            # calculate new size of image but keep aspect
            new_height = 300
            h = (height - new_height)
            w = width/height
            width=int(width-(w*h))
            height=int(height-h)
            # resize image
            img1 = img.resize((width, height))
            # convert image to tkinter image
            imgtk = ImageTk.PhotoImage(image=img1)
            self.info.imgtk = imgtk
            self.info.configure(image=imgtk, width=422, height=290)
        except:
            self.message(text="Error could not read file \n"+person+"\nimage.png  \nmaybe not exist or name is wron", font="arial 12",height=11,fg="yellow")
            self.soundeffect("error")
            raise
            
        try:
            # open profile.txt is in the same folder with the picture and read the info
            with open(person +"/"+ "profile.json", "r") as f:
                i = json.load(f)

                info = ""
                info += "Name: " + str(i["name"]) + " " + str(i["lname"]) + "\n"
                info += "DOB: " + str(i["day"]) +"/"+ str(i["month"]) +"/"+ str(i["year"]) + "\n"
                info += "Location: " + str(i["country"]) +" / "+ str(i["city"]) + "\n"
                info += "Id #: " + str(i["id"]) +" / "+ "Job: " + str(i["job"]) + "\n"
                info += "Gender: " + str(i["gender"]) + "\n"
                info += "Address: " + str(i["address1"]) +"\n       " + str(i["address2"]) + "\n"
                info += "Phone #: " + str(i["phone1"]) +"  /  "+ str(i["phone2"]) + "\n"
                info += "Mail: " + str(i["mail"]) + "\n"

                # delete some text if the line is too long to fix in the label
                for line in info.split("\n"):
                    if len(line) >= 60:
                        info = info.replace(line,line[0:60])
                info += "comment:\n" + i["comment"]
                # now show the info in the label
                self.info2.configure(text=info, font="arial 9",width=60,height=19, justify="left", anchor="nw")
                
                # when a person is recognized add the person to the log listbox
                if add_to_log:
                    t = time.strftime("%m/%d/%y %I:%M %p ")
                    n = str(i["name"]) + " " + str(i["lname"])
                    if i["wanted"][0] or i["wanted"][1]:
                        a = "-->> "
                    else:
                        a = "     "
                    l = [a+n+" "+t+person]
                    for line in (self.log_list.get(0,"end")):
                        l.append(line)
                    self.log_var.set(l)

                
                # if this funtion is called from the list_faces tab, wanted_alert is set to false so will not play alert.
                if wanted_alert == False:
                    return
                self.soundeffect("sucess2")
                # if the person is wanted play alert sound or open file
                # the wanted key contain a list with 3 values the last one is the filepath to open
                if i["wanted"][0]:
                    self.message(text="Wanted person detected")
                    self.soundeffect("alarm")
                if i["wanted"][1]:
                    try:
                        os.startfile(i["wanted"][2])
                    except:
                        self.message(text=("Error file not exist \n"+i["wanted"][2]), font="arial 8", height=16)
                
        except:
            self.info2.configure(text="Error could not read file "+person+"/"+"profile.json \n maybe not exist or name is wron",font="arial 9",width=60,height=19)
            self.message(text="Error could not read file \n"+person+"\nprofile.json \n maybe not exist or name is wron", font="arial 12",height=11,fg="yellow")
            self.soundeffect("error")
            raise




    def delete_profile(self, no_window=False):
        if no_window:
            try:
                # delete all files
                l = os.listdir(self.delete_previus_profile)
                for file in l:
                    try:
                        os.remove(self.delete_previus_profile+'/'+ file)
                    except:
                        None
                # delete empty folder
                os.rmdir(self.delete_previus_profile)
                # delete profile from the log
                lis = []
                self.log_var.set("")
                for line in (self.log_list.get(0,"end")):
                    if self.delete_previus_profile in line:
                        continue
                    lis.append(line)
                    self.log_var.set(lis)
            finally:
                self.delete_previus_profile = False
                myscan.load_data()
                return
            
        self.msg = Toplevel()
        self.msg.geometry("300x200+500+300")
        self.msg.wm_attributes("-alpha",0.6)
        self.msg.overrideredirect(True)
        # show delete profile dialog
        Label(self.msg, text="!!! DELETE PROFILE !!!", font="Arial 20", height=6, bg="orange", fg="red").pack(fill="both")

        def delete():
            self.soundeffect("click")
            self.msg.destroy()
            # remove folder
            
            try:
                # list files
                l = os.listdir(self.last_person_detected)
            except:
                self.message(text=self.last_person_detected +"/\n NOT EXIST",font="arial 12",height="11")
                self.clear()
                self.soundeffect("error")
                return
            # remove all files
            for file in l:
                try:
                    os.remove(self.last_person_detected+'/'+ file)
                except:
                    None
            # remove dir if is empty. not work if there is subfolders
            os.rmdir(self.last_person_detected)
            # delete profile from the log if its in the log.
            lis = []
            self.log_var.set("")
            for line in (self.log_list.get(0,"end")):
                if self.last_person_detected in line:
                    continue
                lis.append(line)
                self.log_var.set(lis)
            # reload data because the current deleted profile not exist.
            self.clear()
            myscan.load_data()
            
            
        def cancell():
            self.soundeffect("click")
            self.msg.destroy()
            
        Button(self.msg, text="DELETE", command=delete, bg="red", fg="white", activebackground="red", font="arial 12").place(x=20,y=160)
        Button(self.msg, text="CANCELL", command=cancell, bg="green", fg="white", activebackground="#00ff00", font="arial 12").place(x=180,y=160)
        self.soundeffect("warning")
        self.msg.grab_set()






    def edit_profile(self):
        ## we need to put the info in the add faces tab entrys, and put placeholder if some entry is empty
        # mark current profile ready to delete and clear search faces tab after done lets go.
        
        ## read the current profile info from file
        try:
            with open(self.last_person_detected +"/"+ "profile.json", "r") as f:
                i = json.load(f)
        except:
            self.message(text=self.last_person_detected +"/\n"+ "profile.json not exits",font="arial 12",height=11)
            self.clear()
            self.soundeffect("error")
            return
        ## clear all entryes in the add faces tab
        self.firtname.delete(0,"end")
        self.lastname.delete(0,"end")
        self.day.delete(0,"end")
        self.month.delete(0,"end")
        self.year.delete(0,"end")
        self.country.delete(0,"end")
        self.city.delete(0,"end")
        self.gender.delete(0,"end")
        self.job.delete(0,"end")
        self.idnumber.delete(0,"end")
        self.address1.delete(0,"end")
        self.address2.delete(0,"end")
        self.phone1.delete(0,"end")
        self.phone2.delete(0,"end")
        self.mail.delete(0,"end")
        self.comment.delete(0.0,"end")
        ## insert the current user info to the add faces tab entryes
        self.firtname.insert(0, i['name'])
        self.lastname.insert(0, i['lname'])
        self.day.insert(0, i['day'])
        self.month.insert(0, i['month'])
        self.year.insert(0, i['year'])
        self.country.insert(0, i['country'])
        self.city.insert(0, i['city'])
        self.gender.insert(0, i['gender'])
        self.job.insert(0, i['job'])
        self.idnumber.insert(0, i['id'])
        self.address1.insert(0, i['address1'])
        self.address2.insert(0, i['address2'])
        self.phone1.insert(0, i['phone1'])
        self.phone2.insert(0, i['phone2'])
        self.mail.insert(0, i['mail'])
        self.comment.insert(0.0, i['comment'])

        self.var_alarm.set(i['wanted'][0])
        self.var_alarm_file.set(i['wanted'][1])
        self.alarm_file_path = i['wanted'][2]
        
        ## the next code configure the new image path, resize and show the image in the button
        self.new_picture_path = self.last_person_detected +"/"+ "image.png"
        # the next code resize the selected image with pillow and show in the button
        img = Image.open(self.new_picture_path)
        img = img.resize((135, 150))
        # make compatible with tkinter
        imgtk = ImageTk.PhotoImage(image=img)
        # configure the image in tkinter button
        self.bt_addimage.imgtk = imgtk
        self.bt_addimage.configure(image=imgtk, relief="ridge", borderwidth=5)

        ## call self.bind_entry funcion to put placeholder on the entry if some is empty.
        # is this case we dont send any event to the funcion so replace event arg with ""
        self.bind_entry("", self.firtname, self.firtname_plh)
        self.bind_entry("", self.lastname, self.lastname_plh)
        self.bind_entry("", self.day, self.day_plh)
        self.bind_entry("", self.month, self.month_plh)
        self.bind_entry("", self.year, self.year_plh)
        self.bind_entry("", self.country, self.country_plh)
        self.bind_entry("", self.city, self.city_plh)
        self.bind_entry("", self.gender, self.gender_plh)
        self.bind_entry("", self.job, self.job_plh)
        self.bind_entry("", self.idnumber, self.idnumber_plh)
        self.bind_entry("", self.address1, self.address1_plh)
        self.bind_entry("", self.address2, self.address2_plh)
        self.bind_entry("", self.phone1, self.phone1_plh)
        self.bind_entry("", self.phone2, self.phone2_plh)
        self.bind_entry("", self.mail, self.mail_plh)

        ## mark current profile ready to delete when the new update is added
        self.delete_previus_profile = str(self.last_person_detected)
        # in the add faces tab change the add button picture
        self.bt_addperson["text"]="UPDATE"
        self.add_img = PhotoImage(file='media/update.png')
        self.add_img2 = PhotoImage(file='media/update2.png')
        self.bt_addperson["image"] = self.add_img
        
        ## finally swich to the add faces tab
        self.add_frame.place(x=0, y=27)
        self.search_frame.place_forget()
        self.list_frame.place_forget()
        self.clear()





    def log_funtion(self, event):
        try:
            x = self.log_list.get(self.log_list.curselection()[0]).split(" ")[-1:][0]
            self.show_person_info(x, wanted_alert=False, add_to_log=False)
            self.soundeffect("click")
        except:
            None
        







    # ============================= SCREEN ADD FACES FUNCIONS ============================


    

    def addimage(self):
        self.soundeffect("alien")
        # we need to pickup an image and save to a var, and show the image in the button.
        n = filedialog.askopenfile(title="Add New Image",filetypes=("Images *.jpg","Images *.jpeg","Images *.png"))
        try:
            self.new_picture_path = (n.name)
            # the next code resize the selected image with pillow and show in the button
            img = Image.open(self.new_picture_path)
            img = img.resize((135, 150))
            # make compatible with tkinter
            imgtk = ImageTk.PhotoImage(image=img)
            # configure the image in tkinter button
            self.bt_addimage.imgtk = imgtk
            self.bt_addimage.configure(image=imgtk, relief="ridge", borderwidth=5)
        except:
            None


    def addperson(self):
        # if no picture added or not name added show message and return
        if self.new_picture_path == "" or self.firtname.get()==self.firtname_plh or self.lastname.get()==self.lastname_plh:
            self.message(text="Image and full\nname required", bg="orange")
            self.soundeffect("warning")
            return
        self.soundeffect("click")
        # get all entry user info and add to the dictionary
        info = {}
        info['name'] = self.firtname.get()
        info['lname'] = self.lastname.get()
        info['day'] = self.day.get()
        info['month'] = self.month.get()
        info['year'] = self.year.get()
        info['country'] = self.country.get()
        info['city'] = self.city.get()
        info['gender'] = self.gender.get()
        info['job'] = self.job.get()
        info['id'] = self.idnumber.get()
        info['address1'] = self.address1.get()
        info['address2'] = self.address2.get()
        info['phone1'] = self.phone1.get()
        info['phone2'] = self.phone2.get()
        info['mail'] = self.mail.get()
        info['comment'] = self.comment.get(1.0,9.0)


        # check if the entry text is the placeholder text to delete from the dictionari if the user leave some empty entry.
        # if the entry not contain the placeholder text its because the user already writed something.
        if info['name'] == self.firtname_plh:
            info['name'] = ""
        if info['lname'] == self.lastname_plh:
            info['lname'] = ""
        if info['day'] == self.day_plh:
            info['day'] = ""
        if info['month'] == self.month_plh:
            info['month'] = ""
        if info['year'] == self.year_plh:
            info['year'] = ""
        if info['country'] == self.country_plh:
            info['country'] = ""
        if info['city'] == self.city_plh:
            info['city'] = ""
        if info['gender'] == self.gender_plh:
            info['gender'] = ""
        if info['job'] == self.job_plh:
            info['job'] = ""
        if info['id'] == self.idnumber_plh:
            info['id'] = ""
        if info['address1'] == self.address1_plh:
            info['address1'] = ""
        if info['address2'] == self.address2_plh:
            info['address2'] = ""
        if info['phone1'] == self.phone1_plh:
            info['phone1'] = ""
        if info['phone2'] == self.phone2_plh:
            info['phone2'] = ""
        if info['mail'] == self.mail_plh:
            info['mail'] = ""
        if info['comment'] == self.comment_plh+"\n":
            info['comment'] = ""

        # add wanted info, if var_alarm. True it will play alarm when person found, if var_alarm_file True will open a user file.
        info["wanted"] = [self.var_alarm.get(), self.var_alarm_file.get(), self.alarm_file_path]


            
        # encode the image on a separate process and wait to get the result if return 0 all correct, if return 1 is error.
        # we need to send the image path to endode and also send the user info, its in the dictionary.
        def process():
            self.bt_addperson["state"]="disabled"
            result = myscan.encode_image(self.new_picture_path, info)
            if result:  
                self.message(text="processed correct", font="arial 20", height=6, bg="gray", fg="#00ff00")
                self.bt_addperson["state"]="normal"
                self.soundeffect("sucess")
                # if the profile is an update delete the previus profile and set vars to default.
                if self.delete_previus_profile:
                    self.bt_addperson["text"]="ADD"
                    self.delete_profile(no_window = True)
                    self.add_img = PhotoImage(file='media/add.png')
                    self.add_img2 = PhotoImage(file='media/add2.png')
                    self.bt_addperson["image"] = self.add_img
                    
            else:
                self.message(text="Error encoding \nthe image file\n please use \nanother image", font="arial 20", height=6, bg="red", fg="white")
                self.soundeffect("error")
            self.bt_addperson["state"]="normal"
            
            
        p = Thread(target=process)
        p.start()


    # ----------- bind funtions for entry ----------------
    # this make the placeholder text hide or show when mouse is over 
    # the funtion receive 3 args: event, entry and the placeholder
    # on enter if the entry text is the placeholder delete text, on leave if entry is empty put the placeholder text.    
                
    def bind_entry(self, event, entry, placeholder):
        # on enter event, change color and check if entry have placeholder to delete.
        if "Enter" in str(event):
            entry.configure(bg="#00ffff", fg="black")
            if entry.get() == placeholder:
                entry.delete(0,"end")
        else:
            # on leave event, if entry is empty put placeholder and change color to default,
            # but if the user write some text it will chage the entry bg to green.
            if entry.get() == "":
                entry.insert(0, placeholder)
                entry.configure(bg="#009999", fg="yellow")
                window.focus()
            else:
                entry.configure(bg="#00cc00",fg="black")



    
    def pickup_alarm_file(self,*event):
        self.soundeffect("click")
        # if the checkbox is already true return
        if self.var_alarm_file.get():
            
            return
        # if checkbox is false pickup the file path to open when a person marked as wanted is recognized.
        n = filedialog.askopenfile(title="Select the file to open if the person is detected")
        try:
            # save file path and set checkbox to True
            self.alarm_file_path = (n.name)
            self.var_alarm_file.set(True)
        except:
            self.alarm_file_path = ""
            self.var_alarm_file.set(False)
            





    def clear_entry(self):
        # clear all entryes in the add faces tab
        self.firtname.delete(0,"end")
        self.lastname.delete(0,"end")
        self.day.delete(0,"end")
        self.month.delete(0,"end")
        self.year.delete(0,"end")
        self.country.delete(0,"end")
        self.city.delete(0,"end")
        self.gender.delete(0,"end")
        self.job.delete(0,"end")
        self.idnumber.delete(0,"end")
        self.address1.delete(0,"end")
        self.address2.delete(0,"end")
        self.phone1.delete(0,"end")
        self.phone2.delete(0,"end")
        self.mail.delete(0,"end")
        self.comment.delete(0.0,"end")
        # add placeholder text to each entry in the add faces tab
        self.firtname.insert(0, self.firtname_plh)
        self.lastname.insert(0, self.lastname_plh)
        self.day.insert(0, self.day_plh)
        self.month.insert(0, self.month_plh)
        self.year.insert(0, self.year_plh)
        self.country.insert(0, self.country_plh)
        self.city.insert(0, self.city_plh)
        self.gender.insert(0, self.gender_plh)
        self.job.insert(0, self.job_plh)
        self.idnumber.insert(0, self.idnumber_plh)
        self.address1.insert(0, self.address1_plh)
        self.address2.insert(0, self.address2_plh)
        self.phone1.insert(0, self.phone1_plh)
        self.phone2.insert(0, self.phone2_plh)
        self.mail.insert(0, self.mail_plh)
        self.comment.insert(1.0, self.comment_plh)
        # also change text and background color to default in the add faces tab
        self.firtname.configure(bg="#009999", fg="yellow")
        self.lastname.configure(bg="#009999", fg="yellow")
        self.day.configure(bg="#009999", fg="yellow")
        self.month.configure(bg="#009999", fg="yellow")
        self.year.configure(bg="#009999", fg="yellow")
        self.country.configure(bg="#009999", fg="yellow")
        self.city.configure(bg="#009999", fg="yellow")
        self.gender.configure(bg="#009999", fg="yellow")
        self.job.configure(bg="#009999", fg="yellow")
        self.idnumber.configure(bg="#009999", fg="yellow")
        self.address1.configure(bg="#009999", fg="yellow")
        self.address2.configure(bg="#009999", fg="yellow")
        self.phone1.configure(bg="#009999", fg="yellow")
        self.phone2.configure(bg="#009999", fg="yellow")
        self.mail.configure(bg="#009999", fg="yellow")
        # set default image to button, delete picture path and reset all vars.
        self.new_picture_path = ""
        self.bt_addimage.configure(image=self.file_img, borderwidth=0)
        self.var_alarm.set(False)
        self.var_alarm_file.set(False)
        self.delete_previus_profile = False
        # change the button picture
        self.bt_addperson["text"]="ADD"
        self.add_img = PhotoImage(file='media/add.png')
        self.add_img2 = PhotoImage(file='media/add2.png')
        self.bt_addperson["image"] = self.add_img
        
        window.focus()
        self.soundeffect("sucess3")
        




    ## =================   SCREEN LIST FACES FUNTION  ============================
        
    def list_all(self):
        self.profile_list.destroy()
        # create objet page and list all profiles
        self.page = widget()
        self.page.list_profiles()
        
        # this method return the frame with all the listed profiles
        self.profile_list = self.page.get_profiles(self.show_person_info, parent=self.list_frame)
        self.profile_list.place(x=0,y=33)
        self.soundeffect("click")


    def func_next_page(self):
        try:
            self.profile_list.destroy()
            self.profile_list = self.page.next_page(self.show_person_info, parent=self.list_frame)
            self.profile_list.place(x=0,y=33)
            self.soundeffect("click")
        except:
            None

            
    def func_prev_page(self):
        try:
            self.profile_list.destroy()
            self.profile_list = self.page.previous_page(self.show_person_info, parent=self.list_frame)
            self.profile_list.place(x=0,y=33)
            self.soundeffect("click")
        except:
            None

            
    def close_profile_list(self):
        self.profile_list.destroy()
        self.soundeffect("click")


        
    def filter_profiles(self):
        self.dialogo = Toplevel()
        self.dialogo.geometry("330x500+850+100")
        self.dialogo.wm_attributes("-alpha",0.8)
        #self.dialogo.overrideredirect(True)
        self.dialogo.configure(bg="#00aaff", relief="ridge", borderwidth=20)
        self.dialogo.title("Filter Profiles")
        

        # create objet page
        self.page = widget()

        f = Frame(self.dialogo, bg="#004444", width=600,height=500, relief="groove", borderwidth=10)
        f.grid(row=0, column=1)
        f1 = Frame(f)
        # create all entry to input filter values
        firtname = Entry(f, width=22,bg="#009999",fg="yellow", font="black 10",relief="sunken",borderwidth=5)
        lastname = Entry(f, width=22,bg="#009999",fg="yellow", font="arial 10",relief="sunken",borderwidth=5)
        day = Entry(f1, width=4,bg="#009999",fg="yellow", font="arial 10",relief="sunken",borderwidth=5)
        month = Entry(f1, width=8,bg="#009999",fg="yellow", font="arial 10",relief="sunken",borderwidth=5)
        year = Entry(f1, width=6,bg="#009999",fg="yellow", font="black 10",relief="sunken",borderwidth=5)
        country = Entry(f, width=22,bg="#009999",fg="yellow", font="arial 10",relief="sunken",borderwidth=5)
        city = Entry(f, width=22,bg="#009999",fg="yellow", font="arial 10",relief="sunken",borderwidth=5)
        gender = Entry(f, width=22,bg="#009999",fg="yellow", font="arial 10",relief="sunken",borderwidth=5)
        job = Entry(f, width=22,bg="#009999",fg="yellow", font="arial 10",relief="sunken",borderwidth=5)
        idnumber = Entry(f, width=22,bg="#009999",fg="yellow", font="arial 10",relief="sunken",borderwidth=5)
        address1 = Entry(f, width=22,bg="#009999",fg="yellow", font="arial 10",relief="sunken",borderwidth=5)
        address2 = Entry(f, width=22,bg="#009999",fg="yellow", font="arial 10",relief="sunken",borderwidth=5)
        phone1 = Entry(f, width=22,bg="#009999",fg="yellow", font="arial 10",relief="sunken",borderwidth=5)
        phone2 = Entry(f, width=22,bg="#009999",fg="yellow", font="arial 10",relief="sunken",borderwidth=5)
        mail = Entry(f, width=22,bg="#009999",fg="yellow", font="arial 10",relief="sunken",borderwidth=5)
        wanted = ttk.Combobox(f, values=("True","False","Any"))
        wanted.set(value="Any")
        # show entry names with an label
        Label(f, text="Name       ", bg="#004444", fg="yellow").grid(row=0, column=0)
        Label(f, text=" Last name", bg="#004444", fg="yellow").grid(row=1, column=0)
        Label(f, text="Day/Month/Year", bg="#004444", fg="yellow").grid(row=2, column=0)
        Label(f, text="Country    ", bg="#004444", fg="yellow").grid(row=3, column=0)
        Label(f, text="City         ", bg="#004444", fg="yellow").grid(row=4, column=0)
        Label(f, text="Gender     ", bg="#004444", fg="yellow").grid(row=5, column=0)
        Label(f, text="Job          ", bg="#004444", fg="yellow").grid(row=6, column=0)
        Label(f, text=" Id number", bg="#004444", fg="yellow").grid(row=7, column=0)
        Label(f, text="Address  ", bg="#004444", fg="yellow").grid(row=8, column=0)
        Label(f, text="Address2", bg="#004444", fg="yellow").grid(row=9, column=0)
        Label(f, text="Phone     ", bg="#004444", fg="yellow").grid(row=10, column=0)
        Label(f, text="Phone 2   ", bg="#004444", fg="yellow").grid(row=11, column=0)
        Label(f, text="Email     ", bg="#004444", fg="yellow").grid(row=12, column=0)
        Label(f, text="Wanted   ", bg="#004444", fg="yellow").grid(row=13, column=0)
        # place entry
        firtname.grid(row=0, column=1)
        lastname.grid(row=1, column=1)
        f1.grid(row=2, column=1)
        day.pack(side="left")
        month.pack(side="left")
        year.pack(side="left")
        country.grid(row=3, column=1)
        city.grid(row=4, column=1)
        gender.grid(row=5, column=1)
        job.grid(row=6, column=1)
        idnumber.grid(row=7, column=1)
        address1.grid(row=8, column=1)
        address2.grid(row=9, column=1)
        phone1.grid(row=10, column=1)
        phone2.grid(row=11, column=1)
        mail.grid(row=12, column=1)
        wanted.grid(row=13, column=1)
        self.soundeffect("click")
        
        def filt_values():
            # get all entry user info and add to the dictionary
            info = {}
            info['name'] = firtname.get()
            info['lname'] = lastname.get()
            info['day'] = day.get()
            info['month'] = month.get()
            info['year'] = year.get()
            info['country'] = country.get()
            info['city'] = city.get()
            info['gender'] = gender.get()
            info['job'] = job.get()
            info['id'] = idnumber.get()
            info['address1'] = address1.get()
            info['address2'] = address2.get()
            info['phone1'] = phone1.get()
            info['phone2'] = phone2.get()
            info['mail'] = mail.get()
            # if true selected, add true to the dictionary to find if any wanted value is true in profile list.
            if wanted.get() == "True":
                info['wanted'] = "True"
            # if false selected, add "false, false," to find the string in users profiles, will mach if both are false.
            if wanted.get() == "False":
                info['wanted'] = "false, false,"
                
            
            self.profile_list.destroy()
            # create objet page
            self.page = widget()
            # list profiles with filter
            self.page.list_profiles(filter_values=info)
            # this method return the frame with all the listed profiles
            self.profile_list = self.page.get_profiles(self.show_person_info, parent=self.list_frame)
            self.profile_list.place(x=0,y=33)
            self.soundeffect("click")

        Button(self.dialogo, text="Filter", bg="green",activebackground="orange", command=filt_values).place(x=40,y=410)
        Button(self.dialogo, text="Cancell", bg="#00bbff",activebackground="orange", command=self.dialogo.destroy).place(x=150,y=410)
    
        


        
        





    ## =================   Programm general messages, sound effects and bind funtions for all tabs ============================



            
    def soundeffect(self,sound):
        if sound == "alarm":
            def alarm():
                self.stop_alarm = False
                while True:
                    playsound("./media/alarm.wav", True)
                    if self.stop_alarm:
                        break
                    
            p = Thread(target=alarm)
            p.start()

        elif self.setting_sound:
            def play():
                try:
                    if sound == "warning":
                        playsound("./media/warning.wav", True)
                    elif sound == "error":
                        playsound("./media/error.wav", True)
                    elif sound == "sucess":
                        playsound("./media/sucess.wav", True)
                    elif sound == "sucess2":
                        playsound("./media/sucess2.wav", True)
                    elif sound == "sucess3":
                        playsound("./media/sucess3.wav", True)
                    elif sound == "click":
                        playsound("./media/click.wav", True)
                    elif sound == "other":
                        playsound("./media/other.wav", True)
                    elif sound == "robot":
                        playsound("./media/robot.wav", True)
                    elif sound == "alien":
                        playsound("./media/alien.wav", True)
                    elif sound == "camera":
                        playsound("./media/camera.wav", True)
                except:
                    print("An error ocurred playing Audio files")
            p = Thread(target=play)
            p.start()



    #----  messages funtion  --------- receive args text, font, height, bg and fg color
            
    def message(self, text="", font="arial 20", height=6, bg="red", fg="white", progressbar=False):
        self.msg = Toplevel()
        self.msg.geometry("300x200+500+300")
        self.msg.wm_attributes("-alpha",0.6)
        self.msg.overrideredirect(True)
        # show general messages dialog
        Label(self.msg, text=text, font=font, height=height, bg=bg, fg=fg).pack(fill="both")

        if progressbar:
            self.progressbar = ttk.Progressbar(self.msg, length=200)
            self.progressbar.place(x=45,y=130)
        
        def ok():
            self.stop_alarm = True
            self.msg.destroy()

        Button(self.msg, text="X",command=ok, bg="red", fg="white", activebackground="red", font="arial 12",width=2).place(x=270,y=5)
        self.msg.grab_set()





    def bind_button(self, event, button, image):
        # if the button add image have the person picture will not change on mouse over.
        if button == self.bt_addimage:
            if self.new_picture_path != "":
                return
        # on enter event, change color and check if entry have placeholder to delete.
        if "Enter" in str(event):
            button.configure(image=image)         
        else:
            button.configure(image=image)
            
    # ______________END _______________








        
# define some funcion and attributes to move the windows
lastClickX = 0
lastClickY = 0

def SaveLastClickPos(event):
    global lastClickX, lastClickY
    lastClickX = event.x
    lastClickY = event.y

def Dragging(event):
    x, y = event.x - lastClickX + window.winfo_x(), event.y - lastClickY + window.winfo_y()
    window.geometry("+%s+%s" % (x , y))



window = Root()

# bind to draw window
window.bar_menu.bind('<Button-1>', SaveLastClickPos)
window.bar_menu.bind('<B1-Motion>', Dragging)

# intercept the wm exit button event however title bar is disabled since I set overrideredirect to True.
window.protocol("WM_DELETE_WINDOW", window._exit)

window["bg"]="#003333"
#window.resizable(1,1)
window.geometry("1280x720+10+0")
window.title("Face Recognition System V 1.3.0")

window.mainloop()



        

