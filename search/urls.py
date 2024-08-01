from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from products import views
from .views import search

urlpatterns = [
    path('', search, name='search'),
    path('product/<slug:slug>/', views.get_product, name='get_product'),
    # other url patterns...
]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
