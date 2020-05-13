from django.contrib import admin
from django.urls import path
from todolist import views

urlpatterns = [
    path('',views.login,name='login'),
    path("login",views.login,name='login'),
    path("addtodo",views.addtodo,name='addtodo'),
    path("delete<int:id>",views.delete,name='delete'),
    path("register",views.register,name='register'),
    path("logout",views.logout,name='logout'),
    path("email_confirm",views.email_confirm,name="email_confirm"),
    path("send_otp",views.send_otp,name="send_otp"),
    path("reset_password",views.reset_password,name="reset_passsword"),
    path("confirmation",views.confirmation,name="confirmation")
]
