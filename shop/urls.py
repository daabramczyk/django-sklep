from django.urls import path
from django.contrib.auth import views as auth_views

from . import api_views
from . import views


urlpatterns = [
    path("", views.home, name="home"),

    path("dashboard/", views.dashboard, name="dashboard"),

    path("products/", views.product_list, name="product_list"),
    path("products/<int:product_id>/", views.product_detail, name="product_detail"),
    path("products/<int:product_id>/review/", views.add_review, name="add_review"),

    path("cart/", views.cart_view, name="cart"),
    path("cart/remove/<int:variant_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("cart/apply-coupon/", views.apply_coupon, name="apply_coupon"),
    path("cart/remove-coupon/", views.remove_coupon, name="remove_coupon"),

    path("checkout/", views.checkout, name="checkout"),

    path("orders/", views.orders, name="orders"),
    path("orders/<int:order_id>/", views.order_detail, name="order_detail"),
    path("orders/<int:order_id>/pay/", views.pay_order, name="pay_order"),
    path("orders/<int:order_id>/ship/", views.ship_order, name="ship_order"),
    path("orders/<int:order_id>/deliver/", views.deliver_order, name="deliver_order"),

    path("register/", views.register_view, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="shop/login.html"), name="login"),
    path("logout/", views.logout_view, name="logout"),

    path("profile/", views.profile_view, name="profile"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),

    path("api/brands/", api_views.BrandListApiView.as_view(), name="api_brands"),
    path("api/categories/", api_views.CategoryListApiView.as_view(), name="api_categories"),
    path("api/products/", api_views.ProductListApiView.as_view(), name="api_products"),
    path("api/products/<int:pk>/", api_views.ProductDetailApiView.as_view(), name="api_product_detail"),
    path("api/orders/", api_views.OrderListApiView.as_view(), name="api_orders"),
]
