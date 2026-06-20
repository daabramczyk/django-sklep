from django.contrib import admin

from .models import (
    Brand,
    Category,
    Product,
    ProductVariant,
    Order,
    OrderItem,
    OrderStatusHistory,
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
    list_display = ("name", "brand", "category", "gender", "material")
    list_filter = ("brand", "category", "gender")
    search_fields = ("name", "brand__name", "category__name")
    inlines = [ProductVariantInline]


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ("product", "color", "size", "sku", "price", "stock")
    list_filter = ("size", "color", "product__brand", "product__category")
    search_fields = ("sku", "product__name", "product__brand__name")


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
    list_display = ("order_number", "user", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("order_number", "user__username", "user__email")
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
