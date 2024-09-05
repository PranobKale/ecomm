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


