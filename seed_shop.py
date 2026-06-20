from decimal import Decimal
from shop.models import Brand, Category, Product, ProductVariant

# marki
nike, _ = Brand.objects.get_or_create(name="Nike", defaults={"description": "Marka sportowa"})
adidas, _ = Brand.objects.get_or_create(name="Adidas", defaults={"description": "Marka sportowa"})
puma, _ = Brand.objects.get_or_create(name="Puma", defaults={"description": "Marka sportowa"})
reserved, _ = Brand.objects.get_or_create(name="Reserved", defaults={"description": "Marka odzieżowa"})
hm, _ = Brand.objects.get_or_create(name="H&M", defaults={"description": "Marka odzieżowa"})

# kategorie
tshirt, _ = Category.objects.get_or_create(name="Koszulki", defaults={"description": "T-shirty i koszulki"})
hoodie, _ = Category.objects.get_or_create(name="Bluzy", defaults={"description": "Bluzy z kapturem i bez"})
pants, _ = Category.objects.get_or_create(name="Spodnie", defaults={"description": "Spodnie długie i krótkie"})
shoes, _ = Category.objects.get_or_create(name="Buty", defaults={"description": "Obuwie"})
jacket, _ = Category.objects.get_or_create(name="Kurtki", defaults={"description": "Odzież wierzchnia"})

products_data = [
    {
        "name": "Air Tee",
        "brand": nike,
        "category": tshirt,
        "description": "Klasyczna koszulka sportowa Nike.",
        "gender": "MEN",
        "material": "100% bawełna",
        "variants": [
            ("Czarny", "M", "NIKE-AIR-TEE-BLK-M", "99.99", 10),
            ("Czarny", "L", "NIKE-AIR-TEE-BLK-L", "99.99", 8),
            ("Biały", "L", "NIKE-AIR-TEE-WHT-L", "99.99", 5),
        ],
    },
    {
        "name": "Club Hoodie",
        "brand": nike,
        "category": hoodie,
        "description": "Ciepła bluza z kapturem.",
        "gender": "UNISEX",
        "material": "80% bawełna, 20% poliester",
        "variants": [
            ("Czarny", "L", "NIKE-CLUB-HOOD-BLK-L", "199.99", 6),
            ("Szary", "XL", "NIKE-CLUB-HOOD-GRY-XL", "199.99", 4),
        ],
    },
    {
        "name": "Essentials Tee",
        "brand": adidas,
        "category": tshirt,
        "description": "Codzienna koszulka Adidas.",
        "gender": "MEN",
        "material": "100% bawełna",
        "variants": [
            ("Granatowy", "M", "ADI-ESS-TEE-NAV-M", "89.99", 12),
            ("Biały", "L", "ADI-ESS-TEE-WHT-L", "89.99", 7),
        ],
    },
    {
        "name": "Classic Pants",
        "brand": reserved,
        "category": pants,
        "description": "Klasyczne spodnie materiałowe.",
        "gender": "MEN",
        "material": "98% bawełna, 2% elastan",
        "variants": [
            ("Czarny", "M", "RES-PANTS-BLK-M", "149.99", 5),
            ("Beżowy", "L", "RES-PANTS-BGE-L", "149.99", 3),
        ],
    },
    {
        "name": "City Jacket",
        "brand": hm,
        "category": jacket,
        "description": "Lekka kurtka miejska.",
        "gender": "UNISEX",
        "material": "Poliester",
        "variants": [
            ("Zielony", "L", "HM-CITY-JACKET-GRN-L", "249.99", 4),
            ("Czarny", "XL", "HM-CITY-JACKET-BLK-XL", "249.99", 2),
        ],
    },
]

for data in products_data:
    product, _ = Product.objects.get_or_create(
        name=data["name"],
        brand=data["brand"],
        category=data["category"],
        defaults={
            "description": data["description"],
            "gender": data["gender"],
            "material": data["material"],
        },
    )

    for color, size, sku, price, stock in data["variants"]:
        ProductVariant.objects.get_or_create(
            sku=sku,
            defaults={
                "product": product,
                "color": color,
                "size": size,
                "price": Decimal(price),
                "stock": stock,
            },
        )

print("Dane testowe dodane.")
