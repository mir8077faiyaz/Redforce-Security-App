from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='loginpage'),
    path('home/', views.home, name='homepage'),
    path('setUpProfile/', views.setUpProfile, name='setUpProfile'),
    path('faceRecog/', views.faceRecog, name='faceRecog'),
    path('check/', views.check, name='check'),
    #path('face_recog', views.faceRecog, name='face_recog'),
    path('logout/', views.logout, name='logout'),
    path('upload/', views.upload_basic, name='upload'),
]
