from django.shortcuts import render
from elasticsearch import Elasticsearch
from products.models import  Product, ColorVariant,ProductVariant,SizeVariant

def get_product(request, slug):
    try:
        print(request,"request")
        product_variant = None
        productvarient_obj = None
        product = Product.objects.get(slug=slug)
        # size1 = SizeVariant.objects.all()
        # print(size1,'size1------------')
        # [<SizeVariant: L>, <SizeVariant: XL>, <SizeVariant: XXL>]>
        if product:
            productvarient_obj = product.variants.all()
        if productvarient_obj:
            print(productvarient_obj,'productvarient_obj--------')
            product_variant = productvarient_obj[0]
        # product.size_variant.add(*size1)
        # Fetch all related size variants
        # color_variants = ColorVariant.objects.all()
        # color_red = ColorVariant.objects.get(color_name="Green")
        # size_small = SizeVariant.objects.get(size_name="XL")
        # print(f"size_small:{size_small},color_red:{color_red}, product:{product} ")
        # print('------------------------------------------------------')
        # product_variant = ProductVariant.objects.get(size_variant=size_small,color_variant=color_red,product=product)
        # product_variant.delete()
        

        
        # ProductVariant.objects.create(product=product, size_variant=size_small, color_variant=color_red)
# <QuerySet [<ColorVariant: Black>, <ColorVariant: Blue>, <ColorVariant: Purple>, <ColorVariant: Green>, <ColorVariant: Brown>]>
        # print(color_variants,'color_variant-------------')
        # print(size_variants,'size_variant------')
        

        context = {
            'product' : product,
            'product_variant' : product_variant 
            }
        if request.GET.get('size'):
            size = request.GET.get('size')
            price = product.get_product_price_by_size(size)
            context['selected_size'] = size
            context['updated_price'] = price

        return render(request,'product/product.html', context = context)
    except  Exception as e:
        print(e)


def get_products(request):
    products = Product.objects.all()
    print(get_products,'get_products--------')
    return render(request, 'home/index.html', {'products': products})

