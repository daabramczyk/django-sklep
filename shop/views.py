from decimal import Decimal

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q, Sum, F, DecimalField, ExpressionWrapper
from django.shortcuts import render, get_object_or_404, redirect

from .app_messages import add_app_message
from .forms import RegisterForm, UserForm, UserProfileForm, ReviewForm
from .models import (
    Brand,
    Category,
    Product,
    ProductVariant,
    Coupon,
    Order,
    OrderItem,
    UserProfile,
    Review,
)


def calculate_cart(request):
    cart = request.session.get("cart", {})

    cart_items = []
    subtotal = Decimal("0.00")

    for variant_id, quantity in cart.items():
        variant = get_object_or_404(ProductVariant, pk=variant_id)
        price = variant.get_price()
        item_total = price * quantity

        cart_items.append({
            "variant": variant,
            "quantity": quantity,
            "price": price,
            "item_total": item_total,
        })

        subtotal += item_total

    coupon = None
    discount_amount = Decimal("0.00")
    total = subtotal

    coupon_code = request.session.get("coupon_code")

    if coupon_code:
        try:
            coupon = Coupon.objects.get(code=coupon_code, is_active=True)
            discount_amount = subtotal * Decimal(coupon.discount_percent) / Decimal("100")
            total = subtotal - discount_amount
        except Coupon.DoesNotExist:
            request.session.pop("coupon_code", None)

    return {
        "cart_items": cart_items,
        "subtotal": subtotal,
        "coupon": coupon,
        "discount_amount": discount_amount,
        "total": total,
    }


def add_to_cart(request):
    variant_id = request.POST.get("variant_id")

    try:
        quantity = int(request.POST.get("quantity", 1))
    except ValueError:
        add_app_message(request, "KB_01")
        return False

    if quantity < 1:
        add_app_message(request, "KB_01")
        return False

    variant = get_object_or_404(ProductVariant, pk=variant_id)

    cart = request.session.get("cart", {})
    current_quantity = cart.get(str(variant_id), 0)
    new_quantity = current_quantity + quantity

    if new_quantity > variant.stock:
        add_app_message(
            request,
            "KB_02",
            f"W koszyku masz już {current_quantity}, dostępne: {variant.stock}."
        )
        return False

    cart[str(variant_id)] = new_quantity
    request.session["cart"] = cart

    add_app_message(request, "KS_01", f"{variant} x {quantity}.")
    return True


def home(request):
    featured_products = Product.objects.filter(is_featured=True).select_related(
        "brand",
        "category",
    ).prefetch_related("variants")[:4]

    top_products = Product.objects.select_related(
        "brand",
        "category",
    ).prefetch_related("variants").annotate(
        sold=Sum("variants__orderitem__quantity")
    ).order_by("-sold")[:4]

    return render(
        request,
        "shop/home.html",
        {
            "featured_products": featured_products,
            "top_products": top_products,
        }
    )


def product_list(request):
    if request.method == "POST":
        success = add_to_cart(request)

        if success:
            return redirect("cart")

        return redirect("product_list")

    products = Product.objects.select_related(
        "brand",
        "category",
    ).prefetch_related("variants", "reviews")

    query = request.GET.get("q", "")
    brand_id = request.GET.get("brand", "")
    category_id = request.GET.get("category", "")
    size = request.GET.get("size", "")

    if query:
        products = products.filter(
            Q(name__icontains=query)
            | Q(brand__name__icontains=query)
            | Q(category__name__icontains=query)
        )

    if brand_id:
        products = products.filter(brand_id=brand_id)

    if category_id:
        products = products.filter(category_id=category_id)

    if size:
        products = products.filter(variants__size=size)

    if query or brand_id or category_id or size:
        add_app_message(request, "KI_01")

    products = products.distinct()

    return render(
        request,
        "shop/product_list.html",
        {
            "products": products,
            "brands": Brand.objects.all(),
            "categories": Category.objects.all(),
            "sizes": ProductVariant.SIZE_CHOICES,
            "selected_query": query,
            "selected_brand": brand_id,
            "selected_category": category_id,
            "selected_size": size,
        }
    )


def product_detail(request, product_id):
    product = get_object_or_404(
        Product.objects.select_related("brand", "category").prefetch_related("variants", "reviews"),
        pk=product_id,
    )

    if request.method == "POST":
        success = add_to_cart(request)

        if success:
            return redirect("cart")

        return redirect("product_detail", product_id=product.id)

    review_form = ReviewForm()

    return render(
        request,
        "shop/product_detail.html",
        {
            "product": product,
            "review_form": review_form,
        }
    )


@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    if request.method == "POST":
        if Review.objects.filter(product=product, user=request.user).exists():
            add_app_message(request, "KB_11")
            return redirect("product_detail", product_id=product.id)

        form = ReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()

            add_app_message(request, "KS_11")
            return redirect("product_detail", product_id=product.id)

    return redirect("product_detail", product_id=product.id)


def cart_view(request):
    cart_data = calculate_cart(request)

    return render(
        request,
        "shop/cart.html",
        cart_data,
    )


def apply_coupon(request):
    if request.method == "POST":
        code = request.POST.get("coupon_code", "").strip().upper()

        try:
            coupon = Coupon.objects.get(code=code, is_active=True)
            request.session["coupon_code"] = coupon.code
            add_app_message(request, "KS_09", f"Kod: {coupon.code}.")
        except Coupon.DoesNotExist:
            add_app_message(request, "KB_10")

    return redirect("cart")


def remove_coupon(request):
    request.session.pop("coupon_code", None)
    add_app_message(request, "KS_10")
    return redirect("cart")


def remove_from_cart(request, variant_id):
    cart = request.session.get("cart", {})
    variant_id = str(variant_id)

    if request.method == "POST":
        remove_quantity = int(request.POST.get("remove_quantity", 1))

        if remove_quantity < 1:
            remove_quantity = 1

        if variant_id in cart:
            current_quantity = cart[variant_id]

            if remove_quantity >= current_quantity:
                del cart[variant_id]
            else:
                cart[variant_id] = current_quantity - remove_quantity

            add_app_message(request, "KI_02")

    request.session["cart"] = cart

    return redirect("cart")


@login_required
def checkout(request):
    cart = request.session.get("cart", {})

    if not cart:
        add_app_message(request, "KB_03")
        return redirect("cart")

    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if not profile.phone or not profile.street or not profile.postal_code or not profile.city:
        add_app_message(
            request,
            "KB_07",
            "Uzupełnij telefon i adres dostawy przed złożeniem zamówienia."
        )
        return redirect("edit_profile")

    if request.method == "POST":
        try:
            with transaction.atomic():
                cart_data = calculate_cart(request)

                order = Order.objects.create(
                    user=request.user,
                    first_name=request.user.first_name,
                    last_name=request.user.last_name,
                    phone=profile.phone,
                    street=profile.street,
                    postal_code=profile.postal_code,
                    city=profile.city,
                    coupon_code=cart_data["coupon"].code if cart_data["coupon"] else "",
                    total_before_discount=cart_data["subtotal"],
                    discount_amount=cart_data["discount_amount"],
                    total_after_discount=cart_data["total"],
                )

                for item in cart_data["cart_items"]:
                    variant = ProductVariant.objects.select_for_update().get(pk=item["variant"].id)
                    quantity = item["quantity"]

                    if quantity > variant.stock:
                        add_app_message(
                            request,
                            "KB_05",
                            f"{variant} — dostępne: {variant.stock}."
                        )
                        return redirect("cart")

                    OrderItem.objects.create(
                        order=order,
                        variant=variant,
                        quantity=quantity,
                        price_at_order=item["price"],
                    )

                    variant.stock -= quantity
                    variant.save()

                request.session["cart"] = {}
                request.session.pop("coupon_code", None)

            add_app_message(request, "KS_02", f"Numer: {order.order_number}.")
            return redirect("orders")

        except ProductVariant.DoesNotExist:
            add_app_message(request, "KB_04")
            return redirect("cart")

    return redirect("cart")


@login_required
def orders(request):
    user_orders = Order.objects.filter(user=request.user).prefetch_related(
        "items",
        "items__variant",
        "items__variant__product",
        "items__variant__product__brand",
    ).order_by("-created_at")

    return render(request, "shop/orders.html", {"orders": user_orders})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(
        Order.objects.prefetch_related(
            "items",
            "items__variant",
            "items__variant__product",
            "items__variant__product__brand",
            "status_history",
        ),
        pk=order_id,
        user=request.user
    )

    return render(
        request,
        "shop/order_detail.html",
        {
            "order": order,
            "total": order.total_after_discount,
        }
    )


@login_required
def pay_order(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)

    if order.status != "NEW":
        add_app_message(request, "KO_01", "Opłacić można tylko nowe zamówienie.")
        return redirect("order_detail", order_id=order.id)

    if request.method == "POST":
        blik_code = request.POST.get("blik_code", "").strip()

        if not blik_code.isdigit() or len(blik_code) != 6:
            add_app_message(request, "KB_09", "Kod BLIK musi mieć dokładnie 6 cyfr.")
            return redirect("order_detail", order_id=order.id)

        order.status = "PAID"
        order.save()

        add_app_message(request, "KS_06", f"Zamówienie {order.order_number} zostało opłacone.")
        return redirect("order_detail", order_id=order.id)

    return redirect("order_detail", order_id=order.id)


@login_required
def ship_order(request, order_id):
    order = get_object_or_404(Order, pk=order_id)

    if not request.user.is_staff:
        add_app_message(request, "KB_06", "Nie masz uprawnień do wysyłki zamówienia.")
        return redirect("order_detail", order_id=order.id)

    if order.status != "PAID":
        add_app_message(request, "KO_02", "Wysłać można tylko opłacone zamówienie.")
        return redirect("order_detail", order_id=order.id)

    if request.method == "POST":
        tracking_number = request.POST.get("tracking_number", "").strip()

        if not tracking_number:
            add_app_message(request, "KB_08", "Podaj numer przesyłki.")
            return redirect("order_detail", order_id=order.id)

        order.tracking_number = tracking_number
        order.status = "SHIPPED"
        order.save()

        add_app_message(request, "KS_07", f"Zamówienie {order.order_number} zostało wysłane.")
        return redirect("order_detail", order_id=order.id)

    return redirect("order_detail", order_id=order.id)


@login_required
def deliver_order(request, order_id):
    order = get_object_or_404(Order, pk=order_id)

    if not request.user.is_staff:
        add_app_message(request, "KB_06", "Nie masz uprawnień do zmiany statusu zamówienia.")
        return redirect("order_detail", order_id=order.id)

    if order.status != "SHIPPED":
        add_app_message(request, "KO_03", "Dostarczyć można tylko wysłane zamówienie.")
        return redirect("order_detail", order_id=order.id)

    if request.method == "POST":
        order.status = "DELIVERED"
        order.save()

        add_app_message(request, "KS_08", f"Zamówienie {order.order_number} zostało dostarczone.")
        return redirect("order_detail", order_id=order.id)

    return redirect("order_detail", order_id=order.id)


def register_view(request):
    if request.user.is_authenticated:
        return redirect("profile")

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            add_app_message(request, "KS_04")
            return redirect("profile")
    else:
        form = RegisterForm()

    return render(request, "shop/register.html", {"form": form})


@login_required
def profile_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    orders = Order.objects.filter(user=request.user)
    orders_count = orders.count()

    total_spent = OrderItem.objects.filter(order__user=request.user).aggregate(
        total=Sum(
            ExpressionWrapper(
                F("quantity") * F("price_at_order"),
                output_field=DecimalField()
            )
        )
    )["total"] or 0

    last_order = orders.order_by("-created_at").first()

    return render(
        request,
        "shop/profile.html",
        {
            "profile": profile,
            "orders_count": orders_count,
            "total_spent": total_spent,
            "last_order": last_order,
        }
    )


@login_required
def edit_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            add_app_message(request, "KS_03")
            return redirect("profile")
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=profile)

    return render(
        request,
        "shop/edit_profile.html",
        {
            "user_form": user_form,
            "profile_form": profile_form,
        }
    )


def logout_view(request):
    logout(request)
    add_app_message(request, "KS_05")
    return redirect("product_list")
