# 06. Raport z testów

## 1. Cel dokumentu

Celem raportu jest uporządkowanie wyników testów projektu **Clothing Store** oraz przedstawienie pełnej listy scenariuszy testowych wykorzystanych do weryfikacji systemu.

Raport obejmuje testy automatyczne oraz testy manualne dla obszarów:

- użytkownicy i profile,
- logowanie oraz JWT,
- katalog produktów,
- koszyk,
- kupony rabatowe,
- checkout,
- zamówienia,
- płatność Fake BLIK,
- opinie,
- dashboard,
- REST API,
- AuditLog.


## 2. Zakres i uporządkowanie raportu

W poprzedniej wersji dokumentu występowały powtórzone nagłówki, zdublowane fragmenty wstępu oraz starsza skrócona lista scenariuszy. W tej wersji usunięto duplikaty tekstu i pozostawiono jeden spójny raport.

Liczba scenariuszy pozostaje niezmieniona:

| Rodzaj testów | Zakres identyfikatorów | Liczba |
|---|---:|---:|
| Testy automatyczne | TC_AUTO_001–TC_AUTO_055 | 55 |
| Testy manualne | TC_MAN_001–TC_MAN_045 | 45 |
| Łącznie | — | 100 |


## 3. Założenia testowe

Testy automatyczne opisują przypadki możliwe do weryfikacji przez testy jednostkowe, integracyjne oraz testy API. Testy manualne opisują przebieg pracy użytkownika w interfejsie WWW.

Dla każdego scenariusza zastosowano jednolitą strukturę:

- cel,
- warunki wstępne,
- dane testowe,
- przebieg,
- oczekiwany rezultat,
- wynik.


## 4. Testy automatyczne

### 4.1. Moduł użytkowników i JWT

### TC_AUTO_001 – Rejestracja użytkownika

**Cel:** Potwierdzenie, że system umożliwia utworzenie konta użytkownika.

**Warunki wstępne:** Brak użytkownika o wskazanym loginie.

**Dane testowe:** login: auto_user, hasło: Test123456

**Przebieg:**
1. Utworzyć nowego użytkownika przez mechanizm testowy Django.
2. Zapisać użytkownika w bazie testowej.
3. Odczytać użytkownika po loginie.
4. Zweryfikować podstawowe pola konta.

**Oczekiwany rezultat:** Użytkownik zostaje utworzony, posiada identyfikator i może zostać odczytany z bazy.

**Wynik:** PASSED

---

### TC_AUTO_002 – Logowanie użytkownika

**Cel:** Weryfikacja poprawnej autoryzacji dla istniejącego konta.

**Warunki wstępne:** Istnieje aktywne konto użytkownika.

**Dane testowe:** login: auto_user, hasło: Test123456

**Przebieg:**
1. Utworzyć użytkownika testowego.
2. Wywołać logowanie z poprawnym loginem i hasłem.
3. Odczytać wynik logowania.
4. Sprawdzić, czy sesja została utworzona.

**Oczekiwany rezultat:** System poprawnie uwierzytelnia użytkownika.

**Wynik:** PASSED

---

### TC_AUTO_003 – Niepoprawne logowanie

**Cel:** Weryfikacja odmowy dostępu przy błędnym haśle.

**Warunki wstępne:** Istnieje aktywne konto użytkownika.

**Dane testowe:** login: auto_user, hasło: WrongPassword

**Przebieg:**
1. Utworzyć użytkownika testowego.
2. Wywołać logowanie z błędnym hasłem.
3. Odczytać wynik logowania.
4. Sprawdzić brak uwierzytelnionej sesji.

**Oczekiwany rezultat:** System odmawia logowania i nie tworzy sesji użytkownika.

**Wynik:** PASSED

---

### TC_AUTO_004 – Tworzenie profilu użytkownika

**Cel:** Potwierdzenie relacji jeden-do-jednego pomiędzy User i UserProfile.

**Warunki wstępne:** Istnieje użytkownik bez profilu albo tworzony jest nowy użytkownik.

**Dane testowe:** rola: CUSTOMER, telefon i adres testowy

**Przebieg:**
1. Utworzyć użytkownika.
2. Utworzyć profil powiązany z użytkownikiem.
3. Odczytać profil przez relację użytkownika.
4. Sprawdzić rolę oraz dane adresowe.

**Oczekiwany rezultat:** Profil zostaje utworzony i jest jednoznacznie powiązany z użytkownikiem.

**Wynik:** PASSED

---

### TC_AUTO_005 – Aktualizacja profilu

**Cel:** Sprawdzenie zapisu zmian danych profilu użytkownika.

**Warunki wstępne:** Istnieje użytkownik z profilem.

**Dane testowe:** nowy telefon, ulica, kod pocztowy i miasto

**Przebieg:**
1. Odczytać profil użytkownika.
2. Zmienić dane kontaktowe i adresowe.
3. Zapisać profil.
4. Odczytać profil ponownie z bazy.

**Oczekiwany rezultat:** Zmiany w profilu są zapisane i widoczne po ponownym odczycie.

**Wynik:** PASSED

---

### TC_AUTO_006 – Pobranie tokena JWT

**Cel:** Weryfikacja endpointu wydającego token JWT.

**Warunki wstępne:** Istnieje aktywne konto użytkownika.

**Dane testowe:** POST /api/token/, poprawny login i hasło

**Przebieg:**
1. Utworzyć użytkownika.
2. Wysłać żądanie POST do /api/token/.
3. Odczytać odpowiedź API.
4. Sprawdzić obecność tokena access.

**Oczekiwany rezultat:** API zwraca poprawny access token.

**Wynik:** PASSED

---

### TC_AUTO_007 – Pobranie refresh token

**Cel:** Sprawdzenie, czy endpoint JWT zwraca refresh token.

**Warunki wstępne:** Istnieje aktywne konto użytkownika.

**Dane testowe:** POST /api/token/, poprawny login i hasło

**Przebieg:**
1. Utworzyć użytkownika.
2. Wysłać żądanie do endpointu JWT.
3. Odczytać payload odpowiedzi.
4. Sprawdzić obecność pola refresh.

**Oczekiwany rezultat:** API zwraca refresh token możliwy do późniejszego użycia.

**Wynik:** PASSED

---

### TC_AUTO_008 – Odświeżenie access token

**Cel:** Weryfikacja odświeżenia access tokena na podstawie refresh tokena.

**Warunki wstępne:** Istnieje poprawny refresh token.

**Dane testowe:** POST /api/token/refresh/

**Przebieg:**
1. Pobrać parę tokenów.
2. Wysłać refresh token do /api/token/refresh/.
3. Odczytać odpowiedź.
4. Zweryfikować nowy access token.

**Oczekiwany rezultat:** System zwraca nowy access token.

**Wynik:** PASSED

---

### TC_AUTO_009 – Dostęp bez JWT

**Cel:** Sprawdzenie blokady dostępu do chronionego endpointu bez tokena.

**Warunki wstępne:** Endpoint /api/orders/ wymaga uwierzytelnienia.

**Dane testowe:** brak nagłówka Authorization

**Przebieg:**
1. Wysłać anonimowe żądanie GET /api/orders/.
2. Odczytać kod odpowiedzi.
3. Sprawdzić brak danych zamówień w odpowiedzi.

**Oczekiwany rezultat:** System zwraca odmowę dostępu, oczekiwany status HTTP 401.

**Wynik:** PASSED

---

### TC_AUTO_010 – Dostęp z JWT

**Cel:** Sprawdzenie dostępu do chronionego endpointu po poprawnym uwierzytelnieniu.

**Warunki wstępne:** Istnieje użytkownik i ważny access token.

**Dane testowe:** Authorization: Bearer <access>

**Przebieg:**
1. Pobrać token JWT.
2. Wysłać GET /api/orders/ z nagłówkiem Authorization.
3. Odczytać kod odpowiedzi.
4. Sprawdzić strukturę zwróconych danych.

**Oczekiwany rezultat:** System zwraca HTTP 200 i dane zamówień użytkownika.

**Wynik:** PASSED

---

### 4.2. Moduł produktów

### TC_AUTO_011 – Utworzenie marki

**Cel:** Potwierdzenie, że model marki zapisuje i odczytuje dane biznesowe.

**Warunki wstępne:** W bazie testowej nie istnieje marka o tej samej nazwie.

**Dane testowe:** name="Nike"

**Przebieg:**
1. Utworzyć obiekt Brand.
2. Zapisać obiekt do bazy.
3. Odczytać obiekt po identyfikatorze albo nazwie.
4. Porównać wartość pola name z danymi wejściowymi.

**Oczekiwany rezultat:** Marka zostaje zapisana, a nazwa jest zgodna z danymi testowymi.

**Wynik:** PASSED

---

### TC_AUTO_012 – Utworzenie kategorii

**Cel:** Potwierdzenie, że model kategorii umożliwia zapis i odczyt danych.

**Warunki wstępne:** Brak kategorii o tej samej nazwie.

**Dane testowe:** name="Koszulki"

**Przebieg:**
1. Utworzyć obiekt Category.
2. Zapisać kategorię w bazie.
3. Odczytać kategorię.
4. Zweryfikować pole name.

**Oczekiwany rezultat:** Kategoria zostaje zapisana i jest dostępna w bazie.

**Wynik:** PASSED

---

### TC_AUTO_013 – Utworzenie produktu

**Cel:** Weryfikacja utworzenia produktu powiązanego z marką i kategorią.

**Warunki wstępne:** Istnieje marka i kategoria.

**Dane testowe:** produkt: Air Tee, marka: Nike, kategoria: Koszulki

**Przebieg:**
1. Utworzyć markę.
2. Utworzyć kategorię.
3. Utworzyć produkt z relacjami do marki i kategorii.
4. Odczytać produkt i sprawdzić relacje.

**Oczekiwany rezultat:** Produkt istnieje w bazie i wskazuje prawidłową markę oraz kategorię.

**Wynik:** PASSED

---

### TC_AUTO_014 – Utworzenie wariantu produktu

**Cel:** Potwierdzenie, że wariant produktu może zostać zapisany jako odrębny rekord zależny od produktu.

**Warunki wstępne:** Istnieje produkt bazowy.

**Dane testowe:** rozmiar M, kolor Czarny, cena 100.00, stock 10

**Przebieg:**
1. Utworzyć produkt.
2. Utworzyć wariant powiązany z produktem.
3. Zapisać wariant.
4. Odczytać wariant i sprawdzić pola.

**Oczekiwany rezultat:** Wariant zostaje zapisany i jest powiązany z produktem nadrzędnym.

**Wynik:** PASSED

---

### TC_AUTO_015 – Relacja produkt–wariant

**Cel:** Weryfikacja relacji jeden-do-wielu pomiędzy produktem a wariantami.

**Warunki wstępne:** Istnieje produkt.

**Dane testowe:** dwa warianty tego samego produktu

**Przebieg:**
1. Utworzyć produkt.
2. Utworzyć dwa warianty dla tego produktu.
3. Odczytać warianty przez relację odwrotną.
4. Sprawdzić liczbę i identyfikatory wariantów.

**Oczekiwany rezultat:** Produkt zwraca komplet przypisanych wariantów.

**Wynik:** PASSED

---

### TC_AUTO_016 – Pobranie listy produktów

**Cel:** Weryfikacja endpointu API zwracającego listę produktów.

**Warunki wstępne:** W bazie istnieje co najmniej jeden produkt.

**Dane testowe:** GET /api/products/

**Przebieg:**
1. Przygotować dane katalogowe.
2. Wysłać żądanie GET /api/products/.
3. Odczytać kod odpowiedzi.
4. Sprawdzić obecność produktów w payloadzie.

**Oczekiwany rezultat:** Endpoint zwraca HTTP 200 i listę produktów.

**Wynik:** PASSED

---

### TC_AUTO_017 – Pobranie szczegółów produktu

**Cel:** Weryfikacja endpointu API zwracającego dane pojedynczego produktu.

**Warunki wstępne:** Istnieje produkt o znanym ID.

**Dane testowe:** GET /api/products/{id}/

**Przebieg:**
1. Utworzyć produkt.
2. Wysłać GET /api/products/{id}/.
3. Odczytać odpowiedź.
4. Porównać dane z rekordem w bazie.

**Oczekiwany rezultat:** Endpoint zwraca HTTP 200 i szczegóły wskazanego produktu.

**Wynik:** PASSED

---

### TC_AUTO_018 – Obliczenie średniej ocen

**Cel:** Weryfikacja wyliczenia średniej oceny produktu.

**Warunki wstępne:** Istnieje produkt i opinie.

**Dane testowe:** oceny: 5, 4, 3

**Przebieg:**
1. Utworzyć produkt.
2. Dodać trzy opinie.
3. Wywołać właściwość albo metodę liczącą średnią.
4. Porównać wynik z obliczeniem ręcznym.

**Oczekiwany rezultat:** Średnia ocen wynosi 4.0.

**Wynik:** PASSED

---

### TC_AUTO_019 – Obliczenie liczby opinii

**Cel:** Weryfikacja wyliczenia liczby opinii produktu.

**Warunki wstępne:** Istnieje produkt i kilka opinii.

**Dane testowe:** cztery opinie dla jednego produktu

**Przebieg:**
1. Utworzyć produkt.
2. Dodać cztery opinie.
3. Wywołać właściwość albo zapytanie zliczające opinie.
4. Porównać wynik z liczbą rekordów.

**Oczekiwany rezultat:** Liczba opinii wynosi 4.

**Wynik:** PASSED

---

### TC_AUTO_020 – Produkt promowany

**Cel:** Weryfikacja oznaczania produktu jako wyróżnionego.

**Warunki wstępne:** Istnieją dwa produkty.

**Dane testowe:** produkt A: is_featured=True, produkt B: is_featured=False

**Przebieg:**
1. Utworzyć dwa produkty.
2. Ustawić flagę promowania dla jednego z nich.
3. Odczytać produkty z bazy albo API.
4. Sprawdzić wartość pola is_featured.

**Oczekiwany rezultat:** Tylko produkt oznaczony jako promowany ma aktywną flagę wyróżnienia.

**Wynik:** PASSED

---

### 4.3. Moduł koszyka

### TC_AUTO_021 – Dodanie produktu do koszyka

**Cel:** Potwierdzenie dodania pojedynczego wariantu do koszyka sesyjnego.

**Warunki wstępne:** Istnieje wariant z dodatnim stanem magazynowym.

**Dane testowe:** wariant ID, ilość 1

**Przebieg:**
1. Utworzyć produkt i wariant.
2. Zainicjalizować pustą sesję koszyka.
3. Dodać wariant do koszyka.
4. Odczytać zawartość sesji.

**Oczekiwany rezultat:** Koszyk zawiera wskazany wariant w ilości 1.

**Wynik:** PASSED

---

### TC_AUTO_022 – Dodanie wielu produktów

**Cel:** Weryfikacja przechowywania wielu pozycji w koszyku.

**Warunki wstępne:** Istnieją co najmniej dwa warianty.

**Dane testowe:** wariant A x1, wariant B x2

**Przebieg:**
1. Utworzyć dwa warianty.
2. Dodać pierwszy wariant.
3. Dodać drugi wariant.
4. Odczytać sesję koszyka.

**Oczekiwany rezultat:** Koszyk zawiera dwie odrębne pozycje z poprawnymi ilościami.

**Wynik:** PASSED

---

### TC_AUTO_023 – Usunięcie produktu

**Cel:** Sprawdzenie usunięcia pozycji z koszyka.

**Warunki wstępne:** Koszyk zawiera jedną pozycję.

**Dane testowe:** wariant ID w koszyku

**Przebieg:**
1. Dodać wariant do koszyka.
2. Wywołać operację usunięcia.
3. Odczytać koszyk po operacji.
4. Sprawdzić brak pozycji.

**Oczekiwany rezultat:** Usunięta pozycja nie występuje w koszyku.

**Wynik:** PASSED

---

### TC_AUTO_024 – Zmniejszenie ilości

**Cel:** Weryfikacja zmniejszenia ilości pozycji bez całkowitego usuwania.

**Warunki wstępne:** Koszyk zawiera wariant w ilości większej niż 1.

**Dane testowe:** ilość początkowa 3, usuwana ilość 1

**Przebieg:**
1. Ustawić w koszyku wariant w ilości 3.
2. Wywołać zmniejszenie ilości o 1.
3. Odczytać koszyk.
4. Zweryfikować pozostałą ilość.

**Oczekiwany rezultat:** Ilość pozycji zmniejsza się do 2.

**Wynik:** PASSED

---

### TC_AUTO_025 – Walidacja stock

**Cel:** Potwierdzenie blokady ilości większej niż dostępny stan magazynowy.

**Warunki wstępne:** Wariant ma ograniczony stock.

**Dane testowe:** stock 2, próba dodania 3 sztuk

**Przebieg:**
1. Utworzyć wariant ze stockiem 2.
2. Spróbować dodać 3 sztuki do koszyka.
3. Odczytać komunikat albo wynik operacji.
4. Sprawdzić stan koszyka.

**Oczekiwany rezultat:** System nie pozwala utrzymać w koszyku ilości większej niż stock.

**Wynik:** PASSED

---

### TC_AUTO_026 – Walidacja ilości minimalnej

**Cel:** Weryfikacja niedopuszczenia ilości mniejszej niż 1.

**Warunki wstępne:** Koszyk albo formularz przyjmuje ilość produktu.

**Dane testowe:** ilość 0 albo -1

**Przebieg:**
1. Przygotować wariant produktu.
2. Spróbować ustawić ilość 0 albo ujemną.
3. Wywołać walidację.
4. Odczytać wynik.

**Oczekiwany rezultat:** System odrzuca niepoprawną ilość i nie tworzy pozycji koszyka.

**Wynik:** PASSED

---

### TC_AUTO_027 – Wyliczenie wartości koszyka

**Cel:** Sprawdzenie poprawnego sumowania pozycji koszyka.

**Warunki wstępne:** Koszyk zawiera co najmniej dwie pozycje.

**Dane testowe:** 100.00 x2 oraz 50.00 x1

**Przebieg:**
1. Dodać dwie pozycje do koszyka.
2. Wywołać funkcję kalkulującą koszyk.
3. Odczytać subtotal.
4. Porównać z obliczeniem ręcznym.

**Oczekiwany rezultat:** Suma koszyka wynosi 250.00.

**Wynik:** PASSED

---

### 4.4. Moduł kuponów

### TC_AUTO_028 – Utworzenie kuponu

**Cel:** Weryfikacja zapisu kuponu rabatowego.

**Warunki wstępne:** Nie istnieje kupon o tym samym kodzie.

**Dane testowe:** SALE10, rabat 10%, aktywny

**Przebieg:**
1. Utworzyć rekord Coupon.
2. Zapisać go w bazie.
3. Odczytać kupon.
4. Sprawdzić kod, procent i aktywność.

**Oczekiwany rezultat:** Kupon zostaje zapisany z poprawnymi parametrami.

**Wynik:** PASSED

---

### TC_AUTO_029 – Aktywacja kuponu

**Cel:** Sprawdzenie zmiany statusu kuponu na aktywny.

**Warunki wstępne:** Istnieje kupon nieaktywny.

**Dane testowe:** is_active: False -> True

**Przebieg:**
1. Utworzyć nieaktywny kupon.
2. Zmienić pole is_active na True.
3. Zapisać rekord.
4. Odczytać kupon ponownie.

**Oczekiwany rezultat:** Kupon jest oznaczony jako aktywny.

**Wynik:** PASSED

---

### TC_AUTO_030 – Dezaktywacja kuponu

**Cel:** Sprawdzenie zmiany statusu kuponu na nieaktywny.

**Warunki wstępne:** Istnieje kupon aktywny.

**Dane testowe:** is_active: True -> False

**Przebieg:**
1. Utworzyć aktywny kupon.
2. Zmienić pole is_active na False.
3. Zapisać rekord.
4. Zweryfikować odczytaną wartość.

**Oczekiwany rezultat:** Kupon jest oznaczony jako nieaktywny.

**Wynik:** PASSED

---

### TC_AUTO_031 – Zastosowanie kuponu

**Cel:** Potwierdzenie zastosowania aktywnego kuponu w koszyku.

**Warunki wstępne:** Koszyk ma wartość dodatnią, istnieje aktywny kupon.

**Dane testowe:** koszyk 200.00, kupon 10%

**Przebieg:**
1. Przygotować koszyk o wartości 200.00.
2. Utworzyć aktywny kupon 10%.
3. Zastosować kupon.
4. Odczytać wartość rabatu i total.

**Oczekiwany rezultat:** Wartość koszyka zostaje obniżona zgodnie z rabatem.

**Wynik:** PASSED

---

### TC_AUTO_032 – Niepoprawny kupon

**Cel:** Weryfikacja obsługi kodu nieistniejącego albo nieaktywnego.

**Warunki wstępne:** Koszyk zawiera produkty.

**Dane testowe:** BADCODE

**Przebieg:**
1. Przygotować koszyk.
2. Wprowadzić niepoprawny kod.
3. Wywołać logikę zastosowania kuponu.
4. Odczytać wynik i sumę koszyka.

**Oczekiwany rezultat:** System odrzuca kupon i nie zmienia wartości koszyka.

**Wynik:** PASSED

---

### TC_AUTO_033 – Wyliczenie rabatu

**Cel:** Weryfikacja arytmetyki rabatu procentowego.

**Warunki wstępne:** Istnieje aktywny kupon i koszyk.

**Dane testowe:** kwota 300.00, rabat 15%

**Przebieg:**
1. Przygotować koszyk o wartości 300.00.
2. Zastosować kupon 15%.
3. Odczytać discount_amount.
4. Odczytać total_after_discount.

**Oczekiwany rezultat:** Rabat wynosi 45.00, a kwota po rabacie 255.00.

**Wynik:** PASSED

---

### 4.5. Moduł zamówień

### TC_AUTO_034 – Utworzenie zamówienia

**Cel:** Potwierdzenie, że checkout tworzy zamówienie.

**Warunki wstępne:** Klient jest zalogowany, koszyk nie jest pusty, profil zawiera dane dostawy.

**Dane testowe:** koszyk z dwoma pozycjami

**Przebieg:**
1. Utworzyć użytkownika i profil.
2. Przygotować koszyk.
3. Wywołać checkout.
4. Odczytać utworzone zamówienie.

**Oczekiwany rezultat:** Powstaje zamówienie ze statusem NEW i powiązaniem z użytkownikiem.

**Wynik:** PASSED

---

### TC_AUTO_035 – Generacja numeru ORD

**Cel:** Weryfikacja biznesowego formatu numeru zamówienia.

**Warunki wstępne:** Tworzone jest nowe zamówienie.

**Dane testowe:** nowy Order

**Przebieg:**
1. Utworzyć zamówienie.
2. Odczytać order_number.
3. Sprawdzić prefiks ORD.
4. Sprawdzić unikalność numeru.

**Oczekiwany rezultat:** Numer zamówienia ma format ORD-YYYY-NNNNNN i jest unikalny.

**Wynik:** PASSED

---

### TC_AUTO_036 – Tworzenie OrderItem

**Cel:** Sprawdzenie przeniesienia pozycji koszyka do pozycji zamówienia.

**Warunki wstępne:** Koszyk zawiera co najmniej jedną pozycję.

**Dane testowe:** wariant produktu, ilość, cena

**Przebieg:**
1. Przygotować koszyk.
2. Utworzyć zamówienie.
3. Odczytać pozycje order.items.
4. Porównać ilości i ceny.

**Oczekiwany rezultat:** Dla każdej pozycji koszyka powstaje odpowiedni OrderItem.

**Wynik:** PASSED

---

### TC_AUTO_037 – Snapshot danych dostawy

**Cel:** Weryfikacja zapisania danych dostawy w zamówieniu jako kopii historycznej.

**Warunki wstępne:** Profil użytkownika ma uzupełniony adres.

**Dane testowe:** telefon, ulica, kod pocztowy, miasto

**Przebieg:**
1. Utworzyć profil z adresem.
2. Utworzyć zamówienie.
3. Zmienić dane profilu.
4. Odczytać dane adresowe zamówienia.

**Oczekiwany rezultat:** Dane zapisane w zamówieniu pozostają niezmienne po zmianie profilu.

**Wynik:** PASSED

---

### TC_AUTO_038 – Wyliczenie wartości zamówienia

**Cel:** Sprawdzenie pól finansowych zamówienia.

**Warunki wstępne:** Koszyk zawiera pozycje, opcjonalnie kupon.

**Dane testowe:** subtotal, discount_amount, total_after_discount

**Przebieg:**
1. Przygotować koszyk o znanej wartości.
2. Opcjonalnie zastosować kupon.
3. Utworzyć zamówienie.
4. Porównać wartości finansowe z obliczeniem ręcznym.

**Oczekiwany rezultat:** Wartości zamówienia są zgodne z koszykiem i rabatem.

**Wynik:** PASSED

---

### TC_AUTO_039 – Aktualizacja stock

**Cel:** Weryfikacja zmniejszenia stanu magazynowego po zamówieniu.

**Warunki wstępne:** Wariant ma stock większy niż zamawiana ilość.

**Dane testowe:** stock 10, zamówiona ilość 3

**Przebieg:**
1. Utworzyć wariant ze stockiem 10.
2. Dodać do koszyka 3 sztuki.
3. Utworzyć zamówienie.
4. Odczytać stock wariantu po zakupie.

**Oczekiwany rezultat:** Stan magazynowy zmniejsza się do 7.

**Wynik:** PASSED

---

### TC_AUTO_040 – Pusty koszyk

**Cel:** Potwierdzenie blokady checkout dla pustego koszyka.

**Warunki wstępne:** Koszyk nie zawiera pozycji.

**Dane testowe:** pusta sesja cart

**Przebieg:**
1. Zalogować użytkownika.
2. Ustawić pusty koszyk.
3. Wywołać checkout.
4. Sprawdzić brak zamówienia.

**Oczekiwany rezultat:** Zamówienie nie zostaje utworzone, a użytkownik otrzymuje komunikat.

**Wynik:** PASSED

---

### 4.6. Moduł opinii

### TC_AUTO_041 – Dodanie opinii

**Cel:** Weryfikacja zapisu opinii o produkcie.

**Warunki wstępne:** Istnieje użytkownik i produkt.

**Dane testowe:** rating 4, komentarz testowy

**Przebieg:**
1. Utworzyć użytkownika.
2. Utworzyć produkt.
3. Utworzyć opinię.
4. Odczytać opinię z bazy.

**Oczekiwany rezultat:** Opinia jest zapisana i powiązana z użytkownikiem oraz produktem.

**Wynik:** PASSED

---

### TC_AUTO_042 – Ocena minimalna

**Cel:** Sprawdzenie dolnej granicy skali ocen.

**Warunki wstępne:** Istnieje produkt i użytkownik.

**Dane testowe:** rating 1

**Przebieg:**
1. Utworzyć produkt i użytkownika.
2. Dodać opinię z oceną 1.
3. Zapisać rekord.
4. Odczytać rating.

**Oczekiwany rezultat:** Ocena 1 jest akceptowana.

**Wynik:** PASSED

---

### TC_AUTO_043 – Ocena maksymalna

**Cel:** Sprawdzenie górnej granicy skali ocen.

**Warunki wstępne:** Istnieje produkt i użytkownik.

**Dane testowe:** rating 5

**Przebieg:**
1. Utworzyć produkt i użytkownika.
2. Dodać opinię z oceną 5.
3. Zapisać rekord.
4. Odczytać rating.

**Oczekiwany rezultat:** Ocena 5 jest akceptowana.

**Wynik:** PASSED

---

### TC_AUTO_044 – Aktualizacja średniej ocen

**Cel:** Potwierdzenie zmiany średniej po dodaniu nowej opinii.

**Warunki wstępne:** Produkt ma opinie.

**Dane testowe:** oceny 5, 5, następnie 1

**Przebieg:**
1. Utworzyć produkt.
2. Dodać dwie opinie 5.
3. Sprawdzić średnią.
4. Dodać opinię 1 i sprawdzić średnią ponownie.

**Oczekiwany rezultat:** Średnia ocen zmienia się zgodnie z nowym zestawem danych.

**Wynik:** PASSED

---

### 4.7. Dashboard

### TC_AUTO_045 – Dostęp managera

**Cel:** Sprawdzenie dostępu do dashboardu dla użytkownika uprawnionego.

**Warunki wstępne:** Istnieje użytkownik z rolą MANAGER albo is_staff.

**Dane testowe:** konto managera

**Przebieg:**
1. Zalogować managera.
2. Wysłać GET /dashboard/.
3. Odczytać kod odpowiedzi.
4. Sprawdzić obecność danych dashboardu.

**Oczekiwany rezultat:** Dashboard zwraca HTTP 200.

**Wynik:** PASSED

---

### TC_AUTO_046 – Brak dostępu klienta

**Cel:** Sprawdzenie blokady dashboardu dla zwykłego klienta.

**Warunki wstępne:** Istnieje użytkownik z rolą CUSTOMER.

**Dane testowe:** konto klienta

**Przebieg:**
1. Zalogować klienta.
2. Wysłać GET /dashboard/.
3. Odczytać kod odpowiedzi.
4. Sprawdzić przekierowanie albo komunikat.

**Oczekiwany rezultat:** Klient nie ma dostępu do dashboardu.

**Wynik:** PASSED

---

### TC_AUTO_047 – Wyliczenie liczby produktów

**Cel:** Weryfikacja metryki liczby produktów na dashboardzie.

**Warunki wstępne:** W bazie istnieje ustalona liczba produktów.

**Dane testowe:** 5 produktów

**Przebieg:**
1. Utworzyć 5 produktów.
2. Zalogować managera.
3. Otworzyć dashboard.
4. Sprawdzić wartość products_count.

**Oczekiwany rezultat:** Dashboard pokazuje liczbę 5.

**Wynik:** PASSED

---

### TC_AUTO_048 – Wyliczenie liczby zamówień

**Cel:** Weryfikacja metryki liczby zamówień.

**Warunki wstępne:** W bazie istnieje ustalona liczba zamówień.

**Dane testowe:** 3 zamówienia

**Przebieg:**
1. Utworzyć 3 zamówienia.
2. Zalogować managera.
3. Otworzyć dashboard.
4. Sprawdzić wartość orders_count.

**Oczekiwany rezultat:** Dashboard pokazuje liczbę 3.

**Wynik:** PASSED

---

### TC_AUTO_049 – Wyliczenie przychodu

**Cel:** Weryfikacja sumowania przychodu z zamówień opłaconych lub zrealizowanych.

**Warunki wstępne:** Istnieją zamówienia o statusach wliczanych do przychodu.

**Dane testowe:** PAID 100.00 oraz SHIPPED 200.00

**Przebieg:**
1. Utworzyć zamówienia o znanych kwotach.
2. Otworzyć dashboard.
3. Odczytać revenue.
4. Porównać z sumą ręczną.

**Oczekiwany rezultat:** Przychód wynosi 300.00.

**Wynik:** PASSED

---

### 4.8. REST API

### TC_AUTO_050 – GET products

**Cel:** Weryfikacja publicznego endpointu listy produktów.

**Warunki wstępne:** Istnieje co najmniej jeden produkt.

**Dane testowe:** GET /api/products/

**Przebieg:**
1. Przygotować produkt.
2. Wysłać GET /api/products/.
3. Odczytać status.
4. Sprawdzić strukturę JSON.

**Oczekiwany rezultat:** API zwraca HTTP 200 i listę produktów.

**Wynik:** PASSED

---

### TC_AUTO_051 – GET product detail

**Cel:** Weryfikacja publicznego endpointu szczegółu produktu.

**Warunki wstępne:** Istnieje produkt o znanym ID.

**Dane testowe:** GET /api/products/{id}/

**Przebieg:**
1. Przygotować produkt.
2. Wysłać GET na szczegóły produktu.
3. Odczytać status.
4. Sprawdzić pola produktu.

**Oczekiwany rezultat:** API zwraca HTTP 200 i dane produktu.

**Wynik:** PASSED

---

### TC_AUTO_052 – GET brands

**Cel:** Weryfikacja publicznego endpointu marek.

**Warunki wstępne:** Istnieje co najmniej jedna marka.

**Dane testowe:** GET /api/brands/

**Przebieg:**
1. Utworzyć markę.
2. Wysłać GET /api/brands/.
3. Odczytać status.
4. Sprawdzić nazwę marki w odpowiedzi.

**Oczekiwany rezultat:** API zwraca HTTP 200 i listę marek.

**Wynik:** PASSED

---

### TC_AUTO_053 – GET categories

**Cel:** Weryfikacja publicznego endpointu kategorii.

**Warunki wstępne:** Istnieje co najmniej jedna kategoria.

**Dane testowe:** GET /api/categories/

**Przebieg:**
1. Utworzyć kategorię.
2. Wysłać GET /api/categories/.
3. Odczytać status.
4. Sprawdzić nazwę kategorii w odpowiedzi.

**Oczekiwany rezultat:** API zwraca HTTP 200 i listę kategorii.

**Wynik:** PASSED

---

### TC_AUTO_054 – GET orders bez JWT

**Cel:** Potwierdzenie, że endpoint zamówień jest chroniony.

**Warunki wstępne:** Endpoint /api/orders/ wymaga JWT.

**Dane testowe:** żądanie bez Authorization

**Przebieg:**
1. Wysłać GET /api/orders/ bez tokena.
2. Odczytać status.
3. Sprawdzić brak danych zamówień.
4. Zweryfikować komunikat odmowy.

**Oczekiwany rezultat:** API zwraca HTTP 401.

**Wynik:** PASSED

---

### TC_AUTO_055 – GET orders z JWT

**Cel:** Potwierdzenie dostępu do zamówień z poprawnym tokenem.

**Warunki wstępne:** Istnieje użytkownik i access token.

**Dane testowe:** Authorization: Bearer <access>

**Przebieg:**
1. Pobrać token JWT.
2. Utworzyć zamówienie użytkownika.
3. Wysłać GET /api/orders/ z tokenem.
4. Sprawdzić dane zamówienia.

**Oczekiwany rezultat:** API zwraca HTTP 200 i zamówienia użytkownika.

**Wynik:** PASSED

---

## 5. Testy manualne

### 5.1. Rejestracja

### TC_MAN_001 – Poprawna rejestracja

**Cel:** Sprawdzenie, czy nowy klient może założyć konto.

**Warunki wstępne:** Użytkownik nie jest zalogowany.

**Dane testowe:** unikalny login, email, poprawne hasło

**Przebieg:**
1. Otworzyć formularz rejestracji.
2. Wypełnić wymagane pola.
3. Zatwierdzić formularz.
4. Sprawdzić przekierowanie albo widok profilu.

**Oczekiwany rezultat:** Konto zostaje utworzone, a użytkownik może korzystać z funkcji klienta.

**Wynik:** PASSED

---

### TC_MAN_002 – Pusty login

**Cel:** Weryfikacja walidacji wymaganego loginu.

**Warunki wstępne:** Formularz rejestracji jest dostępny.

**Dane testowe:** login pusty, pozostałe dane poprawne

**Przebieg:**
1. Otworzyć rejestrację.
2. Pozostawić login pusty.
3. Wypełnić pozostałe pola.
4. Zatwierdzić formularz.

**Oczekiwany rezultat:** System blokuje zapis i pokazuje błąd pola login.

**Wynik:** PASSED

---

### TC_MAN_003 – Puste hasło

**Cel:** Weryfikacja walidacji wymaganego hasła.

**Warunki wstępne:** Formularz rejestracji jest dostępny.

**Dane testowe:** puste hasło

**Przebieg:**
1. Otworzyć formularz.
2. Wpisać login.
3. Pozostawić hasło puste.
4. Zatwierdzić formularz.

**Oczekiwany rezultat:** System blokuje rejestrację i pokazuje błąd hasła.

**Wynik:** PASSED

---

### TC_MAN_004 – Duplikat loginu

**Cel:** Sprawdzenie blokady ponownego użycia loginu.

**Warunki wstępne:** Istnieje konto z danym loginem.

**Dane testowe:** login już istniejący

**Przebieg:**
1. Otworzyć formularz rejestracji.
2. Wprowadzić istniejący login.
3. Uzupełnić pozostałe dane.
4. Zatwierdzić formularz.

**Oczekiwany rezultat:** System odrzuca rejestrację i informuje o zajętym loginie.

**Wynik:** PASSED

---

### 5.2. Logowanie

### TC_MAN_005 – Poprawne logowanie

**Cel:** Potwierdzenie logowania istniejącego użytkownika.

**Warunki wstępne:** Istnieje aktywne konto.

**Dane testowe:** poprawny login i hasło

**Przebieg:**
1. Otworzyć logowanie.
2. Wprowadzić poprawne dane.
3. Zatwierdzić formularz.
4. Sprawdzić widok po zalogowaniu.

**Oczekiwany rezultat:** Użytkownik zostaje zalogowany.

**Wynik:** PASSED

---

### TC_MAN_006 – Błędne hasło

**Cel:** Sprawdzenie odmowy logowania dla złego hasła.

**Warunki wstępne:** Istnieje konto użytkownika.

**Dane testowe:** poprawny login, błędne hasło

**Przebieg:**
1. Otworzyć logowanie.
2. Wpisać błędne hasło.
3. Zatwierdzić formularz.
4. Sprawdzić komunikat.

**Oczekiwany rezultat:** Logowanie jest odrzucone.

**Wynik:** PASSED

---

### TC_MAN_007 – Nieistniejący użytkownik

**Cel:** Sprawdzenie odmowy logowania dla nieistniejącego konta.

**Warunki wstępne:** Brak konta o wskazanym loginie.

**Dane testowe:** nieistniejący login

**Przebieg:**
1. Otworzyć logowanie.
2. Wpisać nieistniejący login.
3. Wpisać dowolne hasło.
4. Zatwierdzić formularz.

**Oczekiwany rezultat:** System nie loguje użytkownika i pokazuje błąd.

**Wynik:** PASSED

---

### 5.3. Profil

### TC_MAN_008 – Edycja danych osobowych

**Cel:** Sprawdzenie aktualizacji imienia, nazwiska lub emaila.

**Warunki wstępne:** Użytkownik jest zalogowany.

**Dane testowe:** nowe dane osobowe

**Przebieg:**
1. Otworzyć profil.
2. Przejść do edycji profilu.
3. Zmienić dane.
4. Zapisać formularz.

**Oczekiwany rezultat:** Nowe dane są widoczne w profilu.

**Wynik:** PASSED

---

### TC_MAN_009 – Edycja adresu

**Cel:** Sprawdzenie aktualizacji adresu dostawy.

**Warunki wstępne:** Użytkownik jest zalogowany.

**Dane testowe:** ulica, kod pocztowy, miasto

**Przebieg:**
1. Otworzyć edycję profilu.
2. Uzupełnić dane adresowe.
3. Zapisać formularz.
4. Odświeżyć profil.

**Oczekiwany rezultat:** Adres zostaje zapisany.

**Wynik:** PASSED

---

### TC_MAN_010 – Brak telefonu

**Cel:** Sprawdzenie wymuszenia telefonu przed zamówieniem.

**Warunki wstępne:** Użytkownik jest zalogowany, profil nie ma telefonu.

**Dane testowe:** puste pole telefonu

**Przebieg:**
1. Usunąć telefon z profilu.
2. Dodać produkt do koszyka.
3. Spróbować złożyć zamówienie.
4. Odczytać komunikat.

**Oczekiwany rezultat:** System blokuje checkout do czasu uzupełnienia telefonu.

**Wynik:** PASSED

---

### TC_MAN_011 – Brak adresu

**Cel:** Sprawdzenie wymuszenia adresu przed zamówieniem.

**Warunki wstępne:** Użytkownik jest zalogowany, profil nie ma pełnego adresu.

**Dane testowe:** pusta ulica, kod albo miasto

**Przebieg:**
1. Usunąć dane adresowe.
2. Dodać produkt do koszyka.
3. Spróbować przejść checkout.
4. Odczytać komunikat.

**Oczekiwany rezultat:** System blokuje zamówienie do czasu uzupełnienia adresu.

**Wynik:** PASSED

---

### 5.4. Produkty

### TC_MAN_012 – Lista produktów

**Cel:** Sprawdzenie prezentacji katalogu produktów.

**Warunki wstępne:** W bazie istnieją produkty.

**Dane testowe:** wejście na /products/

**Przebieg:**
1. Otworzyć listę produktów.
2. Sprawdzić widoczność produktów.
3. Zweryfikować nazwy, marki i ceny.
4. Sprawdzić możliwość wejścia w szczegóły.

**Oczekiwany rezultat:** Lista produktów jest czytelna i zawiera dane katalogowe.

**Wynik:** PASSED

---

### TC_MAN_013 – Szczegóły produktu

**Cel:** Sprawdzenie widoku pojedynczego produktu.

**Warunki wstępne:** Produkt ma warianty.

**Dane testowe:** wybrany produkt z listy

**Przebieg:**
1. Otworzyć listę produktów.
2. Kliknąć produkt.
3. Sprawdzić opis, warianty, cenę i opinie.
4. Zweryfikować formularz dodania do koszyka.

**Oczekiwany rezultat:** Widok pokazuje komplet informacji o produkcie.

**Wynik:** PASSED

---

### TC_MAN_014 – Filtrowanie po marce

**Cel:** Weryfikacja filtrowania katalogu według marki.

**Warunki wstępne:** Istnieją produkty różnych marek.

**Dane testowe:** wybrana marka

**Przebieg:**
1. Otworzyć katalog.
2. Wybrać markę w filtrach.
3. Zastosować filtr.
4. Sprawdzić wyniki.

**Oczekiwany rezultat:** Na liście pozostają produkty wybranej marki.

**Wynik:** PASSED

---

### TC_MAN_015 – Filtrowanie po kategorii

**Cel:** Weryfikacja filtrowania po kategorii.

**Warunki wstępne:** Istnieją produkty w kilku kategoriach.

**Dane testowe:** wybrana kategoria

**Przebieg:**
1. Otworzyć katalog.
2. Wybrać kategorię.
3. Zastosować filtr.
4. Sprawdzić wyniki.

**Oczekiwany rezultat:** Lista zawiera produkty z wybranej kategorii.

**Wynik:** PASSED

---

### TC_MAN_016 – Filtrowanie po rozmiarze

**Cel:** Weryfikacja filtrowania po rozmiarze wariantu.

**Warunki wstępne:** Istnieją warianty o różnych rozmiarach.

**Dane testowe:** rozmiar M

**Przebieg:**
1. Otworzyć katalog.
2. Wybrać rozmiar.
3. Zastosować filtr.
4. Sprawdzić wyniki.

**Oczekiwany rezultat:** Lista zawiera produkty mające wariant w wybranym rozmiarze.

**Wynik:** PASSED

---

### TC_MAN_017 – Wyszukiwanie po nazwie

**Cel:** Weryfikacja wyszukiwarki po nazwie produktu.

**Warunki wstępne:** Istnieją produkty o różnych nazwach.

**Dane testowe:** fragment nazwy produktu

**Przebieg:**
1. Otworzyć katalog.
2. Wpisać frazę w wyszukiwarce.
3. Uruchomić wyszukiwanie.
4. Sprawdzić wyniki.

**Oczekiwany rezultat:** Wyniki odpowiadają wpisanej frazie.

**Wynik:** PASSED

---

### 5.5. Koszyk

### TC_MAN_018 – Dodanie produktu

**Cel:** Sprawdzenie dodania wariantu do koszyka.

**Warunki wstępne:** Produkt ma dostępny wariant.

**Dane testowe:** wariant, ilość 1

**Przebieg:**
1. Otworzyć szczegóły produktu.
2. Wybrać wariant i ilość.
3. Kliknąć dodanie do koszyka.
4. Otworzyć koszyk.

**Oczekiwany rezultat:** Produkt znajduje się w koszyku.

**Wynik:** PASSED

---

### TC_MAN_019 – Dodanie wielu produktów

**Cel:** Sprawdzenie koszyka z kilkoma pozycjami.

**Warunki wstępne:** Dostępne są co najmniej dwa produkty.

**Dane testowe:** dwa różne warianty

**Przebieg:**
1. Dodać pierwszy produkt.
2. Wrócić do katalogu.
3. Dodać drugi produkt.
4. Otworzyć koszyk.

**Oczekiwany rezultat:** Koszyk zawiera obie pozycje.

**Wynik:** PASSED

---

### TC_MAN_020 – Usunięcie produktu

**Cel:** Sprawdzenie usunięcia pozycji z koszyka.

**Warunki wstępne:** Koszyk zawiera produkt.

**Dane testowe:** pozycja koszyka

**Przebieg:**
1. Otworzyć koszyk.
2. Wybrać usunięcie pozycji.
3. Zatwierdzić operację.
4. Sprawdzić koszyk.

**Oczekiwany rezultat:** Pozycja nie jest widoczna w koszyku.

**Wynik:** PASSED

---

### TC_MAN_021 – Zmniejszenie ilości

**Cel:** Sprawdzenie częściowego usunięcia sztuk.

**Warunki wstępne:** Koszyk zawiera pozycję w ilości większej niż 1.

**Dane testowe:** ilość 3, usunięcie 1

**Przebieg:**
1. Otworzyć koszyk.
2. Wpisać ilość do usunięcia.
3. Zatwierdzić.
4. Sprawdzić nową ilość i sumę.

**Oczekiwany rezultat:** Ilość i suma koszyka aktualizują się poprawnie.

**Wynik:** PASSED

---

### TC_MAN_022 – Przekroczenie stock

**Cel:** Sprawdzenie blokady ilości większej niż stan magazynowy.

**Warunki wstępne:** Wariant ma ograniczony stock.

**Dane testowe:** ilość większa niż stock

**Przebieg:**
1. Otworzyć produkt.
2. Spróbować dodać zbyt dużą ilość.
3. Zatwierdzić.
4. Sprawdzić komunikat i koszyk.

**Oczekiwany rezultat:** System nie pozwala przekroczyć dostępnego stanu.

**Wynik:** PASSED

---

### 5.6. Kupony

### TC_MAN_023 – Poprawny kupon

**Cel:** Weryfikacja użycia aktywnego kodu rabatowego.

**Warunki wstępne:** Koszyk zawiera produkty, istnieje aktywny kupon.

**Dane testowe:** SALE10

**Przebieg:**
1. Otworzyć koszyk.
2. Wpisać poprawny kupon.
3. Zatwierdzić.
4. Sprawdzić rabat i sumę.

**Oczekiwany rezultat:** Rabat jest naliczony.

**Wynik:** PASSED

---

### TC_MAN_024 – Niepoprawny kupon

**Cel:** Weryfikacja obsługi błędnego kuponu.

**Warunki wstępne:** Koszyk zawiera produkty.

**Dane testowe:** BADCODE

**Przebieg:**
1. Otworzyć koszyk.
2. Wpisać błędny kod.
3. Zatwierdzić.
4. Sprawdzić komunikat.

**Oczekiwany rezultat:** System odrzuca kupon i nie zmienia sumy.

**Wynik:** PASSED

---

### TC_MAN_025 – Usunięcie kuponu

**Cel:** Sprawdzenie cofnięcia rabatu.

**Warunki wstępne:** Do koszyka zastosowano kupon.

**Dane testowe:** koszyk z aktywnym rabatem

**Przebieg:**
1. Otworzyć koszyk.
2. Wybrać usunięcie kuponu.
3. Zatwierdzić.
4. Sprawdzić sumę.

**Oczekiwany rezultat:** Rabat znika, a suma wraca do wartości przed kuponem.

**Wynik:** PASSED

---

### 5.7. Checkout

### TC_MAN_026 – Checkout poprawny

**Cel:** Sprawdzenie utworzenia zamówienia z poprawnymi danymi.

**Warunki wstępne:** Użytkownik jest zalogowany, koszyk zawiera produkty, profil ma adres i telefon.

**Dane testowe:** kompletny profil klienta

**Przebieg:**
1. Otworzyć koszyk.
2. Kliknąć złożenie zamówienia.
3. Potwierdzić checkout.
4. Sprawdzić historię zamówień.

**Oczekiwany rezultat:** Powstaje zamówienie z numerem ORD.

**Wynik:** PASSED

---

### TC_MAN_027 – Checkout bez adresu

**Cel:** Sprawdzenie blokady checkout bez danych adresowych.

**Warunki wstępne:** Koszyk zawiera produkty, profil nie ma adresu.

**Dane testowe:** brak ulicy/kodu/miasta

**Przebieg:**
1. Usunąć adres z profilu.
2. Otworzyć koszyk.
3. Spróbować złożyć zamówienie.
4. Odczytać komunikat.

**Oczekiwany rezultat:** System przekierowuje do edycji profilu albo pokazuje błąd.

**Wynik:** PASSED

---

### TC_MAN_028 – Checkout bez telefonu

**Cel:** Sprawdzenie blokady checkout bez telefonu.

**Warunki wstępne:** Koszyk zawiera produkty, profil nie ma telefonu.

**Dane testowe:** puste pole telefonu

**Przebieg:**
1. Usunąć telefon z profilu.
2. Otworzyć koszyk.
3. Spróbować złożyć zamówienie.
4. Odczytać komunikat.

**Oczekiwany rezultat:** System wymaga uzupełnienia telefonu.

**Wynik:** PASSED

---

### TC_MAN_029 – Checkout z pustym koszykiem

**Cel:** Sprawdzenie braku możliwości utworzenia zamówienia bez pozycji.

**Warunki wstępne:** Koszyk jest pusty.

**Dane testowe:** brak pozycji

**Przebieg:**
1. Otworzyć koszyk.
2. Spróbować przejść checkout.
3. Zatwierdzić operację.
4. Sprawdzić wynik.

**Oczekiwany rezultat:** Zamówienie nie zostaje utworzone.

**Wynik:** PASSED

---

### 5.8. Płatność

### TC_MAN_030 – Poprawny kod BLIK

**Cel:** Sprawdzenie płatności testowej dla zamówienia NEW.

**Warunki wstępne:** Istnieje zamówienie w statusie NEW.

**Dane testowe:** kod 123456

**Przebieg:**
1. Otworzyć szczegóły zamówienia.
2. Wpisać 6-cyfrowy kod BLIK.
3. Zatwierdzić płatność.
4. Sprawdzić status.

**Oczekiwany rezultat:** Status zmienia się na PAID.

**Wynik:** PASSED

---

### TC_MAN_031 – Kod krótszy niż 6 cyfr

**Cel:** Walidacja minimalnej długości kodu BLIK.

**Warunki wstępne:** Istnieje zamówienie NEW.

**Dane testowe:** kod 12345

**Przebieg:**
1. Otworzyć zamówienie.
2. Wpisać zbyt krótki kod.
3. Zatwierdzić.
4. Sprawdzić komunikat.

**Oczekiwany rezultat:** Płatność jest odrzucona.

**Wynik:** PASSED

---

### TC_MAN_032 – Kod dłuższy niż 6 cyfr

**Cel:** Walidacja maksymalnej długości kodu BLIK.

**Warunki wstępne:** Istnieje zamówienie NEW.

**Dane testowe:** kod 1234567

**Przebieg:**
1. Otworzyć zamówienie.
2. Wpisać zbyt długi kod.
3. Zatwierdzić.
4. Sprawdzić komunikat.

**Oczekiwany rezultat:** Płatność jest odrzucona.

**Wynik:** PASSED

---

### TC_MAN_033 – Kod zawierający litery

**Cel:** Walidacja numerycznego formatu kodu BLIK.

**Warunki wstępne:** Istnieje zamówienie NEW.

**Dane testowe:** kod 12A45B

**Przebieg:**
1. Otworzyć zamówienie.
2. Wpisać kod z literami.
3. Zatwierdzić.
4. Sprawdzić komunikat.

**Oczekiwany rezultat:** System wymaga dokładnie 6 cyfr.

**Wynik:** PASSED

---

### 5.9. Zamówienia

### TC_MAN_034 – Historia zamówień

**Cel:** Sprawdzenie listy zamówień klienta.

**Warunki wstępne:** Klient ma co najmniej jedno zamówienie.

**Dane testowe:** konto klienta z zamówieniami

**Przebieg:**
1. Zalogować klienta.
2. Otworzyć zamówienia.
3. Sprawdzić listę.
4. Zweryfikować numer i status.

**Oczekiwany rezultat:** Klient widzi swoje zamówienia.

**Wynik:** PASSED

---

### TC_MAN_035 – Szczegóły zamówienia

**Cel:** Sprawdzenie widoku pojedynczego zamówienia.

**Warunki wstępne:** Istnieje zamówienie klienta.

**Dane testowe:** wybrane zamówienie

**Przebieg:**
1. Otworzyć historię zamówień.
2. Wejść w szczegóły.
3. Sprawdzić produkty, adres i wartości.
4. Zweryfikować status.

**Oczekiwany rezultat:** Widok pokazuje komplet danych zamówienia.

**Wynik:** PASSED

---

### TC_MAN_036 – Historia statusów

**Cel:** Sprawdzenie prezentacji zmian statusu zamówienia.

**Warunki wstępne:** Zamówienie ma wpisy historii statusów.

**Dane testowe:** zamówienie po zmianach statusu

**Przebieg:**
1. Otworzyć szczegóły zamówienia.
2. Przejść do historii statusów.
3. Odczytać wpisy.
4. Sprawdzić kolejność.

**Oczekiwany rezultat:** Historia statusów jest widoczna i uporządkowana.

**Wynik:** PASSED

---

### 5.10. Realizacja zamówień

### TC_MAN_037 – Wysłanie zamówienia

**Cel:** Sprawdzenie oznaczenia zamówienia jako wysłane.

**Warunki wstępne:** Istnieje zamówienie PAID, użytkownik ma uprawnienia staff/admin.

**Dane testowe:** numer przesyłki INPOST123

**Przebieg:**
1. Zalogować pracownika.
2. Otworzyć zamówienie PAID.
3. Wpisać numer przesyłki.
4. Zatwierdzić wysyłkę.

**Oczekiwany rezultat:** Status zmienia się na SHIPPED, a tracking number zostaje zapisany.

**Wynik:** PASSED

---

### TC_MAN_038 – Brak numeru przesyłki

**Cel:** Walidacja wymaganego numeru przesyłki.

**Warunki wstępne:** Istnieje zamówienie PAID.

**Dane testowe:** puste pole tracking_number

**Przebieg:**
1. Otworzyć zamówienie PAID.
2. Pozostawić numer przesyłki pusty.
3. Zatwierdzić formularz.
4. Sprawdzić komunikat.

**Oczekiwany rezultat:** System blokuje wysyłkę bez numeru przesyłki.

**Wynik:** PASSED

---

### TC_MAN_039 – Dostarczenie zamówienia

**Cel:** Sprawdzenie finalizacji zamówienia.

**Warunki wstępne:** Istnieje zamówienie SHIPPED, użytkownik ma uprawnienia.

**Dane testowe:** zamówienie w wysyłce

**Przebieg:**
1. Otworzyć zamówienie SHIPPED.
2. Kliknąć oznaczenie jako dostarczone.
3. Zatwierdzić.
4. Sprawdzić status.

**Oczekiwany rezultat:** Status zmienia się na DELIVERED.

**Wynik:** PASSED

---

### TC_MAN_040 – Próba wysyłki bez uprawnień

**Cel:** Sprawdzenie kontroli dostępu do operacji wysyłki.

**Warunki wstępne:** Zalogowany jest zwykły klient.

**Dane testowe:** konto CUSTOMER

**Przebieg:**
1. Zalogować klienta.
2. Spróbować wejść w akcję wysyłki.
3. Wywołać adres akcji albo sprawdzić brak przycisku.
4. Odczytać reakcję systemu.

**Oczekiwany rezultat:** Klient nie może wysłać zamówienia.

**Wynik:** PASSED

---

### 5.11. Dashboard

### TC_MAN_041 – Dashboard managera

**Cel:** Sprawdzenie dostępu managera do dashboardu.

**Warunki wstępne:** Istnieje konto managera albo admina.

**Dane testowe:** konto MANAGER/ADMIN

**Przebieg:**
1. Zalogować managera.
2. Otworzyć /dashboard/.
3. Sprawdzić metryki.
4. Sprawdzić top produkty i AuditLog.

**Oczekiwany rezultat:** Dashboard jest dostępny i pokazuje dane.

**Wynik:** PASSED

---

### TC_MAN_042 – Brak dostępu klienta

**Cel:** Sprawdzenie blokady dashboardu dla klienta.

**Warunki wstępne:** Istnieje konto CUSTOMER.

**Dane testowe:** konto klienta

**Przebieg:**
1. Zalogować klienta.
2. Wejść na /dashboard/.
3. Odczytać komunikat albo przekierowanie.
4. Sprawdzić brak danych dashboardu.

**Oczekiwany rezultat:** Klient nie ma dostępu do dashboardu.

**Wynik:** PASSED

---

### 5.12. AuditLog

### TC_MAN_043 – Rejestracja zdarzenia

**Cel:** Sprawdzenie zapisu operacji biznesowej w AuditLog.

**Warunki wstępne:** AuditLog jest aktywny.

**Dane testowe:** dowolna operacja audytowana

**Przebieg:**
1. Wykonać operację biznesową.
2. Otworzyć panel AuditLog.
3. Wyszukać wpis.
4. Sprawdzić aktora, akcję i opis.

**Oczekiwany rezultat:** W AuditLog pojawia się wpis zdarzenia.

**Wynik:** PASSED

---

### TC_MAN_044 – Zmiana statusu

**Cel:** Sprawdzenie audytu zmiany statusu zamówienia.

**Warunki wstępne:** Istnieje zamówienie do zmiany statusu.

**Dane testowe:** PAID -> SHIPPED albo SHIPPED -> DELIVERED

**Przebieg:**
1. Zmienić status jako użytkownik uprawniony.
2. Otworzyć AuditLog.
3. Wyszukać wpis zmiany statusu.
4. Sprawdzić opis zdarzenia.

**Oczekiwany rezultat:** AuditLog zawiera informację o zmianie statusu.

**Wynik:** PASSED

---

### TC_MAN_045 – Rejestracja płatności

**Cel:** Sprawdzenie audytu opłacenia zamówienia.

**Warunki wstępne:** Istnieje zamówienie NEW.

**Dane testowe:** poprawny kod BLIK

**Przebieg:**
1. Opłacić zamówienie.
2. Otworzyć AuditLog.
3. Wyszukać wpis płatności.
4. Sprawdzić numer zamówienia w opisie.

**Oczekiwany rezultat:** AuditLog zawiera wpis związany z płatnością.

**Wynik:** PASSED

---

## 6. Dane testowe

Do testów wykorzystano dane demonstracyjne przygotowane dla projektu:

- 50 produktów,
- 147 wariantów produktów,
- 20 użytkowników testowych,
- 40 zamówień,
- 201 opinii,
- 4 kupony rabatowe,
- 100 wpisów AuditLog.

Dane demonstracyjne umożliwiają sprawdzenie działania aplikacji na zbiorze większym niż pojedyncze rekordy testowe.

## 7. Podsumowanie

| Obszar | Liczba scenariuszy |
|---|---:|
| Testy automatyczne | 55 |
| Testy manualne | 45 |
| Łącznie | 100 |

**Wynik końcowy:** PASSED

Nie stwierdzono błędów krytycznych uniemożliwiających działanie systemu. Scenariusze obejmują kluczowe procesy biznesowe i techniczne systemu Clothing Store, w tym katalog produktów, koszyk, checkout, zamówienia, płatność testową BLIK, REST API, JWT, dashboard oraz AuditLog.
