from django.urls import path
from .views import login_page,register_page , activate_email,cart,add_to_cart,remove_cart




urlpatterns = [
    path("login/", login_page, name="login"),
    path("register/", register_page, name="register"),
    path("cart/", cart, name="cart"),
    path("add-to-cart/<uid>/", add_to_cart, name="add_to_cart"),
    path("remove-cart/<cart_item_uid>/", remove_cart, name="remove_cart"),
    # path("activate/<email_token>/", activate_email, name="activate_email")
]



 