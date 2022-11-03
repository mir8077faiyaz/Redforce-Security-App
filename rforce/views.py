from django.shortcuts import render
from django.http import HttpResponse
import sys
import cv2
from .models import UserInfo
# Create your views here.
def login(request):
    return render(request,'index.html')

def home(request):
    return render(request,'home.html')

def setUpProfile(request):
    if request.method=="POST":
        user=UserInfo.objects.create(
        img=request.POST.get("img_data"),
        )
    return render(request,'setUpProfile.html')



