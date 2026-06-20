from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Brand, Category, Product, Order
from .serializers import (
    BrandSerializer,
    CategorySerializer,
    ProductSerializer,
    OrderSerializer,
)


class BrandListApiView(generics.ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class CategoryListApiView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductListApiView(generics.ListAPIView):
    queryset = Product.objects.select_related(
        "brand",
        "category",
    ).prefetch_related(
        "variants",
        "reviews",
    )
    serializer_class = ProductSerializer


class ProductDetailApiView(generics.RetrieveAPIView):
    queryset = Product.objects.select_related(
        "brand",
        "category",
    ).prefetch_related(
        "variants",
        "reviews",
    )
    serializer_class = ProductSerializer


class OrderListApiView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(
            user=self.request.user
        ).prefetch_related(
            "items",
            "items__variant",
        )
