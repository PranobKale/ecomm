from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import login_page,register_page , activate_email,cart,add_to_cart,remove_cart,remove_coupon,remove_like,toggle_favorite,register_view,profile_page,custom_logout




urlpatterns = [
    path("login/", login_page, name="login"),
    # path('logout/', LogoutView.as_view(next_page='get_products12'), name='logout'),
    path('logout/', custom_logout, name='logout'),
    path("register/", register_page, name="register"),
    # path('register/', register_view, name='register'),
    path("cart/", cart, name="cart"),
    path("add-to-cart/<uid>/", add_to_cart, name="add_to_cart"),
    path("remove-cart/<cart_item_uid>/", remove_cart, name="remove_cart"),
    # path("remove-like/<favorite_product_uid>/", remove_like, name="remove_like"),
    path('toggle-favorite/<slug:slug>/', toggle_favorite, name='toggle_favorite'),
    path('remove_coupon/<cart_id>/',remove_coupon, name='remove_coupon'),
    path('profile/', profile_page, name='profile'),
    # path('success/',success, name='success'),
    # path('toggle_favorite/<uuid:cart_item_uid>/',toggle_favorite, name='toggle_favorite'),
    # path("activate/<email_token>/", activate_email, name="activate_email")
]



 