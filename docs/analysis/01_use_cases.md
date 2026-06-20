# Przypadki użycia — Clothing Store

## Aktorzy

| Aktor | Opis |
|---|---|
| Gość | Niezalogowany użytkownik sklepu |
| Klient | Zalogowany użytkownik z rolą CUSTOMER |
| Magazynier | Użytkownik z rolą WAREHOUSE lub staff |
| Manager | Użytkownik z rolą MANAGER |
| Administrator | Użytkownik z rolą ADMIN lub superuser |
| System | Aplikacja Django wykonująca automatyczne operacje |

---

## UC-01 Rejestracja użytkownika

**Aktor główny:** Gość  
**Cel:** Utworzenie konta klienta.

### Warunki początkowe
- Użytkownik nie jest zalogowany.

### Scenariusz główny
1. Użytkownik przechodzi do `/register/`.
2. System wyświetla formularz rejestracji.
3. Użytkownik podaje login, email i hasło.
4. System waliduje dane.
5. System tworzy konto użytkownika.
6. System tworzy profil użytkownika.
7. System loguje użytkownika.
8. System przekierowuje użytkownika na profil.

### Scenariusze alternatywne
- A1: Login jest zajęty — system zwraca błąd formularza.
- A2: Hasła nie są zgodne — system zwraca błąd formularza.

### Wynik
- Konto użytkownika istnieje w systemie.
- Użytkownik jest zalogowany.

---

## UC-02 Logowanie użytkownika

**Aktor główny:** Gość  
**Cel:** Uzyskanie dostępu do funkcji klienta.

### Scenariusz główny
1. Użytkownik przechodzi do `/login/`.
2. System wyświetla formularz logowania.
3. Użytkownik podaje login i hasło.
4. System uwierzytelnia użytkownika.
5. System przekierowuje użytkownika na profil.

### Scenariusze alternatywne
- A1: Dane są błędne — system pokazuje błąd logowania.

---

## UC-03 Edycja profilu i adresu dostawy

**Aktor główny:** Klient  
**Cel:** Uzupełnienie danych kontaktowych i adresowych.

### Scenariusz główny
1. Klient przechodzi do `/profile/edit/`.
2. System pokazuje formularz danych użytkownika i adresu.
3. Klient uzupełnia imię, nazwisko, email, telefon, ulicę, kod pocztowy i miasto.
4. System zapisuje dane.
5. System pokazuje komunikat KS_03.

### Wynik
- Profil klienta zawiera dane potrzebne do zamówienia.

---

## UC-04 Przeglądanie produktów

**Aktor główny:** Gość/Klient  
**Cel:** Przeglądanie oferty sklepu.

### Scenariusz główny
1. Użytkownik przechodzi do `/products/`.
2. System pobiera produkty, marki, kategorie i warianty.
3. System prezentuje listę produktów.
4. Użytkownik może przejść do szczegółów produktu.

---

## UC-05 Wyszukiwanie produktów

**Aktor główny:** Gość/Klient  
**Cel:** Znalezienie produktu po nazwie, marce lub kategorii.

### Scenariusz główny
1. Użytkownik wpisuje tekst w wyszukiwarce.
2. System filtruje produkty po nazwie, marce lub kategorii.
3. System pokazuje wyniki.
4. System pokazuje komunikat KI_01.

---

## UC-06 Filtrowanie produktów

**Aktor główny:** Gość/Klient  
**Cel:** Zawężenie listy produktów.

### Kryteria filtrowania
- Marka
- Kategoria
- Rozmiar

### Scenariusz główny
1. Użytkownik wybiera filtr.
2. System filtruje listę produktów.
3. System pokazuje przefiltrowane wyniki.
4. System pokazuje komunikat KI_01.

---

## UC-07 Dodanie produktu do koszyka

**Aktor główny:** Gość/Klient  
**Cel:** Dodanie wybranego wariantu produktu do koszyka.

### Scenariusz główny
1. Użytkownik wybiera wariant produktu.
2. Użytkownik podaje ilość.
3. System sprawdza poprawność ilości.
4. System sprawdza dostępny stan magazynowy.
5. System zapisuje produkt w koszyku sesyjnym.
6. System pokazuje komunikat KS_01.

### Scenariusze alternatywne
- A1: Ilość mniejsza od 1 — system pokazuje KB_01.
- A2: Ilość przekracza stan magazynowy — system pokazuje KB_02.

---

## UC-08 Usunięcie produktu z koszyka

**Aktor główny:** Gość/Klient  
**Cel:** Zmniejszenie liczby sztuk lub usunięcie pozycji z koszyka.

### Scenariusz główny
1. Użytkownik przechodzi do `/cart/`.
2. Użytkownik wskazuje liczbę sztuk do usunięcia.
3. System zmniejsza ilość produktu w koszyku.
4. System pokazuje KI_02.

### Scenariusz alternatywny
- A1: Użytkownik usuwa liczbę równą lub większą niż w koszyku — system usuwa całą pozycję.

---

## UC-09 Zastosowanie kuponu rabatowego

**Aktor główny:** Gość/Klient  
**Cel:** Obniżenie wartości koszyka.

### Scenariusz główny
1. Użytkownik wpisuje kod kuponu.
2. System sprawdza, czy kupon istnieje i jest aktywny.
3. System zapisuje kupon w sesji.
4. System przelicza wartość koszyka.
5. System pokazuje KS_09.

### Scenariusz alternatywny
- A1: Kupon nie istnieje albo jest nieaktywny — system pokazuje KB_10.

---

## UC-10 Złożenie zamówienia

**Aktor główny:** Klient  
**Cel:** Utworzenie zamówienia z koszyka.

### Warunki początkowe
- Klient jest zalogowany.
- Koszyk nie jest pusty.
- Klient ma uzupełniony telefon i adres dostawy.

### Scenariusz główny
1. Klient przechodzi do koszyka.
2. Klient klika „Złóż zamówienie”.
3. System sprawdza koszyk.
4. System sprawdza dane dostawy.
5. System tworzy zamówienie.
6. System tworzy pozycje zamówienia.
7. System zapisuje snapshot adresu.
8. System zmniejsza stany magazynowe.
9. System czyści koszyk i kupon.
10. System pokazuje KS_02.

### Scenariusze alternatywne
- A1: Koszyk pusty — KB_03.
- A2: Brak danych dostawy — KB_07.
- A3: Brak stanu magazynowego — KB_05.

---

## UC-11 Opłacenie zamówienia Fake BLIK

**Aktor główny:** Klient  
**Cel:** Zmiana statusu zamówienia z NOWE na OPŁACONE.

### Scenariusz główny
1. Klient otwiera szczegóły zamówienia.
2. System pokazuje formularz kodu BLIK.
3. Klient wpisuje 6-cyfrowy kod.
4. System waliduje kod.
5. System zmienia status na PAID.
6. System zapisuje historię statusu.
7. System zapisuje AuditLog.
8. System pokazuje KS_06.

### Scenariusz alternatywny
- A1: Kod nie ma 6 cyfr — KB_09.
- A2: Zamówienie nie ma statusu NEW — KO_01.

---

## UC-12 Wysłanie zamówienia

**Aktor główny:** Magazynier/Admin  
**Cel:** Oznaczenie opłaconego zamówienia jako wysłane.

### Warunki początkowe
- Użytkownik ma rolę staff/warehouse/admin.
- Zamówienie ma status PAID.

### Scenariusz główny
1. Pracownik otwiera szczegóły zamówienia.
2. System pokazuje panel pracownika.
3. Pracownik wpisuje numer przesyłki.
4. System zapisuje numer przesyłki.
5. System zmienia status na SHIPPED.
6. System zapisuje historię statusu.
7. System zapisuje AuditLog.
8. System pokazuje KS_07.

### Scenariusze alternatywne
- A1: Brak uprawnień — KB_06.
- A2: Status inny niż PAID — KO_02.
- A3: Brak numeru przesyłki — KB_08.

---

## UC-13 Oznaczenie zamówienia jako dostarczone

**Aktor główny:** Magazynier/Admin  
**Cel:** Zakończenie procesu dostawy.

### Scenariusz główny
1. Pracownik otwiera szczegóły zamówienia.
2. System sprawdza uprawnienia.
3. System sprawdza, czy status to SHIPPED.
4. Pracownik klika „Oznacz jako dostarczone”.
5. System zmienia status na DELIVERED.
6. System zapisuje historię statusu.
7. System zapisuje AuditLog.
8. System pokazuje KS_08.

### Scenariusze alternatywne
- A1: Brak uprawnień — KB_06.
- A2: Status inny niż SHIPPED — KO_03.

---

## UC-14 Dodanie opinii o produkcie

**Aktor główny:** Klient  
**Cel:** Dodanie oceny produktu 1–5.

### Scenariusz główny
1. Klient otwiera szczegóły produktu.
2. Klient wpisuje ocenę i komentarz.
3. System waliduje ocenę.
4. System zapisuje opinię.
5. System aktualizuje średnią ocenę produktu.
6. System pokazuje KS_11.

### Scenariusz alternatywny
- A1: Klient próbuje dodać drugą opinię do tego samego produktu — KB_11.

---

## UC-15 Przegląd historii zamówień

**Aktor główny:** Klient  
**Cel:** Wgląd w swoje zamówienia.

### Scenariusz główny
1. Klient przechodzi do `/orders/`.
2. System pobiera zamówienia klienta.
3. System pokazuje numery ORD, statusy i daty.
4. Klient przechodzi do szczegółów zamówienia.

---

## UC-16 Przegląd szczegółów zamówienia

**Aktor główny:** Klient  
**Cel:** Sprawdzenie produktów, statusu, dostawy i historii statusów.

### Scenariusz główny
1. Klient otwiera szczegóły zamówienia.
2. System pokazuje numer zamówienia.
3. System pokazuje status.
4. System pokazuje produkty.
5. System pokazuje dane dostawy.
6. System pokazuje historię statusów.

---

## UC-17 Przegląd dashboardu sklepu

**Aktor główny:** Manager/Admin  
**Cel:** Analiza sprzedaży i aktywności systemu.

### Scenariusz główny
1. Manager przechodzi do `/dashboard/`.
2. System sprawdza uprawnienia.
3. System pokazuje liczbę zamówień.
4. System pokazuje przychód.
5. System pokazuje liczbę produktów i klientów.
6. System pokazuje top produkty.
7. System pokazuje top marki.
8. System pokazuje ostatnie wpisy AuditLog.

### Scenariusz alternatywny
- A1: Brak uprawnień — KB_06.

---

## UC-18 Zarządzanie produktami w adminie

**Aktor główny:** Administrator/Manager  
**Cel:** Zarządzanie katalogiem produktów.

### Scenariusz główny
1. Administrator loguje się do `/admin/`.
2. Administrator tworzy lub edytuje markę.
3. Administrator tworzy lub edytuje kategorię.
4. Administrator tworzy produkt.
5. Administrator dodaje warianty produktu.
6. Administrator ustawia cenę, promocję, stock i zdjęcie.

---

## UC-19 Zarządzanie kuponami

**Aktor główny:** Administrator/Manager  
**Cel:** Tworzenie i dezaktywacja kuponów.

### Scenariusz główny
1. Administrator przechodzi do admina.
2. Administrator tworzy kupon.
3. Administrator ustawia procent rabatu.
4. Administrator ustawia aktywność kuponu.

---

## UC-20 Dostęp do API JWT

**Aktor główny:** Klient/System zewnętrzny  
**Cel:** Uzyskanie tokena JWT i dostęp do chronionego API.

### Scenariusz główny
1. Klient wysyła POST na `/api/token/`.
2. System waliduje login i hasło.
3. System zwraca access token i refresh token.
4. Klient używa access tokena do `/api/orders/`.
5. System zwraca zamówienia klienta.

### Scenariusze alternatywne
- A1: Brak tokena — API zwraca 401.
- A2: Niepoprawny token — API zwraca 401.

---

## UC-21 Przegląd API produktów

**Aktor główny:** Gość/System zewnętrzny  
**Cel:** Pobranie danych katalogowych.

### Endpointy
- `/api/products/`
- `/api/products/{id}/`
- `/api/brands/`
- `/api/categories/`

### Wynik
- System zwraca dane JSON.

---

## UC-22 Przegląd dokumentacji API

**Aktor główny:** Developer/Analityk  
**Cel:** Przegląd kontraktu API.

### Endpointy
- `/api/swagger/`
- `/api/redoc/`
- `/api/schema/`
