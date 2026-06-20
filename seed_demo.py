import random
from decimal import Decimal

from django.contrib.auth.models import User

from shop.models import (
    AuditLog,
    Brand,
    Category,
    Coupon,
    Order,
    OrderItem,
    Product,
    ProductVariant,
    Review,
    UserProfile,
)


random.seed(42)

# Czyścimy dane demo, ale zostawiamy superusera
AuditLog.objects.all().delete()
Review.objects.all().delete()
Order.objects.all().delete()
ProductVariant.objects.all().delete()
Product.objects.all().delete()
Brand.objects.all().delete()
Category.objects.all().delete()
Coupon.objects.all().delete()
User.objects.filter(username__startswith="demo_").delete()
User.objects.filter(username__startswith="worker_").delete()
User.objects.filter(username__startswith="manager_").delete()

brands = [
    "Nike", "Adidas", "Puma", "Reebok", "H&M",
    "Reserved", "Zara", "4F", "Under Armour", "Levi's"
]

categories = [
    "Koszulki", "Bluzy", "Spodnie", "Kurtki", "Buty",
    "Czapki", "Akcesoria"
]

brand_objs = [Brand.objects.create(name=name) for name in brands]
category_objs = [Category.objects.create(name=name) for name in categories]

coupons = [
    ("SALE10", 10),
    ("SUMMER15", 15),
    ("VIP20", 20),
    ("BLACK30", 30),
]

for code, discount in coupons:
    Coupon.objects.create(
        code=code,
        discount_percent=discount,
        is_active=True
    )

users = []

for i in range(1, 21):
    user = User.objects.create_user(
        username=f"demo_customer_{i}",
        email=f"demo_customer_{i}@example.com",
        password="Test123456"
    )

    UserProfile.objects.create(
        user=user,
        role="CUSTOMER",
        phone=f"500100{i:03d}",
        street=f"Testowa {i}",
        postal_code=f"20-{i:03d}",
        city=random.choice(["Lublin", "Warszawa", "Kraków", "Gdańsk", "Poznań"])
    )

    users.append(user)

for i in range(1, 3):
    user = User.objects.create_user(
        username=f"worker_{i}",
        email=f"worker_{i}@example.com",
        password="Test123456"
    )

    UserProfile.objects.create(
        user=user,
        role="WAREHOUSE",
        phone=f"600200{i:03d}",
        street=f"Magazynowa {i}",
        postal_code="20-200",
        city="Lublin"
    )

manager = User.objects.create_user(
    username="manager_demo",
    email="manager_demo@example.com",
    password="Test123456"
)

UserProfile.objects.create(
    user=manager,
    role="MANAGER",
    phone="700300300",
    street="Managerska 1",
    postal_code="20-300",
    city="Lublin"
)

product_names = [
    "Essential Tee", "Classic Hoodie", "City Jacket", "Sport Pants",
    "Runner Shoes", "Training Shorts", "Winter Coat", "Denim Jacket",
    "Logo Cap", "Basic Socks", "Active Leggings", "Casual Shirt",
    "Urban Sweatshirt", "Premium Polo", "Softshell Jacket"
]

colors = ["Czarny", "Biały", "Granatowy", "Szary", "Zielony", "Beżowy", "Czerwony"]
sizes = ["XS", "S", "M", "L", "XL", "XXL"]

products = []

for i in range(1, 51):
    brand = random.choice(brand_objs)
    category = random.choice(category_objs)

    product = Product.objects.create(
        name=f"{random.choice(product_names)} {i}",
        brand=brand,
        category=category,
        description=f"Produkt demo numer {i}. Wygodny, modny i gotowy do zamówienia.",
        gender=random.choice(["MEN", "WOMEN", "UNISEX", "KIDS"]),
        material=random.choice([
            "100% bawełna",
            "80% bawełna, 20% poliester",
            "skóra ekologiczna",
            "softshell",
            "denim"
        ]),
        is_featured=i <= 8
    )

    products.append(product)

    variant_count = random.randint(2, 4)

    for v in range(variant_count):
        price = Decimal(random.choice(["49.99", "79.99", "99.99", "149.99", "199.99", "249.99"]))

        sale_price = None
        if random.choice([True, False, False]):
            sale_price = price - Decimal(random.choice(["10.00", "20.00", "30.00"]))

        ProductVariant.objects.create(
            product=product,
            size=random.choice(sizes),
            color=random.choice(colors),
            sku=f"SKU-{i:03d}-{v:02d}",
            price=price,
            sale_price=sale_price,
            stock=random.randint(5, 40)
        )

# Opinie
for product in products:
    reviewers = random.sample(users, random.randint(2, 6))

    for user in reviewers:
        Review.objects.create(
            product=product,
            user=user,
            rating=random.randint(3, 5),
            comment=random.choice([
                "Bardzo dobry produkt.",
                "Dobra jakość w tej cenie.",
                "Produkt zgodny z opisem.",
                "Polecam.",
                "Rozmiar zgodny z oczekiwaniami."
            ])
        )

# Zamówienia
all_variants = list(ProductVariant.objects.all())
status_flow = ["NEW", "PAID", "SHIPPED", "DELIVERED"]

for i in range(1, 41):
    user = random.choice(users)
    profile = user.userprofile

    selected_variants = random.sample(all_variants, random.randint(1, 4))

    total_before = Decimal("0.00")
    order_lines = []

    for variant in selected_variants:
        quantity = random.randint(1, 3)
        price = variant.get_price()
        total_before += price * quantity
        order_lines.append((variant, quantity, price))

    coupon = random.choice(list(Coupon.objects.all()) + [None, None])
    discount_amount = Decimal("0.00")

    if coupon:
        discount_amount = total_before * Decimal(coupon.discount_percent) / Decimal("100")

    total_after = total_before - discount_amount

    order = Order.objects.create(
        user=user,
        first_name=user.first_name,
        last_name=user.last_name,
        phone=profile.phone,
        street=profile.street,
        postal_code=profile.postal_code,
        city=profile.city,
        coupon_code=coupon.code if coupon else "",
        total_before_discount=total_before,
        discount_amount=discount_amount,
        total_after_discount=total_after,
    )

    for variant, quantity, price in order_lines:
        OrderItem.objects.create(
            order=order,
            variant=variant,
            quantity=quantity,
            price_at_order=price
        )

        variant.stock = max(0, variant.stock - quantity)
        variant.save()

    target_status = random.choice(status_flow)

    if target_status in ["PAID", "SHIPPED", "DELIVERED"]:
        order.status = "PAID"
        order.save()

    if target_status in ["SHIPPED", "DELIVERED"]:
        order.tracking_number = f"INPOST{i:09d}"
        order.status = "SHIPPED"
        order.save()

    if target_status == "DELIVERED":
        order.status = "DELIVERED"
        order.save()

print("Seed zakończony.")
print("Produkty:", Product.objects.count())
print("Warianty:", ProductVariant.objects.count())
print("Użytkownicy demo:", User.objects.filter(username__startswith='demo_').count())
print("Zamówienia:", Order.objects.count())
print("Opinie:", Review.objects.count())
print("Kupony:", Coupon.objects.count())
print("AuditLog:", AuditLog.objects.count())
