# Orion Face Recognition System.   GUI v1.3.4
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
from face_recognition_system import Scanner
from tkinter import Label,Frame,Entry,INSERT,Canvas,Scrollbar,Checkbutton,Spinbox,Button,PhotoImage,Tk,filedialog,Toplevel,ttk,scrolledtext,BooleanVar,IntVar,Listbox,StringVar,DoubleVar,Scale
from quick_face_extractor import extractor
from face_crop import Crop
from minicard import Minicard
from makecard import Makecard
try:
    from twilio_message import Send_message
except:
    print('error in twilio_message.py')
try:
    from mail_ssl import Send_email
except:
    print('error in mail_ssl.py')


ex = extractor()
myscan = Scanner()
myscan.load_data()



class Root(Tk):
    def __init__(self):
        super().__init__()
        
        # load setting from json file if exist 
        try:
            with open("setting.json", "r") as f:
                sett = json.load(f)
            self.setting_sound = sett["sound"]
            self.setting_auto_off_camera = sett["auto_off_camera"]
            self.setting_video_source = sett["video_source"]
            self.show_camera_hud = sett["show_camera_hud"]
            self.quickscan = sett["quickscan"]
            self.tolerance = float(sett["tolerance"])
            self.smtp_host = sett["smtp_host"]
            self.smtp_port = sett["smtp_port"]
            self.smtp_user = sett["smtp_user"]
            self.smtp_pass = sett["smtp_pass"]
            self.smtp_use_ssl = sett["smtp_use_ssl"]
            self.alert_email = sett["alert_email"]
            self.twilio_account_sid = sett["twilio_account_sid"]
            self.twilio_auth_token = sett["twilio_auth_token"]
            self.twilio_active_number = sett["twilio_active_number"]
            self.alert_phone_number = sett["alert_phone_number"]
            self.enable_alert_email = sett["enable_alert_email"]
            self.enable_alert_messages = sett["enable_alert_messages"]

        except:
            self.setting_sound = True
            self.setting_auto_off_camera = False
            self.setting_video_source = 0
            self.show_camera_hud = True
            self.quickscan=True
            self.tolerance=0.55
            # account for email notifications
            self.smtp_host = 'smtp.gmail.com'
            self.smtp_port = 587
            self.smtp_user = 'example@gmail.com'
            self.smtp_pass = 'password' # 16 character google app pass
            self.smtp_use_ssl = True
            self.alert_email = 'destination@gmail.com'
            # account for message notifications
            self.twilio_account_sid = 'copy & paste API sid'
            self.twilio_auth_token = 'copy & paste API token'
            self.twilio_active_number = 'Your twilio virtual number'
            self.alert_phone_number = '+50377777777' # receiver number with area code
            self.enable_alert_email = False
            self.enable_alert_messages = False

            
        # define other vars
        self.new_picture_path = ""
        self.alarm_file_path = ""
        self.last_person_detected = ""
        self.delete_previus_profile = False
        self.stop_alarm = False
        self.profile_list = Frame()
        self.log_var = StringVar()
        myscan.tolerance(self.tolerance)
        self.stop_camera = False
        # alert checkbox vars
        self.alert_var = BooleanVar(value=False)
        self.play_sound_var = BooleanVar(value=False)
        self.run_file_on_alert = BooleanVar(value=False)
        self.email_var = BooleanVar(value=False)
        self.mobile_message_var = BooleanVar(value=False)
        


        
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
        self.wm_iconbitmap(bitmap="media/icon.ico")
        
        self.video_bg = PhotoImage(file='media/video_bg.png')
        self.log_bg = PhotoImage(file='media/log_bg.png')
        #self.card_img = PhotoImage(file='media/card.png')
        self.comment_img = PhotoImage(file='media/comment_img.png')
        self.warning_img = PhotoImage(file='media/warning_img.png')
        self.setting_img = PhotoImage(file='media/setting_img.png')
        
        
        
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


        #button scan file
        self.bt_open_file = Button(self.search_frame, image=self.file_img,command=self.file, borderwidth=0,bg="#002222", activebackground="#002222")
        self.bt_open_file.place(x=520, y=200)
        # button scan muti files
        self.bt_multifiles = Button(self.search_frame, image=self.multifile_img, command=self.multi_files , bd=0,bg="#002222", activebackground="#002222")
        self.bt_multifiles.place(x=520, y=370)
        #button close hided
        self.bt_close = Button(self.search_frame, image=self.close_img,command=self.close,bg="#002222", activebackground="#002222",borderwidth=0)
        #button clear
        self.bt_clear = Button(self.search_frame,image=self.clear_img, command=self.clear,bg="#002222",borderwidth=0, activebackground="#002222")
        self.bt_clear.place(x=520, y=530)

        # create 2 frame with colored border.
        self.info_frame2 = Frame(self.search_frame, bg='#007777', borderwidth=3)
        self.info_frame2.place(x=820,y=20)
        self.info_frame1 = Frame(self.search_frame, bg='#007777', borderwidth=3, width=546, heigh=364)
        self.info_frame1.place(x=680,y=235)
        self.info_frame1.pack_propagate(False)
        # create 2 label to show the recognized person info and card inside of the 2 previous frame.
        self.info = Label(
            self.info_frame1,
            text='NO INFO AVAILABLE',
            bg='#000011',
            fg="#00ffff",
            font=('arial',30),
            heigh=10,
            )
        self.info.pack(fill='both')
        self.info2 = Label(self.info_frame2, image=self.comment_img, bg='#000011')
        self.info2.pack()
        self.show_comment = Label(self.info_frame2, width=30, height=10, bg='black', fg='#66bbff', wrapleng=210, anchor="nw", justify="left")
        self.show_comment.place(x=30, y=38)
        
        # box container with background to show video in label
        self.video_box = Frame(self.search_frame, bg='blue', bd=2)
        self.video_box.place(x=30,y=235)
        Label(self.video_box, image=self.video_bg, bg='black').pack()
        # buttton scan camera
        self.bt_open_camera = Button(self.video_box, image=(self.camera_img), command=self.camera, borderwidth=0,bg="#000000",activebackground="#002222")
        self.bt_open_camera.place(x=100, y=50)
        # label to show video
        self.lvideo = Label(self.video_box, relief="ridge", bg="#0000ff")
        
        
        # buttons delete profile and button edit profile
        self.bt_edit_profile = Button(self.search_frame, text=" Edit profile ", bg="#00aaff", command=self.edit_profile, activebackground="#00aaff")
        self.bt_delete_profile = Button(self.search_frame, text="Delete profile", bg="#00aaff", command=self.delete_profile, activebackground="red")

        # lisbox to show the log of persons recognized in current session.
        self.log_frame = Frame(self.search_frame, bg='blue', borderwidth=2)
        self.log_frame.place(x=30, y=40)
        Label(self.log_frame, image=self.log_bg,bg='black', bd=0).pack()
        self.log_list = Listbox(self.log_frame, listvariable=self.log_var, width=68, height=9, bg="#000000",fg="#00ffff")
        self.log_list.place(x=27,y=25)
                
        #------- create a scrollable widget to show multiresult -------
        def myfunction(event):
            canvas.configure(scrollregion=canvas.bbox("all"), width = 634, height = 600)
            
        self.multi_result_container = Frame(self.search_frame, relief="groove", width=50, height=100, bd=5, bg="#00ffff")
        
        canvas = Canvas(self.multi_result_container, width=634, height=600, bg="#000000")
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
        self.bt_allresult.bind("<Enter>", lambda x: self.bt_allresult.configure(bg="#00ffff"))
        self.bt_allresult.bind("<Leave>", lambda x: self.bt_allresult.configure(bg="#00aaff"))
        

        #-------bind--------- to change button image when mouse is over.
        self.bt_open_camera.bind("<Enter>", lambda event: self.bind_button(event, self.camera_img2))
        self.bt_open_camera.bind("<Leave>", lambda event: self.bind_button(event, self.camera_img))
        self.bt_open_file.bind("<Enter>", lambda event: self.bind_button(event, self.file_img2))
        self.bt_open_file.bind("<Leave>", lambda event: self.bind_button(event, self.file_img))
        self.bt_multifiles.bind("<Enter>", lambda event: self.bind_button(event, self.multifile_img2))
        self.bt_multifiles.bind("<Leave>", lambda event: self.bind_button(event, self.multifile_img))
        self.bt_clear.bind("<Enter>", lambda event: self.bind_button(event, self.clear_img2))
        self.bt_clear.bind("<Leave>", lambda event: self.bind_button(event, self.clear_img))
        self.bt_close.bind("<Enter>", lambda event: self.bind_button(event, self.close_img2))
        self.bt_close.bind("<Leave>", lambda event: self.bind_button(event, self.close_img))
        # hide multiresult container when leave
        self.multi_result_container.bind("<Leave>",lambda x=None: self.multi_result_container.place_forget())
        # show resut when click in the log list
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
        self.bt_clear_entry = Button(self.add_frame, image=self.clear_img,command=self.clear_entry, bg="#002222",borderwidth=0, activebackground="#002222")
        self.bt_clear_entry.place(x=595, y=560)

        # alert options checkbox
        box = Frame(self.add_frame, bg="#00ffff", relief="ridge", borderwidth=3)
        box.place(x=300,y=380)
        Label(box, text="Enable Alert", bg="#00bbbb", fg="yellow", font="arial 14").grid(sticky="NSEW")

        def enable_disable_alert():
            self.soundeffect("click")
            if not self.alert_var.get():
                self.alert_chbox['bg'] = 'red'
                chbox2['state'] = 'disabled'
                chbox3['state'] = 'disabled'
                chbox4['state'] = 'disabled'
                chbox5['state'] = 'disabled'
            else:
                self.alert_chbox['bg'] = '#00ff00'
                chbox2['state'] = 'normal'
                chbox3['state'] = 'normal'
                chbox4['state'] = 'normal'
                chbox5['state'] = 'normal'
                
        self.alert_chbox = Checkbutton(
            box,
            text="Enable Alert",
            bg="red",
            font="arial 10",
            var=self.alert_var,
            relief="raised",
            command=enable_disable_alert,
            borderwidth=5,
            )
        self.alert_chbox.grid(sticky="NSEW")
        
        
        chbox2 = Checkbutton(
            box,
            text="Play alarm",
            bg="#00bbbb",
            font="arial 10",
            var=self.play_sound_var,
            relief="raised",
            borderwidth=5,
            state="disabled",
            )
        chbox2.grid(sticky="NSEW")
        chbox2.bind("<Button-1>", lambda x=None:self.soundeffect("click"))
        
        
        chbox3 = Checkbutton(
            box,
            text="Open file ",
            bg="#00bbbb",
            font="arial 10",
            var=self.run_file_on_alert,
            relief="raised",
            borderwidth=5,
            activebackground="#00bbbb",
            state="disabled",
            )
        chbox3.grid(sticky="NSEW")
        chbox3.bind("<Button-1>", self.pickup_alarm_file)


        chbox4 = Checkbutton(
            box,
            text="Send Email",
            bg="#00bbbb",
            font="arial 10",
            var=self.email_var,
            relief="raised",
            borderwidth=5,
            state="disabled",
            )
        chbox4.grid(sticky="NSEW")
        chbox4.bind("<Button-1>", lambda x=None:self.soundeffect("click"))

        chbox5 = Checkbutton(
            box,
            text="Mobile message",
            bg="#00bbbb",
            font="arial 10",
            var=self.mobile_message_var,
            relief="raised",
            borderwidth=5,
            state="disabled",
            )
        chbox5.grid(sticky="NSEW")
        chbox5.bind("<Button-1>", lambda x=None:self.soundeffect("click"))


        
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
        self.website = Entry(self.add_frame, width=20,bg="#009999",fg="yellow", font="arial 15",relief="sunken",borderwidth=5)
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
        self.website.place(x=840,y=170)
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
        self.website_plh = "Website"
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
        self.website.insert(0, self.website_plh)
        self.phone1.insert(0, self.phone1_plh)
        self.phone2.insert(0, self.phone2_plh)
        self.mail.insert(0, self.mail_plh)
        self.comment.insert(1.0, self.comment_plh)
        
        # call bind funtion to add and delete placeholder from the entry
        # we send the entry name to work on it, and send current placeholder to compare if the current text
        # on the entry is the placeholder or the user text, and put placeholder on the entry if user leave empty.
        self.firtname.bind("<Enter>", lambda event: self.bind_entry(event, self.firtname_plh))
        self.firtname.bind("<Leave>", lambda event: self.bind_entry(event, self.firtname_plh))
        self.lastname.bind("<Enter>", lambda event: self.bind_entry(event, self.lastname_plh))
        self.lastname.bind("<Leave>", lambda event: self.bind_entry(event, self.lastname_plh))
        self.day.bind("<Enter>", lambda event: self.bind_entry(event, self.day_plh))
        self.day.bind("<Leave>", lambda event: self.bind_entry(event, self.day_plh))
        self.month.bind("<Enter>", lambda event: self.bind_entry(event, self.month_plh))
        self.month.bind("<Leave>", lambda event: self.bind_entry(event, self.month_plh))
        self.year.bind("<Enter>", lambda event: self.bind_entry(event, self.year_plh))
        self.year.bind("<Leave>", lambda event: self.bind_entry(event, self.year_plh))
        self.country.bind("<Enter>", lambda event: self.bind_entry(event, self.country_plh))
        self.country.bind("<Leave>", lambda event: self.bind_entry(event, self.country_plh))
        self.city.bind("<Enter>", lambda event: self.bind_entry(event, self.city_plh))
        self.city.bind("<Leave>", lambda event: self.bind_entry(event, self.city_plh))
        self.gender.bind("<Enter>", lambda event: self.bind_entry(event, self.gender_plh))
        self.gender.bind("<Leave>", lambda event: self.bind_entry(event, self.gender_plh))
        self.job.bind("<Enter>", lambda event: self.bind_entry(event, self.job_plh))
        self.job.bind("<Leave>", lambda event: self.bind_entry(event, self.job_plh))
        self.idnumber.bind("<Enter>", lambda event: self.bind_entry(event, self.idnumber_plh))
        self.idnumber.bind("<Leave>", lambda event: self.bind_entry(event, self.idnumber_plh))
        self.address1.bind("<Enter>", lambda event: self.bind_entry(event, self.address1_plh))
        self.address1.bind("<Leave>", lambda event: self.bind_entry(event, self.address1_plh))
        self.website.bind("<Enter>", lambda event: self.bind_entry(event, self.website_plh))
        self.website.bind("<Leave>", lambda event: self.bind_entry(event, self.website_plh))
        self.phone1.bind("<Enter>", lambda event: self.bind_entry(event, self.phone1_plh))
        self.phone1.bind("<Leave>", lambda event: self.bind_entry(event, self.phone1_plh))
        self.phone2.bind("<Enter>", lambda event: self.bind_entry(event, self.phone2_plh))
        self.phone2.bind("<Leave>", lambda event: self.bind_entry(event, self.phone2_plh))
        self.mail.bind("<Enter>", lambda event: self.bind_entry(event, self.mail_plh))
        self.mail.bind("<Leave>", lambda event: self.bind_entry(event, self.mail_plh))


        # bind for buttons (change images when mouse is over)
        self.bt_addimage.bind("<Enter>", lambda event: self.bind_button(event, self.file_img2))
        self.bt_addimage.bind("<Leave>", lambda event: self.bind_button(event, self.file_img))
        self.bt_addperson.bind("<Enter>", lambda event: self.bind_button(event, self.add_img2))
        self.bt_addperson.bind("<Leave>", lambda event: self.bind_button(event, self.add_img))
        self.bt_clear_entry.bind("<Enter>", lambda event: self.bind_button(event, self.clear_img2))
        self.bt_clear_entry.bind("<Leave>", lambda event: self.bind_button(event, self.clear_img))


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
        # create top level dialog
        self.dialogo = Toplevel()
        self.dialogo.geometry("600x350+350+200")#250x320
        self.dialogo.wm_attributes("-alpha",0.9)
        self.dialogo.overrideredirect(True)
        self.dialogo.configure(bd=0,)
        Label(self.dialogo, image=self.setting_img,bd=0, bg="#333333").place(x=0,y=0)
        
        f = Frame(self.dialogo)
        f.place(x=25,y=36)
        
        # create vars for checkbox 
        sound = BooleanVar(value = self.setting_sound)
        stop = BooleanVar(value = self.setting_auto_off_camera)
        hud = BooleanVar(value = self.show_camera_hud)
        vid = IntVar(value = self.setting_video_source)
        quickscan = BooleanVar(value = self.quickscan)
        tolerance = IntVar()
        ssl = BooleanVar(value = self.smtp_use_ssl)
        enable_email = BooleanVar(value = self.enable_alert_email)
        enable_messages = BooleanVar(value = self.enable_alert_messages)


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
            borderwidth=3,
            ).grid(sticky='we')
        
        Checkbutton(
            f,
            text="Stop Camera if Person Found",
            var=stop,
            anchor="nw",
            bg="#00aaff",
            activebackground="orange",
            width=25,
            relief="raised",
            borderwidth=3,
            ).grid(sticky='we')
        
        Checkbutton(
            f,
            text="Show Camera Hud",
            var=hud, anchor="nw",
            bg="#00aaff",
            activebackground="orange",
            width=25,
            relief="raised",
            borderwidth=3,
            ).grid(sticky='we')
        # video source spinbox
        box = Frame(f)
        box.grid()
        video = Spinbox(
            box,
            from_ = 0,
            to = 8,
            textvariable = vid,
            bg="#00aaff",
            font="Verdana 12",
            width=4,
            relief="raised",
            borderwidth=3,
            )
        video.grid(row=0, column=0)
        Label(
            box,
            text="Video Source",
            bg="#00aaff",
            font="Verdana 10",
            width=24,
            relief="ridge",
            borderwidth=3
            ).grid(row=0, column=1)

        # tolerance scale
        box2 = Frame(f, bg="#00aaff", relief="raised", borderwidth=3,)
        box2.grid(sticky='we')
        Scale(
            box2,
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
        Label(box2, text="Tolerance", bg="#00aaff").pack()
        # quick scan checkbox
        Checkbutton(
            f,
            text="Quick Scan",
            var=quickscan,
            anchor="nw",
            bg="#00aaff",
            activebackground="orange",
            width=25,
            relief="raised",
            borderwidth=3,
            ).grid(sticky='we')
        # email & messages alert field
        box3 = Frame(f, bg="#00aaff", relief='ridge',bd=3)
        box3.grid(sticky='we')
        Checkbutton(box3, text='Alert Email', bg="#00aaff", variable=enable_email,anchor='w').grid(row=0, column=0, sticky='we')
        mail_alert = Entry(box3, bg='light blue', width=24)
        mail_alert.grid(row=0, column=1, sticky='we')
        mail_alert.insert(0, self.alert_email)
        Checkbutton(box3, text='Alert Messages', bg="#00aaff", variable=enable_messages).grid(row=1, column=0, sticky='we')
        phone_alert = Entry(box3, bg='light blue', width=24)
        phone_alert.grid(row=1, column=1, sticky='we')
        phone_alert.insert(0, self.alert_phone_number)
        def plus1(event):
            if not phone_alert.get().startswith('+'):
                phone_alert.insert(0,'+')
        phone_alert.bind('<Leave>',plus1)
        

        # -- entry for smtp mail settings --
        bg='#333333'
        fg='#44ddff'
        f2 = Frame(self.dialogo, bg=bg,width=200,height=300)
        f2.place(x = 285, y = 36)
        
        Label(f2,
              text='Smtp account for email alert',
              bg=bg,
              fg='#00ff00',
              font=('verdana',12)
              ).grid(row=0, column=0,columnspan=2, sticky='we',pady=5)
        
        Label(f2, text='Smtp host', bg=bg, fg=fg).grid(row=1, column=0, sticky='we')
        smtp_host = Entry(f2, bg='light blue', width=24)
        smtp_host.grid(row=1, column=1, sticky='we')
        Label(f2, text='Smtp port', bg=bg, fg=fg).grid(row=2, column=0, sticky='we')
        smtp_port = Entry(f2, bg='light blue', width=24)
        smtp_port.grid(row=2, column=1, sticky='we')
        Label(f2, text='Smtp user', bg=bg, fg=fg).grid(row=3, column=0, sticky='we')
        smtp_user = Entry(f2, bg='light blue', width=24)
        smtp_user.grid(row=3, column=1, sticky='we')
        Label(f2, text='Smtp pass', bg=bg, fg=fg).grid(row=4, column=0, sticky='we')
        smtp_pass = Entry(f2, bg='light blue', width=24)
        smtp_pass.grid(row=4, column=1, sticky='we')
        Checkbutton(
            f2,
            text="Use SSL",
            var=ssl,
            bg="#00aaff",
            activebackground="orange",
            width=24,
            font=('arial',8),
            relief="raised",
            ).grid(row=5, column=1, sticky='we')
        
        smtp_host.insert(0, self.smtp_host)
        smtp_port.insert(0, self.smtp_port)
        smtp_user.insert(0, self.smtp_user)
        smtp_pass.insert(0, self.smtp_pass)
        
        # -- entry for twilio messages settings --
        Label(f2,
              text='Twilio account for messages alert',
              bg=bg,
              fg='#00ff00',
              font=('verdana',12),
              ).grid(row=6, column=0,columnspan=2, sticky='we',pady=8)
        
        Label(f2, text='Twilio API sid', bg=bg, fg=fg).grid(row=7, column=0, sticky='we')
        twilio_sid = Entry(f2, bg='light blue', width=24)
        twilio_sid.grid(row=7, column=1, sticky='we')
        Label(f2, text='Twilio Auth token', bg=bg, fg=fg).grid(row=8, column=0, sticky='we')
        twilio_token = Entry(f2, bg='light blue', width=24)
        twilio_token.grid(row=8, column=1, sticky='we')
        Label(f2, text='Twilio virtual number', bg=bg, fg=fg).grid(row=9, column=0, sticky='we')
        twilio_active_number = Entry(f2, bg='light blue', width=24)
        twilio_active_number.grid(row=9, column=1, sticky='we')
        def plus2(event):
            if not twilio_active_number.get().startswith('+'):
                twilio_active_number.insert(0,'+')
        twilio_active_number.bind('<Leave>',plus2)
        

        twilio_sid.insert(0, self.twilio_account_sid)
        twilio_token.insert(0, self.twilio_auth_token)
        twilio_active_number.insert(0, self.twilio_active_number)
        
        
                
                
        def save():
            # save setting, and make changes to start using it.
            self.soundeffect("click")
            self.setting_sound = sound.get()
            self.setting_auto_off_camera = stop.get()
            self.setting_video_source = vid.get()
            self.show_camera_hud = hud.get()
            self.quickscan = quickscan.get()
            # save notification smtp account
            self.smtp_host = smtp_host.get()
            self.smtp_port = smtp_port.get()
            self.smtp_user = smtp_user.get()
            self.smtp_pass = smtp_pass.get()
            self.alert_email = mail_alert.get()
            self.smtp_use_ssl = ssl.get()
            # save notification twilio account
            self.twilio_account_sid = twilio_sid.get()
            self.twilio_auth_token = twilio_token.get()
            self.twilio_active_number = twilio_active_number.get()
            self.alert_phone_number = phone_alert.get()
            self.enable_alert_email = enable_email.get()
            self.enable_alert_messages = enable_messages.get()
            
            # scale widget return tolerance integer but we need float
            # save tolerance in string because float have bug: 0.10 become 0.1
            if tolerance.get() < 10:
                self.tolerance = ("0.0" + str(tolerance.get()))
            else:
                self.tolerance = ("0." + str(tolerance.get()))
                
            # set tolerance setting to the face recognitiom system
            myscan.tolerance(self.tolerance)
            # create dictionari and save the setting to json file
            setting = {
                "sound":sound.get(),
                "auto_off_camera":stop.get(),
                "video_source":vid.get(),
                "show_camera_hud":hud.get(),
                "quickscan":self.quickscan,
                "tolerance":self.tolerance,
                "smtp_host":self.smtp_host,
                "smtp_port":self.smtp_port,
                "smtp_user":self.smtp_user,
                "smtp_pass":self.smtp_pass,
                "smtp_use_ssl":self.smtp_use_ssl,
                "alert_email":self.alert_email,
                "twilio_account_sid":self.twilio_account_sid,
                "twilio_auth_token":self.twilio_auth_token,
                "twilio_active_number":self.twilio_active_number,
                "alert_phone_number":self.alert_phone_number,
                "enable_alert_email":enable_email.get(),
                "enable_alert_messages":enable_messages.get(),
                }
            setting = json.dumps(setting)
            with open("setting.json", "w") as f:
                f.write(setting)
            self.dialogo.destroy()

        def reset():
            sound.set(True)
            stop.set(False)
            hud.set(True)
            vid.set(0)
            quickscan.set(True)
            tolerance.set(55)
            ssl.set(True)
            smtp_host.delete(0,'end')
            smtp_port.delete(0,'end')
            smtp_user.delete(0,'end')
            smtp_pass.delete(0,'end')
            twilio_sid.delete(0,'end')
            twilio_token.delete(0,'end')
            twilio_active_number.delete(0,'end')
            smtp_host.insert(0,'smtp.gmail.com')
            smtp_port.insert(0,'587')
            smtp_user.insert(0,'example@gmail.com')
            smtp_pass.insert(0,'password')
            twilio_sid.insert(0,'copy & paste API sid')
            twilio_token.insert(0,'copy & paste API token')
            twilio_active_number.insert(0,'Your twilio virtual number')
            
        Button(
            self.dialogo,
            text="Ok",
            command=save,
            bg="orange",
            relief="raised",
            borderwidth=3,
            width=8,
            activebackground="green"
            ).place(x=200,y=310)
        Button(
            self.dialogo,
            text="Reset",
            command=reset,
            bg="orange",
            relief="raised",
            borderwidth=3,
            width=8,
            activebackground="green"
            ).place(x=270,y=310)
        Button(
            self.dialogo,
            text="Cancell",
            command=lambda x=None:(self.dialogo.destroy(),self.soundeffect("click")),
            bg="orange",
            relief="raised",
            borderwidth=3,
            width=8,
            activebackground="yellow"
            ).place(x=340,y=310)
        self.soundeffect("other")
        self.dialogo.grab_set()
        # ---------  END SETTING  ------------





    def about(self):
        self.dialogo = Toplevel()
        self.dialogo.geometry("300x200+500+300")
        self.dialogo.wm_attributes("-alpha",0.8)
        self.dialogo.overrideredirect(True)
        # use label with a image as background
        bg = '#333333'
        Label(self.dialogo, image=self.warning_img, bg=bg,).pack()
        
        Label(self.dialogo, text="ORION",bg=bg,fg="orange",font="arial 20").place(x=100,y=5)
        Label(self.dialogo, text="Orion Face Recognition System",bg=bg,fg="#44ddff").place(x=20,y=40)
        Label(self.dialogo, text="Version 1.3.4",bg=bg,fg="#44ddff").place(x=20,y=55)
        Label(self.dialogo, text="Author: Erick Esau Martinez",bg=bg,fg="#44ddff").place(x=20,y=70)
        Label(self.dialogo, text="Mail: martinezesau90@gmail.com",bg=bg,fg="#44ddff").place(x=20,y=85)
        Button(
            self.dialogo,
            text="Website: https://erickesau.wordpress.com",
            command=lambda x=None:webbrowser.open("https://erickesau.wordpress.com"),
            bg="#004444",
            fg="#44ddff",
            activebackground="orange",
            ).place(x=20,y=105)
        
        Button(
            self.dialogo,
            text="Github: https://github.com/Erickesau",
            command=lambda x=None:webbrowser.open("https://github.com/Erickesau"),
            bg="#004444",
            fg="#44ddff",
            activebackground="orange"
            ).place(x=20,y=135)
        
        Button(
            self.dialogo,
            text="Donate with paypal",
            command=lambda x=None:webbrowser.open("https://www.paypal.com/paypalme/erickesau0"),
            bg='orange',
            activebackground="orange"
            ).place(x=90,y=164)
        
        Button(
            self.dialogo,
            text="X",
            command=lambda x=None:(self.dialogo.destroy(),self.soundeffect("click")),
            bg="red",
            fg='white',
            activebackground="orange",
            relief="raised",
            borderwidth=5,
            ).place(x=260,y=10)
        
        self.soundeffect("other")
        self.dialogo.grab_set()


        
        

    # ===================== SCREEN SEARCH FOR FACES FUNCIONS =============================



    def camera(self):
        if self.stop_camera:
            return
        # place the Label to show video
        self.lvideo.place(x=22,y=22)
        self.bt_close.place(x=30, y=600)
        # start camera and send the number of the camera to use default camera=0
        myscan.scan_camera(camera=self.setting_video_source)

        
        def show_frame():
            if self.stop_camera:
                self.stop_camera = False
                return
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
        self.bt_close.place_forget()
        self.stop_camera = True
        self.soundeffect("other")


    def file(self):
        # -------- open a picture to scan and recofnize faces
        self.soundeffect("alien")
        filename = filedialog.askopenfile(title="Open image to scan",filetypes=("Images *.jpg","Images *.jpeg","Images *.png"))
        if filename:
            #------------------ recognize face --------------
            def recognize():
                #recognize face if fullscan is true it will return a tuple with names and distances lists
                match = myscan.scan_file(
                    filename.name,
                    quickscan=self.quickscan,
                    )
                
                if match:
                    
                    if not self.quickscan:
                        
                        # unpack tuple (profiles contain the list of profiles that match)
                        profiles, distance = match
                        # get the index with lowes distance (low tolerance)
                        index = distance.index(min(distance))
                        # get name from that index.
                        person = profiles[index]
                        # show the card
                        self.show_person_info(person, add_to_log=True)
                        return match
                    else:
                        self.show_person_info(match, add_to_log=True)
                        return False
                        
                elif match == None:
                    self.message(text="\nError \nNo Faces Found")
                    self.soundeffect("warning")
                    return False
                else:
                    self.message(text="\n\nNot Person Found", bg="orange")
                    self.soundeffect("warning")
                    return False
                
            match = recognize()
            if match:
                                
                profiles, distances = match
                # ----- load profile images with pillow
                self.loaded_images = []
                for path in profiles:
                    img = Image.open(path + "./thumbnail card.png")
                    #img = img.resize((100,120))
                    self.loaded_images.append(ImageTk.PhotoImage(image=img))
                    
                # ---- destroy all existing buttons from the list ----
                for child in self.multi_result.winfo_children():
                    child.destroy()

                # ---- add new profiles buttons to the list -----
                index = 0
                col = 0
                row = 0
                for name,dis in zip(profiles, distances):
                    # add to log istory
                    self.add_to_log(name)
                    # prepar background color
                    with open(f'./{name}/profile.json', 'r') as f:
                        f = json.load(f)
                        if f['alert']:
                            color = 'red'
                        else:
                            color = 'black'
                    # show profile minicard in the list
                    Button(
                        self.multi_result,
                        image=self.loaded_images[index],
                        command=lambda x=name:self.show_person_info(x, wanted_alert=False),
                        bg=color,
                        bd=2,
                        ).grid(column=col, row=row)
                    
                    index += 1
                    col += 1
                    if col==2:
                        row += 1
                        col = 0
                self.multi_result_container.place(x=20,y=20)
                self.bt_allresult.place(x=10,y=20)
                
            #----------------------------------
                



    #----------------------------------
    #select multifiles
    def multi_files(self):
        def run_on_thread():
            self.soundeffect("alien")
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
                try:
                    p = 100 / num
                except ZeroDivisionError:
                    self.message(text='\nError\n No faces found')
                    raise
                porcent = 0
                self.message(
                    progressbar=1,
                    bg="orange",
                    text="Loading"
                    )
                
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
                    img = Image.open(path + "./thumbnail card.png")
                    #img = img.resize((100,120))
                    self.loaded_images.append(ImageTk.PhotoImage(image=img))
                    
                # ----- show all profiles that math ------------
                # ---- destroy all existing thumbdnail card from the list ----
                for child in self.multi_result.winfo_children():
                    child.destroy()
                # ---- add new profiles thumbdnail card to the list -----
                index = 0
                col = 0
                row = 0
                for name in match:
                    # add to log
                    self.add_to_log(name)
                    # prepar background color
                    with open(f'./{name}/profile.json', 'r') as f:
                        f = json.load(f)
                        if f['alert']:
                            color = 'red'
                        else:
                            color = 'black'
                    # show thumdbnail card
                    Button(
                        self.multi_result,
                        image=self.loaded_images[index],
                        command=lambda x=name:self.show_person_info(x, wanted_alert=False),
                        bg=color,
                        bd=2,
                        ).grid(column=col, row=row)
                    
                    index += 1
                    col += 1
                    if col==2:
                        row += 1
                        col = 0
                        
                self.multi_result_container.place(x=20,y=20)
                self.bt_allresult.place(x=10,y=20)
                self.soundeffect("sucess2")
                self.msg.destroy()
                
            elif match == None:
                self.msg.destroy()
                
            else:
                self.msg.destroy()
                self.message(text="\n\nNot Person Found", bg="orange")
                self.soundeffect("warning")

        th = Thread(target=run_on_thread)
        th.start()

        #----------------------------------
             


                
    def add_to_log(self, path):
        # when a person is recognized add the person to the log listbox
        with open(path + '/profile.json', 'r') as f:
            profile = json.load(f)
        tim = time.strftime("%m/%d/%y %I:%M %p")
        name = str(profile["name"]) + " " + str(profile["lname"])
        if profile["alert"]:
            alert = ">>>>"
        else:
            alert = "______"
        l = [f"{alert} {name} {tim} {path}"]
        for line in (self.log_list.get(0,"end")):
            l.append(line)
        self.log_var.set(l)
        



    def clear(self):
        # set search faces tab to default text and buttons
        self.last_person_detected = ""
        self.bt_edit_profile.place_forget()
        self.bt_delete_profile.place_forget()
        self.multi_result_container.place_forget()
        self.soundeffect("sucess3")
        self.bt_allresult.place_forget()
        self.show_comment['text'] = ''
        self.info.configure(heigh = 10, image = '')
        self.info_frame1['bg'] = '#007777'


    #----------------------------------


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
        self.bt_edit_profile.place(x=745,y=210)
        self.bt_delete_profile.place(x=1100,y=210)
        # show card
        try:
            self.info.img = PhotoImage(file=person+"/"+"card.png")
            self.info.configure(image=self.info.img, heigh = 364)
        except:
            self.message(
                text="Error \ncould not read file \n"+person+"\ncard.png  \nmaybe not exist or name is wron",
                font="arial 12",
                fg="red"
                )
            self.soundeffect("error")
            raise
            
        try:
            # open profile.txt is in the same folder 
            with open(person +"/"+ "profile.json", "r") as f:
                profile = json.load(f)
        except:
            self.message(
                text="Error \ncould not read file \n"+person+"\nprofile.json \n maybe not exist or name is wron",
                font="arial 12",
                fg="red"
                )
            self.soundeffect("error")
            raise
                
        # now show the comment in the label
        self.show_comment['text'] = profile["comment"]
            
        # when a person is recognized add the person to the log listbox
        if add_to_log:
            self.add_to_log(person)
        # show red border if the person have alert active
        if profile["alert"]:
            self.info_frame1['bg'] = 'red'
        else:
            self.info_frame1['bg'] = '#007777'
        
        # if this funtion is called from the list_faces tab, wanted_alert is set to false so will not play alert.
        if wanted_alert == False:
            return
        
        self.soundeffect("sucess2")
        # if the person have alert activated execute the actions
        if profile["alert"]:
            #------------------------
            if profile["play_sound"]:
                self.message(
                    text="\nWanted \nperson detected",
                    bg='#ff0000',
                    fg='white',
                    )
                self.soundeffect("alarm")
            #------------------------
            if profile["open_file"]:
                try:
                    os.startfile(profile["open_file"])
                except:
                    print('cant open ',profile["open_file"])
            #------------------------
            if self.enable_alert_email and profile["send_email"]:
                def fun1():
                    try:
                        Send_email(
                            host = self.smtp_host,
                            port = self.smtp_port,
                            user = self.smtp_user,
                            password = self.smtp_pass,
                            to = self.alert_email,
                            text = profile["name"] + ' ' + profile["lname"],
                            )
                    except :
                        print('error cant send email check internet connection and account info')
                t = Thread(target=fun1)
                t.start()
            
            #------------------------
            if self.enable_alert_messages and profile["send_message"]:
                def fun2():
                    try:
                        Send_message(
                            account_sid = self.twilio_account_sid,
                            auth_token = self.twilio_auth_token,
                            twilio_active_number = self.twilio_active_number,
                            to = self.alert_phone_number,
                            body = '\nperson recognized: ' + profile["name"] + ' ' + profile["lname"],
                            )
                    except:
                        print('error cant send message check internet connection and account info')
                t2 = Thread(target=fun2)
                t2.start()





    #----------------------------------
        

    def delete_profile(self, no_window=False):
        if no_window:
            try:
                myscan.delete_profile(self.delete_previus_profile)
                # delete profile from the log
                lis = []
                for line in (self.log_list.get(0,"end")):
                    if not self.delete_previus_profile in line:
                        lis.append(line)
                self.log_var.set(lis)
            finally:
                self.delete_previus_profile = False
                return
            
        self.msg = Toplevel()
        self.msg.geometry("300x200+500+300")
        self.msg.wm_attributes("-alpha",0.9)
        self.msg.overrideredirect(True)
        # use label with a image as background
        Label(self.msg, image=self.warning_img, bg='yellow',).pack()
        # create frame container
        box = Frame(self.msg, width=276, height=160, bg='yellow')
        box.pack_propagate(False)
        box.place(x=11, y=18)
        # show delete profile dialog
        Label(box, text="\n!!! DELETE PROFILE !!!", bg='yellow', fg="red", font="Arial 20").pack(fill='both')

        def delete():
            self.soundeffect("click")
            self.msg.destroy()
            try:
                # list files
                l = os.listdir(self.last_person_detected)
            except:
                self.message(text=self.last_person_detected +"/\n NOT EXIST",font="arial 12",height="11")
                self.clear()
                self.soundeffect("error")
                return
            # remove profile
            myscan.delete_profile(self.last_person_detected)
            # delete profile from the log if its in the log.
            lis = []
            for line in (self.log_list.get(0,"end")):
                if not self.last_person_detected in line:
                    lis.append(line)
            self.log_var.set(lis)
            self.clear()

            
            
        def cancell():
            self.soundeffect("click")
            self.msg.destroy()
            
        Button(
            self.msg,
            text="DELETE",
            command=delete,
            bg="red",
            fg="white",
            activebackground="red",
            font="arial 12"
            ).place(x=24,y=150)
        
        Button(
            self.msg,
            text="CANCELL",
            command=cancell,
            bg="green",
            fg="white",
            activebackground="#00ff00",
            font="arial 12"
            ).place(x=180,y=150)
        
        self.soundeffect("warning")
        self.msg.grab_set()



    #----------------------------------



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
        self.website.delete(0,"end")
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
        self.website.insert(0, i['website'])
        self.phone1.insert(0, i['phone1'])
        self.phone2.insert(0, i['phone2'])
        self.mail.insert(0, i['mail'])
        self.comment.insert(0.0, i['comment'])

        # uncheck alert checkbox
        if self.alert_var.get():
            self.alert_chbox.invoke()
        # check checkbox if profile have alert enabled
        if i['alert']:
            self.alert_chbox.invoke()
        self.play_sound_var.set(i['play_sound'])
        if i['open_file']:
            self.run_file_on_alert.set(True)
            self.alarm_file_path = i['open_file']
        else:
            self.run_file_on_alert.set(False)
            self.alarm_file_path = ''
        self.email_var.set(i['send_email'])
        self.mobile_message_var.set(i['send_message'])

        
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

        # put pleceholder if entry is empty
        def pl(widget, placeholder):
            if widget.get() == "":
                widget.insert(0, placeholder)
                widget.configure(bg="#009999", fg="yellow")
                window.focus()
            else:
                widget.configure(bg="#00cc00",fg="black")
        pl(self.firtname, self.firtname_plh)
        pl(self.lastname, self.lastname_plh)
        pl(self.day, self.day_plh)
        pl(self.month, self.month_plh)
        pl(self.year, self.year_plh)
        pl(self.country, self.country_plh)
        pl(self.city, self.city_plh)
        pl(self.gender, self.gender_plh)
        pl(self.job, self.job_plh)
        pl(self.idnumber, self.idnumber_plh)
        pl(self.address1, self.address1_plh)
        pl(self.website, self.website_plh)
        pl(self.phone1, self.phone1_plh)
        pl(self.phone2, self.phone2_plh)
        pl(self.mail, self.mail_plh)


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
        if n == None:
            return
        # show loading bar
        self.message(progressbar=2, bg="orange", text = "Loading")
        
        def proces():
            try:
                # crop face with face_crop script it will return the path where the face was saved
                path = Crop().crop(image=n.name)
                # the next code resize the selected image with pillow and show in the button
                img = Image.open(path)
                img = img.resize((135, 150))
                # make compatible with tkinter
                imgtk = ImageTk.PhotoImage(image=img)
                # configure the image in tkinter button
                self.bt_addimage.imgtk = imgtk
                self.bt_addimage.configure(image=imgtk, relief="ridge", borderwidth=5)
                # save path
                self.new_picture_path = (path)
            except:
                raise
            finally:
                # destroy loading dialog
                self.msg.destroy()
        p = Thread(target=proces)
        p.start()


    def addperson(self):
        # if no picture added or not name added show message and return
        if self.new_picture_path == "" or self.firtname.get()==self.firtname_plh or self.lastname.get()==self.lastname_plh:
            self.message(
                text="\nImage and full\nname required",
                bg="orange",
                fg='white'
                )
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
        info['website'] = self.website.get()
        info['phone1'] = self.phone1.get()
        info['phone2'] = self.phone2.get()
        info['mail'] = self.mail.get()
        info['comment'] = self.comment.get(1.0,9.0)
        # add alert options
        info['alert'] = self.alert_var.get()
        info['play_sound'] = self.play_sound_var.get()
        if self.run_file_on_alert.get():
            info['open_file'] = self.alarm_file_path
        else:
            info['open_file'] = ''
        info['send_email'] = self.email_var.get()
        info['send_message'] = self.mobile_message_var.get()


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
        if info['website'] == self.website_plh:
            info['website'] = ""
        if info['phone1'] == self.phone1_plh:
            info['phone1'] = ""
        if info['phone2'] == self.phone2_plh:
            info['phone2'] = ""
        if info['mail'] == self.mail_plh:
            info['mail'] = ""
        if info['comment'] == self.comment_plh+"\n":
            info['comment'] = ""


            
        # encode the image on a separate process and wait to get the result if return 0 all correct, if return 1 is error.
        # we need to send the image path to endode and also send the user info, its in the dictionary.
        def process():
            self.bt_addperson["state"]="disabled"
            result_path = myscan.encode_image(self.new_picture_path, info)
            if result_path:
                # make mini card
                Minicard(
                    image="./media/minicard.png",
                    face=self.new_picture_path,
                    output=f"./{result_path}/thumbnail card.png",
                    text_list=[
                        info["name"] + " " + info["lname"],
                        "BORN : " + info["day"] +"/"+ info["month"] +"/"+ info["year"],
                        "Gender : " + info["gender"],
                        "ID : " + info["id"],
                        "JOB : " + info["job"],
                        "LOC : " + info["country"],
                        "      " + info["city"],
                        "TEL : " + info["phone1"],
                        info["mail"],
                        info["address1"],
                        ],
                    )
                # make card
                Makecard(
                    image="./media/card.png",
                    face=self.new_picture_path,
                    output=f"./{result_path}/card.png",
                    text_list=[
                        info['id'],
                        info['phone1'],
                        info['phone2'],
                        info['name'] + ' ' + info['lname'],
                        info['day'] +'/'+ info['month'] +'/'+ info['year'],
                        info['country'],
                        info['city'],
                        info['gender'],
                        info['job'],
                        info['website'],
                        info['mail'],
                        info['address1'],
                        ]
                    )

                # show message and change some vars
                self.message(
                    text="\n\nprocessed correct",
                    font="arial 20",
                    height=6,
                    bg="gray",
                    fg="#00ff00"
                    )
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
                self.message(
                    text="Error encoding \nthe image file\n please use \nanother image",
                    font="arial 20",
                    height=6,
                    bg="red",
                    fg="white")
                self.soundeffect("error")
            self.bt_addperson["state"]="normal"
            
            
        p = Thread(target=process)
        p.start()


    # ----------- bind funtions for entry ----------------
    # this make the placeholder text hide or show when mouse is over 
    # the funtion receive 3 args: event, entry and the placeholder
    # on enter if the entry text is the placeholder delete text, on leave if entry is empty put the placeholder text.    
                
    def bind_entry(self, event, placeholder):
        # on enter event, change color and check if entry have placeholder to delete.
        if "Enter" in str(event):
            event.widget.configure(bg="#00ffff", fg="black")
            if event.widget.get() == placeholder:
                event.widget.delete(0,"end")
        else:
            # on leave event, if entry is empty put placeholder and change color to default,
            # but if the user write some text it will chage the entry bg to green.
            if event.widget.get() == "":
                event.widget.insert(0, placeholder)
                event.widget.configure(bg="#009999", fg="yellow")
                window.focus()
            else:
                event.widget.configure(bg="#00cc00",fg="black")



    
    def pickup_alarm_file(self,*event):
        self.soundeffect("click")
        # if the checkbox is already true return
        if self.run_file_on_alert.get():
            
            return
        # if checkbox is false pickup the file path to open when a person marked as wanted is recognized.
        n = filedialog.askopenfile(title="Select the file to open if the person is detected")
        try:
            # save file path and set checkbox to True
            self.alarm_file_path = (n.name)
            self.run_file_on_alert.set(True)
        except:
            self.alarm_file_path = ""
            self.run_file_on_alert.set(False)
            





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
        self.website.delete(0,"end")
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
        self.website.insert(0, self.website_plh)
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
        self.website.configure(bg="#009999", fg="yellow")
        self.phone1.configure(bg="#009999", fg="yellow")
        self.phone2.configure(bg="#009999", fg="yellow")
        self.mail.configure(bg="#009999", fg="yellow")
        # set default image to button, delete picture path and reset all vars.
        self.new_picture_path = ""
        self.bt_addimage.configure(image=self.file_img, borderwidth=0)
        self.delete_previus_profile = False
        # disable alert options
        if self.alert_var.get():
            self.alert_chbox.invoke()
        self.play_sound_var.set(False)
        self.run_file_on_alert.set(False)
        self.alarm_file_path = ''
        self.email_var.set(False)
        self.mobile_message_var.set(False)
        
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
        website = Entry(f, width=22,bg="#009999",fg="yellow", font="arial 10",relief="sunken",borderwidth=5)
        phone1 = Entry(f, width=22,bg="#009999",fg="yellow", font="arial 10",relief="sunken",borderwidth=5)
        phone2 = Entry(f, width=22,bg="#009999",fg="yellow", font="arial 10",relief="sunken",borderwidth=5)
        mail = Entry(f, width=22,bg="#009999",fg="yellow", font="arial 10",relief="sunken",borderwidth=5)
        alert = ttk.Combobox(f, values=("True","False","Any"))
        alert.set(value="Any")
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
        Label(f, text="website", bg="#004444", fg="yellow").grid(row=9, column=0)
        Label(f, text="Phone     ", bg="#004444", fg="yellow").grid(row=10, column=0)
        Label(f, text="Phone 2   ", bg="#004444", fg="yellow").grid(row=11, column=0)
        Label(f, text="Email     ", bg="#004444", fg="yellow").grid(row=12, column=0)
        Label(f, text="Alert   ", bg="#004444", fg="yellow").grid(row=13, column=0)
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
        website.grid(row=9, column=1)
        phone1.grid(row=10, column=1)
        phone2.grid(row=11, column=1)
        mail.grid(row=12, column=1)
        alert.grid(row=13, column=1)
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
            info['website'] = website.get()
            info['phone1'] = phone1.get()
            info['phone2'] = phone2.get()
            info['mail'] = mail.get()
            # if true selected, add true to the dictionary to find if any wanted value is true in profile list.
            if alert.get() == "True":
                info['alert'] = "true"
            # if false selected, add "false" to find the string in users profiles.
            if alert.get() == "False":
                info['alert'] = "false"
                
            
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
            
    def message(self, text="", font="arial 20", height=5, bg="yellow", fg="black", progressbar=False):
        self.msg = Toplevel()
        self.msg.geometry("300x200+500+300")
        self.msg.wm_attributes("-alpha",0.8)
        self.msg.overrideredirect(True)
        # use label with a image as background
        Label(self.msg, image=self.warning_img, bg=bg,).pack()
        # create frame container
        box = Frame(self.msg, width=276, height=160, bg=bg)
        box.pack_propagate(False)
        box.place(x=11, y=18)
        # show general messages dialog in a label inside of the frame
        Label(box, text=text, font=font, bg=bg, fg=fg).pack(fill='both')

        if progressbar == 1:
            self.progressbar = ttk.Progressbar(self.msg, length=200)
            self.progressbar.place(x=45,y=130)
        if progressbar == 2:
            self.progressbar = ttk.Progressbar(self.msg, length=200)
            self.progressbar.start(interval=1)
            self.progressbar.place(x=45,y=130)
            self.msg.grab_set()
            return
            
        def ok():
            self.stop_alarm = True
            self.msg.destroy()

        Button(self.msg, text="X",command=ok, bg="red", fg="white", activebackground="red", font="arial 12",width=2).place(x=270,y=5)
        self.msg.grab_set()





    def bind_button(self, event, image):
        # if the button add image have the person picture will not change on mouse over.
        if event.widget == self.bt_addimage:
            if self.new_picture_path != "":
                return
        # on enter event, change color and check if entry have placeholder to delete.
        if "Enter" in str(event):
            event.widget.configure(image=image)         
        else:
            event.widget.configure(image=image)
            
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
window.title("Face Recognition System V 1.3.4")

window.mainloop()



        

