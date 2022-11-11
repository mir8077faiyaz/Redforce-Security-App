from django.shortcuts import render
from django.http import HttpResponse
import sys
import cv2
from django.template import RequestContext
from .models import UserInfo, TestUser
import face_recognition
import base64
import os
from django.shortcuts import redirect
from django.contrib.auth import logout as auth_logout
from django.shortcuts import render
from rforce import models
import requests
import json
count = 0
stop = 0
anti="pika"
# Create your views here.
def login(request):
    auth_logout(request)
    return render(request,'index.html')

def home(request):
    return render(request,'home.html')

def setUpProfile(request):
    global stop
    if (stop==1):
        return redirect(f"/faceRecog/")
    user = request.user
    print(user)
    alluser =  models.UserInfo.objects.filter()
    print(alluser)
    list = []
    list.append(alluser)
    

    for i in alluser:
        if(user==i.user):
            return redirect(f"/faceRecog/")
        
        
    if request.method=="POST":
        user=UserInfo.objects.create(
        img=request.POST.get("img_data"),
        user = request.user,
        
        )
        stop = 1
        return redirect(f"/faceRecog/")
      
    return render(request,'setUpProfile.html')

def faceRecog(request):
    if request.method=="POST":
        test=TestUser.objects.create(
        img=request.POST.get("img_data"),
        user = request.user
        )
        global anti 
        anti= request.POST.get("img_data2")
        global stop
        stop=0
        
    
        return redirect(f"/check/")
    return render(request,'faceRecog.html')



def check(request):
   
    db = UserInfo.objects.get(user=request.user)
    db_img=db.img
    dbu=db.user
    print("1")
    
    
    db1 = TestUser.objects.get(user=request.user)
    db_img1=db1.img
    dbu1=db1.user
    print("2")
    
    with open(f"{dbu}.jpg", "wb") as fh:
        fh.write(base64.b64decode(db_img))
    
    try:       
        known_image = face_recognition.load_image_file(f"{dbu}.jpg")
        known_encoding = face_recognition.face_encodings(known_image)[0]
        print("3") 
        #Anti-spoofing starts here

        url = "https://liveness-detection1.p.rapidapi.com/api/v1/liveness-detection"

        payload = {
            "imageUrl":anti,
            "isface": True
        }
        headers = {
            "content-type": "application/json",
            "X-RapidAPI-Key": "a5c157836emshff1b311d2ca4376p103370jsn6c6d66b82114",
            "X-RapidAPI-Host": "liveness-detection1.p.rapidapi.com"
        }

        response = requests.request("POST", url, json=payload, headers=headers)
        data = response.json()
        print(type(data))
        keys = data.keys()
        print(keys)
        print(type(data['predict']))

        print(response.text)
        #Anti-Spoofing ends here
        with open(f"{dbu1}.jpg", "wb") as fk:
            fk.write(base64.b64decode(db_img1))
        unknown_image = face_recognition.load_image_file(f"{dbu1}.jpg")

        
        unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
        print("4") 
    
        results = face_recognition.compare_faces([known_encoding], unknown_encoding,tolerance=0.45)
        print(results)

        f = open(f"{dbu}.jpg", 'w')
        f.close()
        os.remove(f.name)
        
        f1 = open(f"{dbu1}.jpg", 'w')
        f1.close()
        os.remove(f1.name)

        #removing test-user
        instance =TestUser.objects.get(user=request.user)
        instance.delete()
        stresult = str(results)
        global count
        
        if (stresult == "[True]" and data['predict']=="real"):
        
            return redirect(f"/home/")          
        else:
            count=count+1
            print(count)
            if(count==3):
                count = 0
                return redirect(f"/logout/")
            else:
                return redirect(f"/faceRecog/")
    except:
        #global count2
        count=count+1
        
        print("An exception occurred")   
        f1 = open(f"{dbu1}.jpg", 'w')
        f1.close()
        os.remove(f1.name)
        instance =TestUser.objects.get(user=request.user)
        instance.delete()
        if(count==3):
            count=0
            return redirect(f"/logout/")
        else:
            return redirect(f"/faceRecog/")
     


def logout(request):
    """Logs out user"""
    auth_logout(request)
    #return render('index.html', {}, RequestContext(request))   
    return render(request,'index.html')    
    
    

   






