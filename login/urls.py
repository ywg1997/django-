
from django.urls import path,include

import login
from login import views

urlpatterns = [

    path('login',views.login),
    path('logout',views.logout),
    path('register',views.register),

]
