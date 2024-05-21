from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from products.models import *




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
        print(first_name)
        print(last_name)
        print(email)
        print(password)
        print(request.POST.get('first_name'))
        
        # Check if the email is already in use
        if User.objects.filter(email=email).exists():
            messages.warning(request, "Email is already taken.")
            return HttpResponseRedirect(reverse('register'))
        # user_object = User.objects.filter(username = email)
        # print(user_object)
        # if user_object.exists():
        #     messages.warning(request, "Email is already taken.")
        #     return HttpResponseRedirect(request.path_info)
        
        user_object = User.objects.create(username=email ,first_name=first_name, last_name=last_name, email=email, password=password )
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

def add_to_cart(request, uid):
    from .models import Cart,CartItems
    varient = request.GET.get('varient')

    product = Product.objects.get(uid = uid)
    user = request.user
    cart ,created= Cart.objects.get_or_create(user=user,is_paid=False)

    cart_items = CartItems.objects.create(cart = cart, product=product)

    if varient:
        varient = request.GET.get('varient')
        size_variant = SizeVariant.objects.get(size_name = varient)
        cart_items.size_variant = size_variant
        cart_items.save()
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def remove_cart(request, cart_item_uid):
    from .models import Cart,CartItems
    try:
        print(cart_item_uid,"cart_item_uid---------")
        cart_items = CartItems.objects.get(uid=cart_item_uid)
        cart_items.delete()
    except Exception as e:
        print(e)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def cart(request):
    from .models import Cart,CartItems

    cart_obj = Cart.objects.get(is_paid=False, user = request.user)
    print(cart_obj.pro)
    if request.method == 'POST':
        print("request.method == 'POST':")
        coupon = request.POST.get('coupon')
        coupon_obj = Coupon.objects.filter(coupon_code__icontaines = coupon)
        if coupon_obj.exists():
            messages.warning(request, "Invalid Coupon.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        if cart_obj.coupon:
            messages.warning(request, "Coupon already exists.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        cart_obj.coupon = coupon_obj[0]
        cart_obj.save()
        messages.success(request, "Coupon applied.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


    context = {'cart' :  cart_obj}
    return render(request, 'accounts/cart.html',context=context)

