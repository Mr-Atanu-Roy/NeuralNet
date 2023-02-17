from django.shortcuts import render, redirect

from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required

from django.contrib import messages

import datetime
import pytz
from django.conf import settings

# Get the timezone object for the timezone specified in settings.py
tz = pytz.timezone(settings.TIME_ZONE)

# Get the current time in the timezone
current_time = datetime.datetime.now(tz)

from accounts.models import *
from core.models import ChitChat

from .utils import *

from core.prompts import *


# Create your views here.

def login(request):
    if request.session.get('user_email'):
        del request.session['user_email']
        
    if request.user.is_authenticated:
        messages.warning(request, "you are already logged in")
        return redirect('/')
    else:
        try:
            email = password = ""
            context = {
                "email" : email,
                "password" : password
            }
            if request.method == "POST":
                email = request.POST.get("email")
                password = request.POST.get("password")
                
                context["email"] = email
                context["password"] = password
                
                if email != "" and password != "":
                    print("Hello12")
                    checkUser = User.objects.filter(email=email).first()
                    print("Hello")
                    if checkUser:
                        user = auth.authenticate(email = email, password = password)
                        if user is not None:
                            if checkUser.is_verified:
                                auth.login(request, user)
                                messages.success(request, "you are successfully logged in")
                                if request.GET.get('next') != None:
                                    return redirect(request.GET.get('next'))
                                
                                return redirect('/')
                                
                            else:
                                messages.warning(request, "Your email is not verified. Please verify it to login")
                        else:
                            messages.error(request, "Invalid credentials. Please check your email and password")
                    else:
                        messages.error(request, "No account exists with this email address")                  
                else:
                    messages.error(request, "Email and password are required")
                    
        except Exception as e:
            print(e)
            
    return render(request, './accounts/login.html', context)


def signin(request):
    if request.session.get('user_email'):
        del request.session['user_email']
        
    if request.user.is_authenticated:
        messages.warning(request, "you are already logged in")
        return redirect('/')
    else:
        try:
            fname = lname = email = password = cpassword = ""
            context = {
                "fname" : fname,
                "lname" : lname,
                "email" : email,
                "password" : password,
                "cpassword" : cpassword,
            }
            if request.method == "POST":
                fname = request.POST.get("fname")
                lname = request.POST.get("lname")
                email = request.POST.get("email")
                password = request.POST.get("password")
                cpassword = request.POST.get("cpassword")
                
                context['fname'] = fname
                context['lname'] = lname
                context['email'] = email
                context['password'] = password
                context['cpassword'] = cpassword
                
                if email != "":
                    if User.objects.filter(email = email).first() :
                        messages.error(request, "An account already exists with this email")
                    else:
                        if fname != "" and lname != "" and email != "" and password != "" and cpassword != "":
                            if password == cpassword:
                                newUser = User.objects.create_user(email=email, password=password)
                                newUser.first_name = fname
                                newUser.last_name = lname
                                newUser.save()
                                
                                request.session['user_email'] = email
                                
                                context['fname'] = context['lname'] = context['email'] = context['password'] = context['cpassword'] = ""
                                newBot = ChitChat(user=newUser)
                                newBot.save()
                
                                messages.success(request, "Account created successfully. Check your email for OTP")
                                return redirect('email-verify')
                            else:
                                messages.error(request, "Your password do not match")
                        else:
                            messages.error(request, "All fields are required")
                else:
                    messages.error(request, "All fields are required")
            
        except Exception as e:
            print(e)
            
    return render(request, './accounts/signin.html', context)


@login_required(login_url="/auth/login")
def logout(request):
    if request.session.get('user_email'):
        del request.session['user_email']
    auth.logout(request)  
    messages.warning(request, "You are logged out now")  
    return redirect('login')


@login_required(login_url="/auth/login")
def profile(request):
    try:
        fname = lname = age = name = bot = ""
        context = {
            "fname" : fname,
            "lname" : lname,
            "name" : name,
            "age" : age,
            "bot" : bot,
            "bot_types" : Bots().get_bots_type(),
        }
        
        #gettings the user instance from User model
        getUser = User.objects.filter(email=request.user).first()
        fname = getUser.first_name
        lname = getUser.last_name
        
        #gettings the chatbot instance of user from ChitChat model
        getBot = ChitChat.objects.filter(user = getUser).first()
        name = getBot.name
        bot = getBot.bot_type
        age = getBot.age
        
        if request.method == "POST" and "form1" in request.POST:
            fname = request.POST.get("fname")
            lname = request.POST.get("lname")

            if fname != "" and lname != "":
                getUser.first_name = fname
                getUser.last_name = lname
                getUser.save()
                messages.success(request, "Account updated successfully")
            else:
                messages.error(request, "First and Last name can't be blank")
                
        if request.method == "POST" and "form2" in request.POST:
            name = request.POST.get("name")
            age = int(request.POST.get("age"))
            bot = request.POST.get("bot")
            
            if age == "" or bot == "ai-assistant" : age = 0
            
            if name != "":
                if bot != "ai-assistant" and age < 5:
                    messages.error(request, "Age must be greater that 5 for the selected bot type")
                else:
                    if bot == "ai-assistant" or bot == "girlfriend" or bot == "female-friend":
                        gender = "female"
                    else:
                        gender = "male"
                    
                    createBot = Bots(name, age, bot)
                    bot_prompt = createBot.make_bot(bot)
                    
                    getBot.name = name
                    getBot.age = age
                    getBot.bot_type = bot
                    getBot.gender = gender
                    getBot.prompt = bot_prompt
                    
                    getBot.save()
                    
                    messages.success(request, "Bot settings updated successfully")
            else:
                messages.error(request, "A bot must have bot name")
                
        context["fname"] = fname
        context["lname"] = lname
        context["name"] = name
        context["age"] = age
        context["bot"] = bot
                
    except Exception as e:
        print(e) 

    return render(request, './accounts/profile.html', context)



def email_verify(request):
    if request.user.is_authenticated:
        messages.warning("You are already logged in")
        return redirect("/")
    
    else:
        try:
            email = otp = ""
            context = {
                "email": email,
                "otp": otp,
            }
            
            if request.session.get('user_email'):
                email = request.session.get('user_email')
                
            if request.method == "POST" and "form1" in request.POST:
                email = request.POST.get("email")
                email = email.lstrip()
                email = email.rstrip()
                                
                if email != "":
                    getUser = User.objects.filter(email=email).first()
                    if getUser is not None:
                        newOTP = OTP(user=getUser)
                        newOTP.save()
                        
                        request.session["user_email"] = email
                        messages.info(request, "OTP has been send to your email")
                    else:
                        messages.error(request, "This email is not registered")
                else:
                    messages.error(request, "Email is required")

            if request.method == "POST" and "form2" in request.POST:
                otp = request.POST.get("otp")
                otp = otp.lstrip()
                otp = otp.rstrip()
                
                if otp != "":
                    getUser = User.objects.filter(email=email).first()
                    if getUser is not None:
                        if getUser.is_verified == False:
                            ten_min_ago = current_time - datetime.timedelta(minutes=10)
                            checkOTP = OTP.objects.filter(auth_token=otp, user=getUser, is_expired=False, purpose="email_verification", created_at__gte=ten_min_ago).first()
                            if checkOTP:
                                getUser.is_verified = True
                                getUser.save()
                                
                                checkOTP.is_expired = True
                                checkOTP.save()
                                messages.success(request, "Email verified successfully. Now you can login")
                                
                                return redirect('login')
                            else:
                                messages.error(request, "Invalid OTP")
                        else:
                            messages.warning(request, "This account is already verified")
                            return redirect('login')
                    else:
                        messages.error(request, "This email is not registered")
                        
                else:
                    messages.error(request, "OTP is required")

            context["email"] = email
            context["otp"] = otp
            
                
        except Exception as e:
            print(e)
            
        return render(request, './accounts/email_verify.html', context)


def reset_password(request):
    try:
        email = otp = password = cpassword = ""
        context = {
            "email": email,
            "otp": otp,
            "password": password,
            "cpassword": cpassword,
        }
        
        if request.session.get('user_email'):
            email = request.session.get('user_email')

        if request.method == "POST" and "form1" in request.POST:
            email = request.POST.get("email")
            if email != "":
                getUser = User.objects.filter(email=email).first()
                if getUser is not None:
                    newOTP = OTP(user=getUser, purpose="reset_password")
                    newOTP.save()
                    
                    request.session["user_email"] = email
                    messages.info(request, "OTP has been send to you email")
                else:
                    messages.error(request, "This email is not registered")
            else:
                messages.error(request, "Email is required")
                
        if request.method == "POST" and "form2" in request.POST:
            otp = request.POST.get("otp")
            password = request.POST.get("password")
            cpassword = request.POST.get("cpassword")
            
            if otp != "" and password !="" and cpassword != "":
                if password == cpassword:
                    getUser = User.objects.filter(email=email).first()
                    if getUser is not None:
                        ten_min_ago = current_time - datetime.timedelta(minutes=10)
                        checkOTP = OTP.objects.filter(auth_token=otp, user=getUser, is_expired=False, purpose="reset_password", created_at__gte=ten_min_ago).first()
                        if checkOTP:                        
                            checkOTP.is_expired = True
                            checkOTP.save()
                            
                            getUser.set_password(password)
                            getUser.save()
                            
                            messages.success(request, "Password reset successfull. Now please login")
                            return redirect('login')

                        else:
                            messages.error(request, "Invalid OTP")
                    else:
                        messages.error(request, "This email is not registered")
                else:
                    messages.error(request, "Passwords do not match")
            
            else:
                messages.error(request, "OTP, Passwords are required")
            
            
        context["email"] = email
        context["otp"] = otp
        context["password"] = password
        context["cpassword"] = cpassword
        
    
    except Exception as e:
        print(e)
    
    return render(request, './accounts/reset_password.html', context)


