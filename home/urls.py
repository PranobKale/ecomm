from django.urls import path
from home.views import index,get_product_by_mwk



urlpatterns = [
    path("", index, name="index"),
    path('get_product_by_mwk/', get_product_by_mwk, name='get_product_by_mwk'),

]



 