from django.shortcuts import render, redirect
from mysite.settings import EMAIL_HOST_USER
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import auth, User
from django.contrib import messages
from django.core.mail import send_mail
from .models import todoview
from django.contrib.auth.decorators import login_required
import random
from win10toast import ToastNotifier

# Create your views here.


@login_required(login_url="login")
def addtodo(request):
    if request.method == "POST":
        x = request.session["sname"]
        cont = request.POST["cont"]
        if cont != "":
            if todoview.objects.filter(cont=cont, name=x).exists():
                return redirect("addtodo")
            else:
                s = todoview(cont=cont, name=x)
                s.save()
                list = todoview.objects.filter(name=x)
                messages.info(request, x)
                return render(request, "todo1.html", {"list": list})
        else:
            list = todoview.objects.filter(name=x)
            messages.info(request, x)
            return render(request, "todo1.html", {"list": list})
    else:
        if request.session["sname"]:
            x = request.session["sname"]
            list = todoview.objects.filter(name=x)
            messages.info(request, x)
            return render(request, "todo1.html", {"list": list})
        else:
            return redirect("login")


@login_required(login_url="login")
def delete(request, id):
    s = todoview.objects.get(id=id)
    s.delete()
    return redirect("addtodo")


def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            toast = ToastNotifier()
            toast.show_toast(
                "The ToDo Website",
                "We have recieved a request to login in your account!",
                duration=5,
            )
            request.session["sname"] = username
            return redirect("addtodo")
        else:
            user1 = User.objects.get(username=username)
            if user1 is not None:
                messages.info(request, "Incorrect Password")
                return render(request, "login.html")
            else:
                messages.info(request, "YOU HAVENOT REGISTERED YET")
                return render(request, "registertodo.html")
    else:
        if request.session.has_key("sname"):
            return redirect("addtodo")
        else:
            return render(request, "login.html")


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        passw = request.POST["password"]
        passw1 = request.POST["password1"]
        email = request.POST["email"]
        if passw == passw1:
            if User.objects.filter(username=username).exists():
                messages.info(request, "username is already taken")
                return render(request, "registertodo.html")
            else:
                user = User.objects.create_user(
                    username=username, password=passw, email=email
                )
                user.save()
                return render(request, "login.html")
        else:
            messages.info(request, "wrong password")
            return render(request, "registertodo.html")

    else:
        return render(request, "registertodo.html")


@login_required(login_url="login")
def logout(request):
    auth.logout(request)
    return render(request, "login.html")


def email_confirm(request):
    return render(request, "password.html")


def send_otp(request):
    if request.method == "POST":
        s = random.randint(111111, 999999)
        gmail = request.POST["gmail"]
        if User.objects.filter(email=gmail).exists():
            subject = "Email Verification"
            otp = str(s)
            message = (
                "We have recievd a request for changing your password.Here is the 6-digit OTP  "
                + otp
                + "  Enter the otp to change password.Ignore if its not You.Keep this OTP confidential"
            )
            send_mail(subject, message, EMAIL_HOST_USER, [gmail], fail_silently=False)
            return render(request, "confirmation.html", {"otp": s})
        else:
            return HttpResponse("you havenot registered with this gmail")


def confirmation(request):
    return render(request, "reset_password.html")


def reset_password(request):
    if request.method == "POST":
        gmail = request.session["gmail"]
        user = User.objects.get(email=gmail)
        password = request.POST["password1"]
        user.set_password(password)
        user.save()
        return render(request, "login.html")
