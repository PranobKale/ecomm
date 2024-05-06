from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect
from django.urls import reverse




def login_page(request):

    if request.method == 'POST':
        
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_obj =  User.objects.filter(email=email)
         
        # Check if the email is already in use
        if not user_obj:
            messages.warning(request, "Account is not found")
            return HttpResponseRedirect(reverse('login'))   
        
        if not user_obj[0].profile.is_email_verified:
            messages.warning(request, "Your account is not verified")
            return HttpResponseRedirect(reverse('login'))
        
        user_obj = authenticate(username = email, password = password)
        if user_obj:
            login(request,user_obj)
            return redirect('/')

        messages.warning(request, "Invalid Credentials")
        return HttpResponseRedirect(reverse('login'))
    
    return render(request, 'accounts/login.html')

def register_page(request):

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
         
        # Check if the email is already in use
        if User.objects.filter(email=email).exists():
            messages.warning(request, "Email is already taken.")
            return HttpResponseRedirect(reverse('register'))
        # user_object = User.objects.filter(username = email)
        # print(user_object)
        # if user_object.exists():
        #     messages.warning(request, "Email is already taken.")
        #     return HttpResponseRedirect(request.path_info)
        
        user_object = User.objects.create(first_name=first_name, last_name=last_name, email=email, password=password )
        user_object.set_password(password) #hashing the password 
        user_object.save()

        messages.success(request, "An email has been sent on your mail.")
        return HttpResponseRedirect(reverse('register'))

    return render(request, 'accounts/register.html')

def activate_email(email_token,Profile):
    try:
        user = Profile.objects.get(email_token= email_token)
        user.is_email_verified = True
        user.save()
        return redirect('/')
    except Exception as e:
        messages.error("Invalid Email token")
        return HttpResponseRedirect(reverse('login'))
