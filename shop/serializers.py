from rest_framework import serializers

from .models import Brand, Category, Product, ProductVariant, Order, OrderItem


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = [
            "id",
            "name",
            "description",
        ]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "description",
        ]


class ProductVariantSerializer(serializers.ModelSerializer):
    final_price = serializers.SerializerMethodField()

    class Meta:
        model = ProductVariant
        fields = [
            "id",
            "size",
            "color",
            "sku",
            "price",
            "sale_price",
            "final_price",
            "stock",
        ]

    def get_final_price(self, obj):
        return obj.get_price()


class ProductSerializer(serializers.ModelSerializer):
    brand = BrandSerializer()
    category = CategorySerializer()
    variants = ProductVariantSerializer(many=True)
    average_rating = serializers.SerializerMethodField()
    reviews_count = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "brand",
            "category",
            "description",
            "gender",
            "material",
            "is_featured",
            "average_rating",
            "reviews_count",
            "variants",
        ]

    def get_average_rating(self, obj):
        return obj.average_rating

    def get_reviews_count(self, obj):
        return obj.reviews_count


class OrderItemSerializer(serializers.ModelSerializer):
    variant = ProductVariantSerializer()

    class Meta:
        model = OrderItem
        fields = [
            "variant",
            "quantity",
            "price_at_order",
        ]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "order_number",
            "status",
            "created_at",
            "coupon_code",
            "total_before_discount",
            "discount_amount",
            "total_after_discount",
            "tracking_number",
            "items",
        ]
