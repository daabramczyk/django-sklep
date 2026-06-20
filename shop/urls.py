from django.urls import path
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    path("products/", views.product_list, name="product_list"),
    path("products/<int:product_id>/", views.product_detail, name="product_detail"),

    path("cart/", views.cart_view, name="cart"),
    path("cart/remove/<int:variant_id>/", views.remove_from_cart, name="remove_from_cart"),

    path("checkout/", views.checkout, name="checkout"),

    path("orders/", views.orders, name="orders"),
    path("orders/<int:order_id>/", views.order_detail, name="order_detail"),

    path(
        "orders/<int:order_id>/pay/",
        views.pay_order,
        name="pay_order"
    ),

    path(
        "orders/<int:order_id>/ship/",
        views.ship_order,
        name="ship_order"
    ),

    path(
        "orders/<int:order_id>/deliver/",
        views.deliver_order,
        name="deliver_order"
    ),

    path(
        "register/",
        views.register_view,
        name="register"
    ),

    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="shop/login.html"
        ),
        name="login"
    ),

    path(
        "logout/",
        views.logout_view,
        name="logout"
    ),

    path(
        "profile/",
        views.profile_view,
        name="profile"
    ),

    path(
        "profile/edit/",
        views.edit_profile,
        name="edit_profile"
    ),
]
