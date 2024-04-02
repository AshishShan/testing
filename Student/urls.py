from django.contrib import admin
from django.urls import re_path, include
from . import views

 

urlpatterns = [
    re_path("",views.index,name="studenthome"),          
    re_path("gatepass/",views.gatepass,name="gatepass"),
    re_path("show_gatepass/",views.show_gatepass,name="show_gatepass"),
    re_path("leave/",views.leave,name="leave"),
    re_path("login/",views.login,name="login"),
    re_path("logout/",views.logout,name="logout"),
    re_path("complaint/",views.complaint,name="complaint"),
    re_path("show_complaint/",views.show_complaint,name="show_complaint"),
    re_path("change_password/",views.change_password,name="change_password"),
    re_path("complaint/<int:pk>/", views.disable_complaint, name="disable_complaint" )
    # path("gatepass/<int:pk>/", views.disable_gatepass, name="disable_gatepass" )

]
