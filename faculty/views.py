from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib.auth import authenticate, login as loginn
from django.contrib.auth import logout as logout_view
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_str  # Use force_str instead of force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.urls import reverse
from django import template
from .utils import generate_token
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib.auth import authenticate, login as loginn
from django.contrib.auth import logout as logout_view
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_str  # Use force_str instead of force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.urls import reverse
from django import template
from .utils import generate_token
from django.conf import settings
from .demo import EMAIL_HOST_USER
from student.models import Gatepass
from operator import *
import json

# Create your views here.
def index(request):
    return render(request, 'faculty/index.html')

# ... (rest of your views with corrected force_str import)

def complaint(request):
    if(request.user.userprofile.warden==True):
        return render(request,'faculty/complaints.html')
    else:
        return render(request,'faculty/error_page.html')
def gatepass(request):
    if(request.user.userprofile.warden==True):
        return render(request,'faculty/gatepass.html')
    else:
        return render(request,'faculty/error_page.html')

def main_gate(request):
    if(request.user.userprofile.main_gate==True):
        if request.method=="POST":
            roll = request.POST.get('roll', '')
            try:
                order = Gatepass.objects.filter(roll=roll,active=True,left_gate=False)
                count = 0
                if len(order)>0:
                    updates = []
                    for item in reversed(order):
                        if(count<5):
                            count = count +1
                            updates.append({'name': item.student_name, 'email': item.student_email,'hostel':item.hostel,'roll':item.roll,'date_out':item.date_out,'date_in':item.date_in,'room':item.room,'reason':item.reason,'address':item.address,'s_contact':item.s_contact,'p_contact':item.p_contact,'items':item.items,'supervisor':item.approved_supervisor,'guard':item.approved_guard,'control_room':item.approved_control_room})
                            response = json.dumps({"status":"success", "updates": updates}, default=str)
                        else:
                            break
                    return HttpResponse(response)
                else:
                    return HttpResponse('{"status":"nogatepass"}')
            except Exception as e:
                return HttpResponse('{"status":"error"}')

        return render(request, 'faculty/main_gate.html')
    else:
       return render(request,'faculty/error_page.html')
@login_required
def register(request):
    if(request.user.userprofile.warden==True):
        if request.method=="POST":
            student_name = request.POST.get('name', '')
            student_email = request.POST.get('email', '')
            password = request.POST.get('password', '')
            hostel = request.POST.get('hostel', '')
            address = request.POST.get('address', '')
            s_contact = request.POST.get('scontact', '')
            p_contact = request.POST.get('pcontact', '')
            image = request.POST.get('image','')
            enrollment_no = request.POST.get('enroll','')
            gender = request.POST.get('gender','')
            room_no = request.POST.get('room','')
            course = request.POST.get('course','')
            roll_no = request.POST.get('roll','')
            user = User.objects.create_user(username=student_email,email=student_email,password=password,first_name=student_name,last_name='student')
            user.is_active = False
            profile = user.userprofile
            profile.hostel=hostel
            profile.address=address
            profile.contact=s_contact
            profile.p_contact=p_contact
            profile.image=image
            profile.enroll=enrollment_no
            profile.gender=gender
            profile.room=room_no
            profile.applied_for_member=True
            profile.student=True
            profile.course=course
            profile.roll=roll_no
            profile.save()
            user.save()
            
            thank = True
            mail_subject = 'IIITM Hostel Management'
            message=render_to_string('faculty/register_apply.html',{'user': user,'reference_name' : student_email ,'domain': '127.0.0.1:8000','uid': urlsafe_base64_encode(force_bytes(user.pk)),'token': generate_token.make_token(user),})
            email=EmailMessage(mail_subject,message,settings.EMAIL_HOST_USER,[student_email])
            email.send()
            return HttpResponse("email sent")
            return render(request, 'faculty/register.html',{'thank':thank})
        else:
            return render(request,"faculty/register.html")
    else:
       return render(request,'faculty/error_page.html')

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and generate_token.check_token(user, token):
        profile = user.userprofile
        profile.is_member = True
        user.is_active = True
        profile.save()
        user.save()
        loginn(request, user)
        return HttpResponse('Thank you for your confirmation')
    else:
        return HttpResponse('link is invalid! or You have already confirmed!!')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            loginn(request, user)

            if user.is_active:
                loginn(request, user)
                
                return render(request,"faculty/index.html")
            else:
                HttpResponse("Inactive User.")
                return redirect("facultyhome")
        else:
            return render(request,"faculty/login.html")
    else:
        return render(request,"faculty/login.html")

@login_required
def logout(request):
    logout_view(request)
    return redirect("facultyhome")

from student.models import Gatepass
from operator import *
import json

# Create your views here.
def index(request):
    return render(request, 'faculty/index.html')

# ... (rest of your views with corrected force_str import)

def complaint(request):
    if(request.user.userprofile.warden==True):
        return render(request,'faculty/complaints.html')
    else:
        return render(request,'faculty/error_page.html')
def gatepass(request):
    if(request.user.userprofile.warden==True):
        return render(request,'faculty/gatepass.html')
    else:
        return render(request,'faculty/error_page.html')

def main_gate(request):
    if(request.user.userprofile.main_gate==True):
        if request.method=="POST":
            roll = request.POST.get('roll', '')
            try:
                order = Gatepass.objects.filter(roll=roll,active=True,left_gate=False)
                count = 0
                if len(order)>0:
                    updates = []
                    for item in reversed(order):
                        if(count<5):
                            count = count +1
                            updates.append({'name': item.student_name, 'email': item.student_email,'hostel':item.hostel,'roll':item.roll,'date_out':item.date_out,'date_in':item.date_in,'room':item.room,'reason':item.reason,'address':item.address,'s_contact':item.s_contact,'p_contact':item.p_contact,'items':item.items,'supervisor':item.approved_supervisor,'guard':item.approved_guard,'control_room':item.approved_control_room})
                            response = json.dumps({"status":"success", "updates": updates}, default=str)
                        else:
                            break
                    return HttpResponse(response)
                else:
                    return HttpResponse('{"status":"nogatepass"}')
            except Exception as e:
                return HttpResponse('{"status":"error"}')

        return render(request, 'faculty/main_gate.html')
    else:
       return render(request,'faculty/error_page.html')
@login_required
def register(request):
    if(request.user.userprofile.warden==True):
        if request.method=="POST":
            student_name = request.POST.get('name', '')
            student_email = request.POST.get('email', '')
            password = request.POST.get('password', '')
            hostel = request.POST.get('hostel', '')
            address = request.POST.get('address', '')
            s_contact = request.POST.get('scontact', '')
            p_contact = request.POST.get('pcontact', '')
            image = request.POST.get('image','')
            enrollment_no = request.POST.get('enroll','')
            gender = request.POST.get('gender','')
            room_no = request.POST.get('room','')
            course = request.POST.get('course','')
            roll_no = request.POST.get('roll','')
            user = User.objects.create_user(username=student_email,email=student_email,password=password,first_name=student_name,last_name='student')
            user.is_active = False
            profile = user.userprofile
            profile.hostel=hostel
            profile.address=address
            profile.contact=s_contact
            profile.p_contact=p_contact
            profile.image=image
            profile.enroll=enrollment_no
            profile.gender=gender
            profile.room=room_no
            profile.applied_for_member=True
            profile.student=True
            profile.course=course
            profile.roll=roll_no
            profile.save()
            user.save()
            
            thank = True
            mail_subject = 'IIITM Hostel Management'
            message=render_to_string('faculty/register_apply.html',{'user': user,'reference_name' : student_email ,'domain': '127.0.0.1:8000','uid': urlsafe_base64_encode(force_bytes(user.pk)),'token': generate_token.make_token(user),})
            email=EmailMessage(mail_subject,message,settings.EMAIL_HOST_USER,[student_email])
            email.send()
            return HttpResponse("email sent")
            return render(request, 'faculty/register.html',{'thank':thank})
        else:
            return render(request,"faculty/register.html")
    else:
       return render(request,'faculty/error_page.html')

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and generate_token.check_token(user, token):
        profile = user.userprofile
        profile.is_member = True
        user.is_active = True
        profile.save()
        user.save()
        loginn(request, user)
        return HttpResponse('Thank you for your confirmation')
    else:
        return HttpResponse('link is invalid! or You have already confirmed!!')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            loginn(request, user)

            if user.is_active:
                loginn(request, user)
                
                return render(request,"faculty/index.html")
            else:
                HttpResponse("Inactive User.")
                return redirect("facultyhome")
        else:
            return render(request,"faculty/login.html")
    else:
        return render(request,"faculty/login.html")

@login_required
def logout(request):
    logout_view(request)
    return redirect("facultyhome")
