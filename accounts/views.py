from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from products.models import *
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse,HttpResponse
import razorpay
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required



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

import traceback
@login_required
def add_to_cart(request, uid):
    from .models import Cart, CartItems
    try:
        # Retrieve the 'variant' (size) from the request GET parameters
        size_name = request.GET.get('variant')
        print(size_name, 'Selected size=============')
        
        # Get the product by its unique ID (uid)
        product = Product.objects.get(uid=uid)
        user = request.user
        print(user, 'User--------')

        # Get or create the cart for the user (ensure cart exists for unpaid items)
        cart, created = Cart.objects.get_or_create(user=user, is_paid=False)
        if created:
            print("New cart created.")
        else:
            print("Cart already exists, updated.")

        # Ensure size_name is present
        if size_name:
            # Retrieve the SizeVariant object based on the selected size name
            size_variant = SizeVariant.objects.get(size_name=size_name)

            # Fetch the first product variant (assuming the color_variant is associated with the product)
            product_variant = product.variants.filter(size_variant=size_variant).first()

            # Ensure a valid product variant exists
            if not product_variant:
                print("No matching product variant found.")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            # Extract the color_variant from the found product_variant
            color_variant = product_variant.color_variant

            # Ensure both the size_variant and color_variant are valid
            if not color_variant or not size_variant:
                print("Invalid color or size variant.")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            # Create or update the cart item with the selected size and color variants
            cart_item = CartItems.objects.create(
                cart = cart, 
                product=product,
                size_variant=size_variant,
                color_variant=color_variant
            )

            # cart_item, created = CartItems.objects.get_or_create(
            #     cart=cart,
            #     product=product,
            #     size_variant=size_variant,
            #     color_variant=color_variant
            # )
            print(cart_item,'cart_item=======')
            if cart_item:
                print("New cart item created.")
            else:
                print("Cart item already exists, updated.")
            
            # Save the cart item
            cart_item.save()

    except Product.DoesNotExist:
        print(f"Product with uid {uid} does not exist.")
    except SizeVariant.DoesNotExist:
        print(f"Size variant '{size_name}' does not exist.")
    except Exception as e:
        traceback.print_exc()
        print(f"An error occurred: {e}")
    
    # Redirect back to the referring page after adding the product to the cart
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



################################previous add to cart function ###############################3
# def add_to_cart(request, uid):
#     from .models import Cart,CartItems
#     try:
#         varient = request.GET.get('variant')
#         if varient:
#             print(varient,'varient=============')
#             # print(uid,'uid----------')
#             product = Product.objects.get(uid = uid)
        
#             # print(product_variant[0].size_variant,'product_variant---------------')
#             user = request.user
#             print(user,'user-------')
#             cart ,created= Cart.objects.get_or_create(user=user,is_paid=False)
#             # print(product.color_variant)

#             cart_items = CartItems.objects.create(cart = cart, product=product)

#             if varient:
#                 # ,color_variant=product.color_variant,size_variant=product.size_variant
#                 varient = request.GET.get('varient')
#                 print(varient,'varient-------------')
#                 product_variant = product.variants.first()
#                 color_variant = product_variant.color_variant
#                 color_name = color_variant.color_name
#                 print(color_name)
#                 size_variant = SizeVariant.objects.get(size_name = varient)
#                 color_variant_obj = ColorVariant.objects.get(color_name = color_name)
#                 cart_items.size_variant = size_variant
#                 cart_items.color_variant = color_variant_obj
#                 cart_items.save()
        
#     except Exception as e:
#         print(e)
    
#     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def remove_cart(request, cart_item_uid):
    from .models import Cart,CartItems
    try:
        print(cart_item_uid,"cart_item_uid---------")
        cart_items = CartItems.objects.get(uid=cart_item_uid)
        cart_items.delete()
    except Exception as e:
        print(e)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def remove_like(request, favorite_product_uid):
    from .models import FavoriteProduct
    try:
        print(favorite_product_uid,"favorite_product_uid---------")
        favorite_product = FavoriteProduct.objects.get(uid=favorite_product_uid)
        print(favorite_product,'---------favorite_product')
        favorite_product.delete()
    except Exception as e:
        print(e)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



@login_required
def cart(request):
    from .models import Cart,CartItems,FavoriteProduct
    try:
        cart_obj = Cart.objects.get(is_paid=False, user=request.user)
    except Cart.DoesNotExist:
        cart_obj = None

    if request.method == 'POST' and cart_obj:
       
        coupon = request.POST.get('coupon')
        try:
            coupon_obj = Coupon.objects.get(coupon_code__icontains=coupon)
            print(coupon_obj, 'coupon---------')
        except Coupon.DoesNotExist:
            messages.warning(request, "Invalid Coupon.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if cart_obj.coupon:
            messages.warning(request, "Coupon already exists.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        if coupon_obj.is_expired:
            messages.warning(request, 'Coupon should be expired')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        print(cart_obj.get_cart_total())
        print(coupon_obj.minimum_amount,'coupon_obj.minimum_amount')
        if cart_obj.get_cart_total() < coupon_obj.minimum_amount:
            messages.warning(request, f"Amount should be greater than {coupon_obj.minimum_amount}")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



        cart_obj.coupon = coupon_obj
        cart_obj.save()
        messages.success(request, "Coupon applied.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    cart_items = []
    payment = None
    from ecomm import settings
    client = razorpay.Client(auth=(settings.KAY,settings.SECRET))
    if cart_obj:
        cart_items = cart_obj.cart_items.all()
        for cart_item in cart_items:
            # print(cart_item.color_variant.color_name)
            # print(cart_item.size_variant.size_name)
            cart_item.is_favorited = FavoriteProduct.objects.filter(user=request.user, product=cart_item.product).exists()
            # var = cart_item.product
            # prod = var.variants
        try:
            payment = client.order.create({'amount':cart_obj.get_cart_total() * 100,'currency':'INR','payment_capture': 1})
            print(payment,'---------payment')
            cart_obj.razor_pay_order_id = payment['id']
            cart_obj.save()
        except Exception as e:
            payment = None

    context = {
        'cart': cart_obj,
        'cart_items': cart_items,
        'payment' : payment
    }
    print(context,'context----------')
    # context = {'cart': cart_obj}
    return render(request, 'accounts/cart.html', context=context)

def remove_coupon(request,cart_id):
    from products.models import Coupon
    from .models import Cart,CartItems
    cart = Cart.objects.get(uid=cart_id)
    coupon_id = cart.coupon
    print(coupon_id,'coupon_id-------=---')
    # coupon = Coupon.objects.get(uid=coupon_id)
    # print(coupon,'coupon----')
    cart.coupon = None
    coupon_id.is_expired = False
    cart.save()
    coupon_id.save()

    messages.success(request, "Coupon removed.")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def toggle_favorite(request, slug):
    from products.models import Product
    from .models import FavoriteProduct
    if request.method == 'POST':
        try:
            product = get_object_or_404(Product, slug=slug)
            favorite, created = FavoriteProduct.objects.get_or_create(user=request.user, product=product)
            if not created:
                favorite.delete()
                is_favorited = False
            else:
                is_favorited = True
            return JsonResponse({'is_favorited': is_favorited})
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({'error': 'An error occurred'}, status=500)
    return JsonResponse({'error': 'Invalid request'}, status=400)


def register_view(request):
    print('inside regi view')
    return render(request, 'accounts/register.html')


@login_required
def profile_page(request):
    return render(request, 'accounts/profile.html')

def custom_logout(request):
    logout(request)
    return redirect('get_product_by_mwk') 

def success(request):
    from .models import Cart
    order_id = request.GET.get('order_id')
    cart = Cart.objects.get(razor_pay_order_id=order_id)
    cart.is_paid = True
    cart.save()
    return HttpResponse('Payment Success')





# def cart(request):
#     from .models import Cart,CartItems

#     cart_obj = Cart.objects.get(is_paid=False, user = request.user)
#     print(cart_obj.pro)
#     if request.method == 'POST':
#         print("request.method == 'POST':")
#         coupon = request.POST.get('coupon')
#         coupon_obj = Coupon.objects.filter(coupon_code__icontaines = coupon)
#         if coupon_obj.exists():
#             messages.warning(request, "Invalid Coupon.")
#             return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
#         if cart_obj.coupon:
#             messages.warning(request, "Coupon already exists.")
#             return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
#         cart_obj.coupon = coupon_obj[0]
#         cart_obj.save()
#         messages.success(request, "Coupon applied.")
#         return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


#     context = {'cart' :  cart_obj}
#     return render(request, 'accounts/cart.html',context=context)

