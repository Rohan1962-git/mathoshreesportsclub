from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import logout
from .models import CustomUser, Book_Turf, Admin, Event
from django.core.mail import send_mail
from django.conf import settings


# Home page
def index(request):
    return render(request, "index.html")

def about(request):
    return render(request, "about.html")

# User Registration
def user_reg(request):
    return render(request, "user_reg.html")

def user_test(request):
    if request.method == "POST":
        name = request.POST["name"]
        email = request.POST["email"]
        gender = request.POST["gender"]
        password = request.POST["password"]
        contact = request.POST["contact"]

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect("user_reg")

        CustomUser.objects.create(
            name=name,
            email=email,
            gender=gender,
            password=password,
            contact=contact
        )
        messages.success(request, "Registration successful")
        return redirect("user_login")
    return redirect("user_reg")


# User Login
def user_login(request):
    return render(request, "user_login.html")

def user_check(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        try:
            user = CustomUser.objects.get(email=email, password=password)
            request.session["uid"] = user.uid
            request.session["uname"] = user.name
            return redirect("userhome")
        except CustomUser.DoesNotExist:
            messages.error(request, "Invalid credentials")
            return redirect("user_login")
    return redirect("user_login")


# User Home
def userhome(request):
    if "uid" not in request.session:
        return redirect("user_login")
    return render(request, "userhome.html")


# User Logout
def user_logout(request):
    logout(request)
    return redirect("index")


# Turf Booking
def ground_booking(request):
    if "uid" not in request.session:
        return redirect("user_login")
    return render(request, "ground_booking.html")

def data_ground_booking(request):
    if request.method == "POST":
        uid = request.session["uid"]
        name = request.POST["name"]
        date = request.POST["date"]
        time = request.POST["time"]
        mobile = request.POST["mobile"]

        Book_Turf.objects.create(
            uid=uid,
            name=name,
            date=date,
            time=time,
            mobile=mobile
        )
        messages.success(request, "Turf booked successfully")
        return redirect("userhome")
    return redirect("ground_booking")


# Admin Login
def admin_login_page(request):
    return render(request, "admin_login.html")

def admin_check(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        try:
            admin = Admin.objects.get(email=email, password=password)
            request.session["admin_id"] = admin.id
            request.session["admin_name"] = admin.name
            return redirect("admin_booking")
        except Admin.DoesNotExist:
            messages.error(request, "Invalid admin credentials")
            return redirect("admin_login_page")
    return redirect("admin_login_page")


# Admin Pages
def admin_booking(request):
    if "admin_id" not in request.session:
        return redirect("admin_login_page")
    bookings = Book_Turf.objects.all()
    return render(request, "admin_booking.html", {"bookings": bookings})

def admin_event(request):
    if "admin_id" not in request.session:
        return redirect("admin_login_page")
    events = Event.objects.all()
    return render(request, "admin_event.html", {"events": events})

def add_event(request):
    return render(request, "add_event.html")

def db_add_event(request):
    if request.method == "POST":
        name = request.POST["name"]
        date = request.POST["date"]
        time = request.POST["time"]
        duration = request.POST["duration"]

        Event.objects.create(
            name=name,
            date=date,
            time=time,
            duration=duration
        )
        messages.success(request, "Event added successfully")
        return redirect("admin_event")
    return redirect("add_event")

def event_delete(request):
    if "admin_id" not in request.session:
        return redirect("admin_login_page")

    eid = request.GET.get("eid")
    Event.objects.filter(eid=eid).delete()
    messages.success(request, "Event deleted successfully")
    return redirect("admin_event")

def admin_logout(request):
    logout(request)
    return redirect("index")


# Event for Users
def show_event(request):
    events = Event.objects.all()
    return render(request, "show_event.html", {"events": events})


# Forgot Password (OTP)
def mail_send(request):
    return render(request, "mail_send.html")

def email_check(request):
    if request.method == "POST":
        email = request.POST["email"]
        try:
            user = CustomUser.objects.get(email=email)
            otp = "1234"  # (replace with random generator in future)
            request.session["otp"] = otp
            request.session["reset_email"] = email

            send_mail(
                "Password Reset OTP",
                f"Your OTP is {otp}",
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            messages.success(request, "OTP sent to your email")
            return redirect("otp_check")
        except CustomUser.DoesNotExist:
            messages.error(request, "Email not found")
            return redirect("mail_send")
    return redirect("mail_send")

def otp_check(request):
    if request.method == "POST":
        otp = request.POST["otp"]
        if otp == request.session.get("otp"):
            return redirect("update_pass")
        else:
            messages.error(request, "Invalid OTP")
            return redirect("otp_check")
    return render(request, "otp_check.html")

def update_pass(request):
    if request.method == "POST":
        password = request.POST["password"]
        email = request.session.get("reset_email")
        CustomUser.objects.filter(email=email).update(password=password)
        messages.success(request, "Password updated successfully")
        return redirect("user_login")
    return render(request, "update_pass.html")
