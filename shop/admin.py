from django.contrib import admin

from .models import (
    Brand,
    Category,
    Product,
    ProductVariant,
    Coupon,
    Order,
    OrderItem,
    OrderStatusHistory,
    UserProfile,
    Review,
)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "brand", "category", "gender", "is_featured", "average_rating")
    list_filter = ("brand", "category", "gender", "is_featured")
    search_fields = ("name", "brand__name", "category__name")
    inlines = [ProductVariantInline]


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ("product", "color", "size", "sku", "price", "sale_price", "stock")
    list_filter = ("size", "color", "product__brand", "product__category")
    search_fields = ("sku", "product__name", "product__brand__name")


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ("code", "discount_percent", "is_active")
    list_filter = ("is_active",)
    search_fields = ("code",)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("variant", "quantity", "price_at_order")
    can_delete = False


class OrderStatusHistoryInline(admin.TabularInline):
    model = OrderStatusHistory
    extra = 0
    readonly_fields = ("status", "created_at")
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "order_number",
        "user",
        "status",
        "coupon_code",
        "total_before_discount",
        "discount_amount",
        "total_after_discount",
        "tracking_number",
        "created_at",
    )
    list_filter = ("status", "created_at")
    search_fields = ("order_number", "user__username", "user__email", "tracking_number")
    inlines = [OrderItemInline, OrderStatusHistoryInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "variant", "quantity", "price_at_order")
    search_fields = ("order__order_number", "variant__sku")


@admin.register(OrderStatusHistory)
class OrderStatusHistoryAdmin(admin.ModelAdmin):
    list_display = ("order", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("order__order_number",)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "phone", "city")
    search_fields = ("user__username", "phone", "city")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("product", "user", "rating", "created_at")
    list_filter = ("rating", "created_at")
    search_fields = ("product__name", "user__username")
