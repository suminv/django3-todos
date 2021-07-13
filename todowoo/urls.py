from django.contrib import admin
from django.urls import path
from todo import views


urlpatterns = [
    path('admin/', admin.site.urls),
    #Auth
    path('signup/', views.signupuser, name='signupuser'),
    #Logout
    path('logout/', views.logoutuser, name='logoutuser'),
    path('login/', views.loginuser, name='loginuser'),
    
    # TOdos
    path('current/', views.currenttodos, name='currenttodos'),
    path('create', views.createtodo
    , name='createtodo'),

    # Home page
    path('', views.home, name='home'),
]   


