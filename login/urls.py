
from django.urls import path,include

import login
from login import views
#配置url

urlpatterns = [

    path('login',views.login),
    path('logout',views.logout),
    path('register',views.register),

]
