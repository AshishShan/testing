from django.contrib import admin

from django.urls import re_path, include
from . import views


urlpatterns = [
    re_path("",views.index,name="facultyhome"),
    re_path("register/",views.register,name="registerstudent"),
    # path("gatepass/",views.gatepass,name="gatepass"),
    # path("leave/",views.leave,name="leave"),
    re_path("complaint/",views.complaint,name="complaint"),
    re_path("gatepass/",views.gatepass,name="gatepass"),
    re_path("login/",views.login,name="login"),
    re_path("logout/",views.logout,name="logout"),
    re_path("main_gate/",views.main_gate,name="main_gate"),


    re_path(r'^activatemembers/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
]
