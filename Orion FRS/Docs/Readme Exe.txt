
* * * Orion Face Recognition System * * *
Its a software that provides features for facial recognition using AI (Artificial Inteligency).
if you like please contribute with a small donation.

_________________________________________________

FUNCTION AVAILABLE IN THE LAST RELEASE
--------------------------------------
> Add new person profile to the data base.
> List all person profiles that are in data base.
> Find profiles with the filter feature.
> Edit Delete and update profiles.
> Recognize persons from a picture.
> Recognize persons from multifiles with few faces using hog algorithm.
> Recognize persons using the webcam.
> Mark person as wanted to play alarm when its recognized.
> Mark person as wanted to open a custom file  when its recognized.
> Log of previous recognized persons.
> Futuristic design with Visual effects and sound effects.
> email and messages alert feature
_________________________________________________

License: MIT
Copyright (c) 2021-2022 Erick Esau Martinez
Programing Language: Python3
Platform: Windows
Web www.erickesau.wordpress.com

https://www.paypal.com/paypalme/erickesau0
Email: martinezesau90@gmail.com
https://github.com/Erickesau
Personal spanish blog Outdated www.erickesau.blogspot.com

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




EMAIL ALERT:
    1 create google gmail account
    2 goto google security settings and enable 2 step autentication
    3 you will get the option to create a google app pass (select create a pass for other)
    4 in orion setting fill the field with the gmail address and google app pass. (personal password will not work please generate google app pass)

MESSAGES ALERT:
    1 goto www.twilio.com and create account.
    2 get a free twilio phone number.
    3 goto caller ID and register your personal phone (free accounts can not send messages to unregistered phones)
      if you buy a twilio plan you can send messages to everybody without register the number.
    4 goto orion setting fill the field with twilio api sid, api token and virtual number.
______________________________________________

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