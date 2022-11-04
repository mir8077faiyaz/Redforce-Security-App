from django.shortcuts import render
from django.http import HttpResponse
import sys
import cv2
from .models import UserInfo
import face_recognition
import base64
import os
# Create your views here.
def login(request):
    return render(request,'index.html')

def home(request):
    return render(request,'home.html')

def setUpProfile(request):
    if request.method=="POST":
        user=UserInfo.objects.create(
        img=request.POST.get("img_data"),
        user = request.user
        )
        # implementing fcr
        db = UserInfo.objects.get(user=request.user)
        db_img=db.img
        dbu=db.user
        #print(dbu)

        with open(f"{dbu}.jpg", "wb") as fh:
            fh.write(base64.b64decode(db_img))
        #print(db_img)

        known_image = face_recognition.load_image_file(f"{dbu}.jpg")
        unknown_image = face_recognition.load_image_file("mir3.jpg")

        known_encoding = face_recognition.face_encodings(known_image)[0]
        unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

        results = face_recognition.compare_faces([known_encoding], unknown_encoding)
        print(results)
        f = open(f"{dbu}.jpg", 'w')
        f.close()
        os.remove(f.name)
    return render(request,'setUpProfile.html')






