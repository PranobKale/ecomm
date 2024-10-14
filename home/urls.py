from django.urls import path
from home.views import index,get_product_by_mwk,get_price



urlpatterns = [
    path("", index, name="index"),
    path('get_product_by_mwk/', get_product_by_mwk, name='get_product_by_mwk'),
    path('get_price/', get_price, name='get_price'),


]



 