from django.urls import path
from . import views
blog_namespace = "myblog"
urlpatterns = [
    path('', views.login, name='loginpage'),

]
