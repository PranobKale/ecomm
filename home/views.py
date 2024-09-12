from django.shortcuts import render
from products.models import Product,ProductVariant

# Create your views here.
def index(request):
    try:
        product_obj = Product.objects.all()
        # val = product_obj.varient
        # productvarient_obj = ProductVariant.objects.all()
    except Exception as e:
        # product_obj = Product.objects.none()
        # productvarient_obj = ProductVariant.objects.none()
        print(f'Error : {e}')
    context = {
               'products' : product_obj,
            #    'productvarients' : productvarient_obj
                
               }
    return render(request,'home/index.html', context)



from django.http import JsonResponse
from django.shortcuts import render

def get_product_by_mwk(request):
    # Landing page, show all products
    if request.method == 'GET' and 'flag' not in request.GET:
        products = Product.objects.all()
        return render(request, 'home/index.html', {'products': products})

    # If the request is AJAX (to fetch specific products by category)
    flag = request.GET.get('flag')
    products = Product.objects.filter(mwk_flag=flag)
    product_list = [
        {
            'product_name': product.product_name,
            'slug': product.slug,
            'price': product.price,
            'product_image': product.product_image.first().image.url if product.product_image.exists() else None
        }
        for product in products
    ]
    return JsonResponse({'products': product_list})
