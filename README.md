# Clothing Store – platforma sprzedaży internetowej

## Cel projektu

Projekt przedstawia kompletny system sklepu internetowego zbudowany w technologii Django, PostgreSQL oraz Docker.

Celem projektu było zaprojektowanie i implementacja rozwiązania obejmującego pełny proces sprzedaży internetowej – od przeglądania katalogu produktów, przez składanie i opłacanie zamówień, aż po ich realizację i dostarczenie.

Projekt został wykonany jako przykład połączenia:

* analizy biznesowej,
* analizy systemowej,
* modelowania danych,
* projektowania architektury,
* implementacji backendu,
* projektowania REST API,
* przygotowania dokumentacji technicznej i analitycznej,
* automatyzacji testów.

System został zaprojektowany w sposób umożliwiający jego dalszy rozwój oraz integrację z usługami zewnętrznymi.

---

# Dane dostępowe

## Konto administratora

Login:

```text
admin
```

Hasło:

```text
admin12345
```

## Konto testowe klienta

Login:

```text
testowyk
```

Hasło:

```text
Test123456
```

---

# Uzasadnienie biznesowe projektu

Większość współczesnych sklepów internetowych realizuje podobny proces biznesowy:

1. Prezentacja oferty.
2. Wybór produktu.
3. Dodanie do koszyka.
4. Złożenie zamówienia.
5. Płatność.
6. Realizacja zamówienia.
7. Dostarczenie produktu.

Projekt został przygotowany tak, aby odwzorować ten proces możliwie wiernie przy zachowaniu rozsądnego poziomu złożoności.

Dzięki temu możliwe było przećwiczenie pełnego cyklu projektowania systemu informatycznego.

---

# Zakres funkcjonalny

## Zarządzanie katalogiem produktów

System umożliwia:

* definiowanie marek,
* definiowanie kategorii,
* tworzenie produktów,
* tworzenie wariantów produktów,
* obsługę rozmiarów,
* obsługę kolorów,
* obsługę promocji,
* oznaczanie produktów wyróżnionych.

### Dlaczego zastosowano warianty produktów?

W praktycznych systemach e-commerce produkt oraz jego wariant są odrębnymi bytami biznesowymi.

Przykład:

Produkt:

```text
Nike Air Max
```

Warianty:

```text
42 / Czarny
43 / Czarny
42 / Biały
43 / Biały
```

Pozwala to zarządzać stanami magazynowymi na poziomie konkretnego wariantu.

---

## Koszyk zakupowy

Koszyk przechowywany jest w sesji użytkownika.

### Dlaczego zastosowano sesję?

Na etapie projektu nie było wymagania utrzymywania trwałego koszyka między urządzeniami.

Zastosowanie sesji:

* upraszcza implementację,
* ogranicza liczbę tabel w bazie danych,
* pozwala szybko realizować proces zakupowy.

---

## Zamówienia

System umożliwia:

* tworzenie zamówień,
* przegląd historii zamówień,
* śledzenie statusów,
* przechowywanie danych dostawy.

Przykładowy numer zamówienia:

```text
ORD-2026-000001
```

### Dlaczego dane adresowe są kopiowane do zamówienia?

Adres użytkownika może zmieniać się w czasie.

Zamówienie przechowuje tzw. snapshot danych dostawy, dzięki czemu możliwe jest odtworzenie historycznego stanu zamówienia.

---

## Płatności

Aktualnie zaimplementowano moduł:

```text
Fake BLIK
```

### Dlaczego zastosowano Fake BLIK?

Celem projektu nie było integrowanie się z rzeczywistym operatorem płatności.

Moduł umożliwia jednak pełne przetestowanie procesu:

```text
NEW → PAID
```

oraz przygotowuje system do przyszłej integracji z PayU, Przelewy24 lub Stripe.

---

## Kupony rabatowe

System umożliwia:

* definiowanie kodów rabatowych,
* określanie wysokości rabatu,
* aktywowanie i dezaktywowanie kuponów.

Mechanizm odwzorowuje najczęściej spotykane rozwiązania stosowane w sklepach internetowych.

---

## Opinie o produktach

System umożliwia:

* ocenę produktu w skali 1–5,
* dodawanie komentarzy,
* wyliczanie średniej oceny.

Funkcjonalność wspiera proces podejmowania decyzji zakupowych przez klientów.

---

## Dashboard zarządczy

Dashboard prezentuje:

* liczbę zamówień,
* liczbę klientów,
* liczbę produktów,
* przychód,
* najpopularniejsze produkty,
* najpopularniejsze marki,
* historię działań systemowych.

### Dlaczego dashboard?

Dashboard umożliwia szybkie monitorowanie działania sklepu bez konieczności wykonywania zapytań bezpośrednio do bazy danych.

---

# Role użytkowników

| Rola          | Zakres odpowiedzialności |
| ------------- | ------------------------ |
| Gość          | przeglądanie katalogu    |
| Klient        | składanie zamówień       |
| Magazynier    | realizacja wysyłek       |
| Manager       | analiza sprzedaży        |
| Administrator | administracja systemem   |

### Dlaczego zastosowano role?

Rozdzielenie uprawnień zwiększa bezpieczeństwo oraz pozwala odwzorować rzeczywiste obowiązki użytkowników.

---

# Proces realizacji zamówienia

Statusy zamówienia:

```text
NEW
↓
PAID
↓
SHIPPED
↓
DELIVERED
```

Opis:

* NEW – zamówienie utworzone,
* PAID – zamówienie opłacone,
* SHIPPED – zamówienie wysłane,
* DELIVERED – zamówienie dostarczone.

---

# Architektura rozwiązania

System wykorzystuje architekturę warstwową.

```text
Warstwa prezentacji
        ↓
Warstwa aplikacyjna
        ↓
Warstwa domenowa
        ↓
Warstwa persystencji
        ↓
PostgreSQL
```

### Dlaczego architektura warstwowa?

Pozwala:

* oddzielić logikę biznesową od prezentacji,
* ograniczyć zależności,
* uprościć rozwój systemu,
* zwiększyć testowalność rozwiązania.

---

# Wykorzystane technologie i uzasadnienie wyboru

## Django

Wybrano ze względu na:

* dojrzałość frameworka,
* wbudowany ORM,
* gotowy system autoryzacji,
* panel administracyjny,
* możliwość szybkiego tworzenia aplikacji biznesowych.

## PostgreSQL

Wybrano ze względu na:

* zgodność ACID,
* wysoką stabilność,
* obsługę relacyjnych modeli danych,
* popularność w systemach produkcyjnych.

## Django REST Framework

Wybrano w celu budowy REST API umożliwiającego integrację z aplikacjami zewnętrznymi.

## JWT

Wdrożono w celu przygotowania systemu do komunikacji z klientami mobilnymi i integracjami zewnętrznymi.

## Docker

Wdrożono w celu:

* standaryzacji środowiska,
* uproszczenia wdrożeń,
* eliminacji problemów konfiguracyjnych.

---

# REST API

Publiczne endpointy:

```http
GET /api/products/
GET /api/products/{id}
GET /api/brands/
GET /api/categories/
```

Chronione endpointy:

```http
GET /api/orders/
```

Dostęp realizowany jest przy użyciu JWT.

---

# Dokumentacja API

Swagger:

```text
/api/swagger/
```

Redoc:

```text
/api/redoc/
```

Schema:

```text
/api/schema/
```

---

# Model danych

Główne encje:

* User
* UserProfile
* Brand
* Category
* Product
* ProductVariant
* Review
* Coupon
* Order
* OrderItem
* OrderStatusHistory
* AuditLog

Szczegółowy model danych:

```text
docs/analysis/02_erd.md
```

---

# Testy

Projekt zawiera:

* testy automatyczne,
* testy manualne,
* dane demonstracyjne.

Raport testów:

```text
docs/analysis/06_test_report.md
```

---

# Dane demonstracyjne

W projekcie przygotowano automatyczne zasilenie bazy danych:

* 50 produktów,
* 147 wariantów,
* 20 użytkowników,
* 40 zamówień,
* 201 opinii,
* 4 kupony,
* 100 wpisów AuditLog.

---

# Dokumentacja analityczna

* 01_use_cases.md
* 02_erd.md
* 03_bpmn.md
* 04_class_diagram.md
* 05_component_diagram.md
* 06_test_report.md

---

# Możliwe kierunki rozwoju

* integracja z PayU,
* integracja z Przelewy24,
* integracja z InPost API,
* integracja z TERYT,
* powiadomienia e-mail,
* raporty XLSX,
* GitHub Actions,
* CI/CD,
* Kubernetes.

---

# Autor

Damian Abramczyk

Analityk biznesowo-systemowy

Projekt został przygotowany jako demonstracja umiejętności z zakresu:

* analizy biznesowej,
* analizy systemowej,
* modelowania UML,
* modelowania BPMN,
* projektowania baz danych,
* projektowania REST API,
* implementacji aplikacji Django.
