from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q, Sum, F, DecimalField, ExpressionWrapper

from .app_messages import add_app_message
from .forms import RegisterForm, ProfileEditForm
from .models import Brand, Category, Product, ProductVariant, Order, OrderItem


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


def product_list(request):
    if request.method == "POST":
        success = add_to_cart(request)

        if success:
            return redirect("cart")

        return redirect("product_list")

    products = Product.objects.select_related(
        "brand",
        "category",
    ).prefetch_related("variants")

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
    product = get_object_or_404(Product, pk=product_id)

    if request.method == "POST":
        success = add_to_cart(request)

        if success:
            return redirect("cart")

        return redirect("product_detail", product_id=product.id)

    return render(request, "shop/product_detail.html", {"product": product})


def cart_view(request):
    cart = request.session.get("cart", {})

    cart_items = []
    total = 0

    for variant_id, quantity in cart.items():
        variant = get_object_or_404(ProductVariant, pk=variant_id)
        item_total = variant.price * quantity

        cart_items.append({
            "variant": variant,
            "quantity": quantity,
            "item_total": item_total,
        })

        total += item_total

    return render(request, "shop/cart.html", {"cart_items": cart_items, "total": total})


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

    if request.method == "POST":
        try:
            with transaction.atomic():
                order = Order.objects.create(user=request.user)

                for variant_id, quantity in cart.items():
                    variant = ProductVariant.objects.select_for_update().get(pk=variant_id)

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
                        price_at_order=variant.price,
                    )

                    variant.stock -= quantity
                    variant.save()

                request.session["cart"] = {}

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

    total = 0

    for item in order.items.all():
        total += item.quantity * item.price_at_order

    return render(
        request,
        "shop/order_detail.html",
        {
            "order": order,
            "total": total,
        }
    )


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
    orders = Order.objects.filter(user=request.user)

    orders_count = orders.count()

    total_spent = OrderItem.objects.filter(
        order__user=request.user
    ).aggregate(
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
            "orders_count": orders_count,
            "total_spent": total_spent,
            "last_order": last_order,
        }
    )


@login_required
def edit_profile(request):
    if request.method == "POST":
        form = ProfileEditForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            add_app_message(request, "KS_03")
            return redirect("profile")
    else:
        form = ProfileEditForm(instance=request.user)

    return render(request, "shop/edit_profile.html", {"form": form})


def logout_view(request):
    logout(request)
    add_app_message(request, "KS_05")
    return redirect("product_list")

@login_required
def pay_order(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)

    if order.status != "NEW":
        add_app_message(request, "KO_01", "Opłacić można tylko nowe zamówienie.")
        return redirect("order_detail", order_id=order.id)

    if request.method == "POST":
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
        order.status = "SHIPPED"
        order.save()

        add_app_message(request, "KS_07", f"Zamówienie {order.order_number} zostało wysłane.")
        return redirect("order_detail", order_id=order.id)

    return redirect("order_detail", order_id=order.id)
