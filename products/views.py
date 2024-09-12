from django.shortcuts import render
from elasticsearch import Elasticsearch
from products.models import  Product, ColorVariant,ProductVariant,SizeVariant
from django.http import HttpResponse, Http404

def get_product(request, slug):
    try:
        product_variant = None
        productvarient_obj = None
        product = Product.objects.get(slug=slug)

        if product:
            productvarient_obj = product.variants.all()

        if productvarient_obj:
            print(productvarient_obj, 'productvarient_obj--------')
            product_variant = productvarient_obj[0]

        context = {
            'product': product,
            'product_variant': product_variant
        }

        if request.GET.get('size'):
            size = request.GET.get('size')
            price = product.get_product_price_by_size(size)
            context['selected_size'] = size
            context['updated_price'] = price

        return render(request, 'product/product.html', context=context)

    except Product.DoesNotExist:
        # If the product is not found, raise a 404 error
        raise Http404("Product not found")

    except Exception as e:
        print(e)
        # Return a generic error page or response
        return HttpResponse("An error occurred while fetching the product.", status=500)


def get_products(request):
    products = Product.objects.all()
    print(products,'get_products--------')
    return render(request, 'home/index.html', {'products': products})

