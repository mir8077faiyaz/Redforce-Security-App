from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='loginpage'),
    path('home/', views.home, name='homepage'),
    path('setUpProfile/', views.setUpProfile, name='setUpProfile'),
    path('faceRecog/', views.faceRecog, name='faceRecog'),
    #path('face_recog', views.faceRecog, name='face_recog'),
]
