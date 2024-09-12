from django.urls import path
from products.views import get_product,get_products



urlpatterns = [
    path("<slug>/", get_product, name="get_product"),
    path('', get_products, name='get_products12'),
    # path('get_product_by_mwk/', get_product_by_mwk, name='get_product_by_mwk'),
]

# urlpatterns = [
# ]


