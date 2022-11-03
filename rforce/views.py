from django.shortcuts import render
from django.http import HttpResponse
import sys
import cv2

# Create your views here.
def login(request):
    return render(request,'index.html')

def home(request):
    return render(request,'home.html')

def setUpProfile(request):
    return render(request,'setUpProfile.html')

