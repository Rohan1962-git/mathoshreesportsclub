import datetime

import random
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render
from .models import User, Book_Turf,Admin,Event


# Create your views here.
def index(request):
    return render(request,"index.html")


def about(request):
   return render(request,"about.html")

def user_reg(request):
    return render(request,"user_reg.html")

def user_test(request):
    if request.method=='POST':
        name = request.POST.get("uname")
        email = request.POST.get("email")
        gender = request.POST.get("gender")
        password = request.POST.get("password")
        contact = request.POST.get("contact")
        record = User(name=name,email=email, gender=gender, password=password, contact=contact)
        record.save()
        return render(request, "user_login.html")

def user_login(request):
    if 'u_name' in request.session:
        param = {'name': request.session.get("a=u_name")}
        return render(request, "userhome.html", param)
    return render(request, "user_login.html")
def user_check(request):
    if request.method == 'POST':
        uname=request.POST.get("uname")
        password=request.POST.get("password")
        try:
            user=User.objects.get(name=uname)
            if user.password==password:
                request.session['u_name']=uname

                return userhome(request)
            else:
                param = {"msg": "password is wrong..."}
                return render(request, "user_login.html", param)



        except Exception as e:
            param={"msg":"This username is not exist..."}
            return render(request,"user_login.html",param)

def userhome(request):
    if 'u_name' in request.session:
        uname = request.session.get("u_name")
        param = {"name": uname}
        return render(request, "userhome.html", param)
    else:
        param={"status":"you first neeed to login"}
        return render(request,"user_login",param)

def ground_booking(request):
    if 'u_name' in request.session:
        param={'date':datetime.date.today}
        return render(request,"ground_booking.html",param)

    else:
        param={'status':"you need to login..."}
        return render(request,"user_reg",param)

def data_ground_booking(request):
    if request.method == 'POST':
        date=request.POST.get("date")
        time=request.POST.get("time")
        try:
            book = Book_Turf.objects.get(date=date)
            param = {'status': 'Please select other date...'}
            return render(request, "ground_booking.html", param)
        except Exception as e:
            user=User.objects.get(name=request.session.get("u_name"))
            book=Book_Turf(uid=user.uid,name=user,date=date,time=time,mobile=user.contact)
            book.save()
            param={'status':'Booking successful..'}
            return render(request,"userhome.html",param)
        else:
            param={"msg":"Something wrong"}
            return render(request,"ground_booking.html",param)

def admin_login_page(request):
    if 'a_name' in request.session:
        param = {'name': request.session.get("a_name")}
        return render(request, "adminhome.html", param)
    return render(request, "admin_login.html")




def admin_check(request):
    if request.method == 'POST':
        aname = request.POST.get("aname")
        password = request.POST.get("password")
        try:
            ad =Admin.objects.get(name=aname)

            if ad.password == password:
                request.session['a_name'] = aname

                return adminhome(request)
            else:
                param = {"msg": "password is not exists..."}
                return render(request, "admin_login.html", param)
        except Exception as e:
            param={"msg":"This username doesnot exist.."}
            return render(request,"admin_login.html",param)

def adminhome(request):
    if 'a_name' in request.session:
        aname = request.session.get("a_name")
        param = {"name": aname}
        return render(request,"adminhome.html",param)

    else:
        param = {"status": "you first need to login"}
        return render(request, "user_login", param)

def admin_booking(request):
    if 'a_name' in request.session:
        booking = Book_Turf.objects.all()
        param={'data':booking}
        return render(request,"admin_booking.html",param)
    else:
        param = {'status': "You Need to login...."}
        return render(request,"admin_login.html",param)


def admin_event(request):
    if 'a_name' in request.session:
        event=Event.objects.all()
        param={'data':event}
        return render(request,"admin_event.html",param)
    else:
        param = {'status': "You Need to login...."}
        return render(request, "admin_login.html", param)

def add_event(request):
    if 'a_name' in request.session:
        param = {'date': datetime.date.today}
        return render(request,"add_event.html",param)
    else:
        param = {'status': "You Need to login...."}
        return render(request, "admin_login.html", param)


def db_add_event(request):
    if request.method=='POST':
        ename=request.POST.get("ename")
        edate=request.POST.get("edate")
        etime=request.POST.get("etime")
        eduration=request.POST.get("eduration")

        event=Event(name=ename,date=edate,time=etime,duration=eduration)
        event.save()
       # request.session['event_status']="Event Added Succesfully.."
        return admin_event(request)
    else:
        return admin_event(request)

def admin_logout(request):
    if 'a_name' in request.session:
        del request.session['a_name']
        return render(request, "admin_login.html",)


    else:
        param = {'status':"YoU need to login "}
        return render(request,"admin_login.html",param)


def user_logout(request):
    if 'u_name' in request.session:
        del request.session['u_name']
        return render(request, "user_login.html", )


    else:
        param = {'status': "YoU need to login "}
        return render(request, "user_login.html", param)

def show_event(request):
    if 'u_name' in request.session:
        event = Event.objects.all()
        param = {'data': event}
        return render(request, "show_event.html", param)
    else:
        param = {'status': "You Need to login...."}
        return render(request, "user_login.html", param)
def event_delete(request):
    id = request.GET.get("eid")
    Event.objects.filter(eid=id).delete()
    return admin_event(request)

def mail_send(request):
    return render(request,"email_form.html",)


def email_check(request):
    email=request.POST.get("email")
    subject="Forget password"
    otp=random.randint(1000,9999)
    msg="OTP:"
    msg+=str(otp)
    email_from=settings.EMAIL_HOST_USER
    to=(email,)
    send_mail(subject,msg,email_from,to)
    param={"otp":otp,"email":email}
    return render(request,"enter_otp.html",param)


def otp_check(request):
    myotp=request.POST.get("myotp")
    emailid=request.POST.get("emailid")
    otp=request.POST.get("otp")
    if(myotp==otp):
        param={"email":emailid}
        return render(request,"update_pass.html",param)
    else:
        param={"otp":myotp,"email":emailid,"msg":"wrong Otp"}
        return render(request,"enter_otp.html",param)

def update_pass(request):
     password = request.POST.get("password")
     myemail = request.POST.get("emailid")
     user = User.objects.get(email=myemail)
     user.password = password
     user.save()
     return render(request, "user_login.html")
































