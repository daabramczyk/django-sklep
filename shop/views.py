from django.shortcuts import render, get_object_or_404, redirect

from .models import Product, ProductVariant


def product_list(request):
    if request.method == "POST":
        variant_id = request.POST.get("variant_id")
        quantity = int(request.POST.get("quantity", 1))

        if quantity < 1:
            quantity = 1

        cart = request.session.get("cart", {})

        if variant_id in cart:
            cart[variant_id] += quantity
        else:
            cart[variant_id] = quantity

        request.session["cart"] = cart

        return redirect("cart")

    products = Product.objects.select_related(
        "brand",
        "category",
    ).prefetch_related("variants")

    return render(
        request,
        "shop/product_list.html",
        {
            "products": products
        }
    )


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    if request.method == "POST":
        variant_id = request.POST.get("variant_id")
        quantity = int(request.POST.get("quantity", 1))

        if quantity < 1:
            quantity = 1

        cart = request.session.get("cart", {})

        if variant_id in cart:
            cart[variant_id] += quantity
        else:
            cart[variant_id] = quantity

        request.session["cart"] = cart

        return redirect("cart")

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

    return render(
        request,
        "shop/cart.html",
        {
            "cart_items": cart_items,
            "total": total,
        }
    )


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

    request.session["cart"] = cart

    return redirect("cart")
