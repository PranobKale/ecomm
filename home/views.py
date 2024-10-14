from django.shortcuts import render
from products.models import Product,ProductVariant, SizeVariant,ColorVariant

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

from django.shortcuts import get_object_or_404

def get_price(request):
    try:
        size1 = request.GET.get('size')
        product_instance = request.GET.get('product_id')
        color_variant_instance = request.GET.get('color_variant')
        # size_variant_instance = request.GET.get('size_variant_instance')
        print((product_instance),'product-----------1234')

        # Query the product based on slug
        product1 = get_object_or_404(Product, uid=product_instance)
        color_variant_instance = get_object_or_404(ColorVariant, color_name=color_variant_instance)
        size_variant_instance = get_object_or_404(SizeVariant, size_name=size1)

        # product = ProductVariant.objects.get(uuid=product_id)
        product = ProductVariant.objects.filter(
        product=product1,
        color_variant=color_variant_instance,
        size_variant=size_variant_instance
    )
    except Exception as e:
        print(e)
        raise e




    # Fetch the price based on the selected size
    print(product,'product-----------')
    print(product,'product-----------')
    # variant = ProductVariant.objects.get(size_variant__size_name=size)
    price = product1.get_product_price_by_size(size1)
    # context['selected_size'] = size
    # context['updated_price'] = price
    try:
        return JsonResponse({'price': price})  # Assuming price is an attribute of ProductVariant
    except ProductVariant.DoesNotExist:
        return JsonResponse({'price': None}, status=404)
