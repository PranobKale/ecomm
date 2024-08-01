from django.shortcuts import render
from elasticsearch import Elasticsearch
from products.models import  Product

def get_product(request, slug):
    try:
        print(request,"request")
        print(request.user,"request.user")
        product = Product.objects.get(slug=slug)

        context = {'product' : product}
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

