from django.urls import path

from . import views

urlpatterns = [
    path("products/", views.product_list, name="product_list"),
    path("products/<int:product_id>/", views.product_detail, name="product_detail"),
    path("cart/", views.cart_view, name="cart"),
    path("cart/remove/<int:variant_id>/", views.remove_from_cart, name="remove_from_cart"),
]

