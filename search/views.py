# search/views.py

from products.models import Product
from django.shortcuts import render
from .documents import ProductDocument

# def search(request):
#     query = request.GET.get('q')
#     print(query,'puery-----')
#     if query:
#         products = ProductDocument.search().query("multi_match", query=query, fields=['product_name', 'product_description'])
#     else:
#         products = []
    
#     print(products)
def search(request):
    query = request.GET.get('q')
    if query:
        search_results = ProductDocument.search().query("multi_match", query=query, fields=['product_name', 'product_description'])
        slugs = [hit.slug for hit in search_results]
        print(slugs)
        products = Product.objects.filter(slug__in=slugs)

    else:
        products = Product.objects.all()

    return render(request, 'home/index.html', {'products': products})

