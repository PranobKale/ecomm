from django.urls import path
from products import views
from .views import search

urlpatterns = [
    path('', search, name='search'),
    path('product/<slug:slug>/', views.get_product, name='get_product'),
]
