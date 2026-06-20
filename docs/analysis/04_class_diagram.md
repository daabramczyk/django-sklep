# Diagram klas UML — Clothing Store

## Cel

Diagram klas przedstawia strukturę obiektową systemu sklepu internetowego oraz relacje pomiędzy klasami domenowymi.

## Główne klasy domenowe

### User

Odpowiada za uwierzytelnienie użytkownika.

### UserProfile

Przechowuje dane biznesowe użytkownika:

- rola
- telefon
- adres dostawy

### Brand

Reprezentuje markę produktu.

### Category

Reprezentuje kategorię produktu.

### Product

Produkt biznesowy.

Przykład:

- Nike Air Max
- Adidas Superstar

### ProductVariant

Konkretny wariant produktu.

Przykład:

- Nike Air Max
- rozmiar: 42
- kolor: czarny

### Coupon

Kod rabatowy.

### Review

Ocena produktu.

Zakres:

- 1 gwiazdka
- 5 gwiazdek

### Order

Reprezentuje zamówienie klienta.

Statusy:

- NEW
- PAID
- SHIPPED
- DELIVERED

### OrderItem

Pozycja zamówienia.

### OrderStatusHistory

Historia zmian statusów.

### AuditLog

Historia operacji wykonywanych w systemie.

---

## Diagram UML

```mermaid
classDiagram

class User

class UserProfile {
    +role
    +phone
    +street
    +postal_code
    +city
}

class Brand {
    +name
}

class Category {
    +name
}

class Product {
    +name
    +description
    +gender
    +material
    +is_featured
    +average_rating()
    +reviews_count()
}

class ProductVariant {
    +size
    +color
    +sku
    +price
    +sale_price
    +stock
    +get_price()
    +is_on_sale()
}

class Coupon {
    +code
    +discount_percent
    +is_active
}

class Review {
    +rating
    +comment
}

class Order {
    +order_number
    +status
    +tracking_number
    +coupon_code
    +total_before_discount
    +discount_amount
    +total_after_discount
}

class OrderItem {
    +quantity
    +price_at_order
}

class OrderStatusHistory {
    +status
    +created_at
}

class AuditLog {
    +action
    +object_type
    +object_id
    +description
    +created_at
}

User "1" --> "1" UserProfile

Brand "1" --> "*" Product
Category "1" --> "*" Product

Product "1" --> "*" ProductVariant

Product "1" --> "*" Review
User "1" --> "*" Review

User "1" --> "*" Order

Order "1" --> "*" OrderItem
ProductVariant "1" --> "*" OrderItem

Order "1" --> "*" OrderStatusHistory

User "0..1" --> "*" AuditLog
```

## Relacje UML

### Asocjacje

| Klasa A | Klasa B | Typ |
|----------|----------|------|
| User | UserProfile | 1:1 |
| Brand | Product | 1:* |
| Category | Product | 1:* |
| Product | ProductVariant | 1:* |
| Product | Review | 1:* |
| User | Review | 1:* |
| User | Order | 1:* |
| Order | OrderItem | 1:* |
| ProductVariant | OrderItem | 1:* |
| Order | OrderStatusHistory | 1:* |
| User | AuditLog | 0..1:* |

## Najważniejsze reguły projektowe

1. Produkt nie przechowuje stanu magazynowego.
2. Stan magazynowy znajduje się na poziomie wariantu.
3. Zamówienie przechowuje snapshot danych dostawy.
4. Opinia jest unikalna dla pary:
   - użytkownik
   - produkt
5. AuditLog jest niezależny od procesu zamówienia.
6. Historia statusów nie nadpisuje wcześniejszych zmian.
