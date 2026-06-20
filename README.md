# Clothing Store

Kompletny system sklepu internetowego zbudowany w technologii Django, PostgreSQL i Docker.

Projekt został przygotowany jako przykład pełnego rozwiązania biznesowo-systemowego obejmującego analizę biznesową, model danych, architekturę systemu, implementację backendu, REST API, uwierzytelnianie JWT, testy automatyczne oraz dokumentację projektową.

Logowanie:
Konto administratora:
login: admin 
hasło: admin12345

Kontro testowe:
login: testowyk
hasło: Test123456

---

# Business Overview

Celem systemu jest obsługa sprzedaży produktów odzieżowych online.

System umożliwia:

* zarządzanie katalogiem produktów,
* obsługę klientów,
* realizację zamówień,
* stosowanie kuponów rabatowych,
* ocenianie produktów,
* monitorowanie procesu realizacji zamówień,
* udostępnianie danych przez REST API.

Projekt został przygotowany w sposób zbliżony do rzeczywistych systemów e-commerce.

---

# Functional Scope

## Katalog produktów

* marki produktów,
* kategorie produktów,
* warianty produktów,
* rozmiary,
* kolory,
* promocje,
* produkty wyróżnione.

## Koszyk

* dodawanie produktów,
* usuwanie produktów,
* walidacja stanów magazynowych,
* przechowywanie koszyka w sesji.

## Zamówienia

* checkout,
* historia zamówień,
* szczegóły zamówień,
* numer zamówienia:

```text
ORD-2026-000001
```

* historia statusów.

## Płatności

Aktualna implementacja:

```text
Fake BLIK
```

Obsługiwane statusy:

```text
NEW
PAID
SHIPPED
DELIVERED
```

## Kupony rabatowe

* rabaty procentowe,
* aktywacja/dezaktywacja kuponów,
* automatyczne przeliczanie koszyka.

## Opinie

* oceny 1–5,
* komentarze,
* średnia ocena produktu.

## Dashboard

* liczba zamówień,
* liczba klientów,
* liczba produktów,
* przychód,
* top produkty,
* top marki,
* AuditLog.

## REST API

* produkty,
* marki,
* kategorie,
* zamówienia.

## Swagger / OpenAPI

* Swagger UI,
* Redoc,
* OpenAPI Schema.

---

# User Roles

## CUSTOMER

Klient sklepu.

Uprawnienia:

* przeglądanie produktów,
* składanie zamówień,
* płatność,
* opinie,
* historia zamówień.

## WAREHOUSE

Pracownik magazynu.

Uprawnienia:

* wysyłka zamówień,
* nadawanie numerów przesyłek,
* oznaczanie dostarczenia.

## MANAGER

Kierownik sklepu.

Uprawnienia:

* dashboard,
* raportowanie,
* analiza sprzedaży.

## ADMIN

Administrator systemu.

Uprawnienia:

* pełna administracja systemem.

---

# Business Processes

## Rejestracja użytkownika

1. Rejestracja.
2. Utworzenie profilu.
3. Automatyczne logowanie.

## Zakup produktu

1. Wybór produktu.
2. Dodanie do koszyka.
3. Checkout.
4. Utworzenie zamówienia.

## Płatność

```text
NEW → PAID
```

## Realizacja zamówienia

```text
PAID → SHIPPED → DELIVERED
```

---

# Data Model

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

Pełny model danych znajduje się w:

```text
docs/analysis/02_erd.md
```

---

# Architecture

Architektura warstwowa:

```text
Presentation Layer
↓
Application Layer
↓
Domain Layer
↓
Persistence Layer
↓
PostgreSQL
```

Dokumentacja architektury:

```text
docs/analysis/05_component_diagram.md
```

---

# Technology Stack

## Backend

* Python 3.12+
* Django
* Django REST Framework
* SimpleJWT

## Database

* PostgreSQL

## API Documentation

* Swagger
* Redoc
* drf-spectacular

## Tests

* Django Test Framework
* APITestCase

## Containerization

* Docker
* Docker Compose

---

# JWT Authentication

Pobranie tokena:

```http
POST /api/token/
```

Odświeżenie tokena:

```http
POST /api/token/refresh/
```

Przykład:

```json
{
  "username": "user",
  "password": "password"
}
```

Odpowiedź:

```json
{
  "refresh": "...",
  "access": "..."
}
```

---

# REST API

## Public

```http
GET /api/products/
GET /api/products/{id}/

GET /api/brands/
GET /api/categories/
```

## Protected

```http
GET /api/orders/
```

JWT wymagany.

---

# Swagger

Dokumentacja API:

```text
/api/swagger/
/api/redoc/
/api/schema/
```

---

# Automated Tests

Zakres testów:

* modele,
* autoryzacja,
* JWT,
* zamówienia,
* kupony,
* opinie,
* dashboard,
* checkout,
* REST API.

Uruchomienie:

```bash
docker compose exec web python manage.py test
```

---

# Docker

Budowa:

```bash
docker compose build
```

Uruchomienie:

```bash
docker compose up -d
```

Zatrzymanie:

```bash
docker compose down
```

---

# Local Installation

## 1. Klonowanie repozytorium

```bash
git clone <repository_url>
cd django-sklep
```

## 2. Docker

```bash
docker compose up -d --build
```

## 3. Migracje

```bash
docker compose exec web python manage.py migrate
```

## 4. Superuser

```bash
docker compose exec web python manage.py createsuperuser
```

## 5. Uruchomienie

```text
http://localhost:8000
```

---

# Documentation

## Use Cases

```text
docs/analysis/01_use_cases.md
```

## ERD

```text
docs/analysis/02_erd.md
```

## BPMN

```text
docs/analysis/03_bpmn.md
```

## UML Class Diagram

```text
docs/analysis/04_class_diagram.md
```

## Component Diagram

```text
docs/analysis/05_component_diagram.md
```

---

# Roadmap

Planowane rozszerzenia:

* Przelewy24
* Stripe
* Email Notifications
* GitHub Actions
* CI/CD
* Eksport XLSX
* Raporty sprzedaży
* Wykresy sprzedaży
* Nginx + Gunicorn
* Kubernetes

---

# Author

Damian Abramczyk

Business & System Analyst

Technologie:

* Django
* PostgreSQL
* Docker
* REST API
* JWT
* UML
* BPMN
* BABOK
* Analiza biznesowa
* Analiza systemowa

