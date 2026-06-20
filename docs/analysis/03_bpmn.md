# BPMN / Procesy biznesowe — Clothing Store

## BP-01 Rejestracja użytkownika

```mermaid
flowchart TD
    A([Start]) --> B[Użytkownik otwiera rejestrację]
    B --> C[Wypełnia formularz]
    C --> D{Dane poprawne?}
    D -- Nie --> E[Komunikaty błędów formularza]
    E --> C
    D -- Tak --> F[Utworzenie User]
    F --> G[Utworzenie UserProfile]
    G --> H[Automatyczne logowanie]
    H --> I[Przejście do profilu]
    I --> J([Koniec])
```

## BP-02 Zakup produktu

```mermaid
flowchart TD
    A([Start]) --> B[Przegląd produktów]
    B --> C[Wybór wariantu]
    C --> D[Podanie ilości]
    D --> E{Ilość poprawna?}
    E -- Nie --> F[KB_01]
    E -- Tak --> G{Dostępny stock?}
    G -- Nie --> H[KB_02]
    G -- Tak --> I[Dodanie do koszyka]
    I --> J[KS_01]
    J --> K([Koniec])
```

## BP-03 Checkout

```mermaid
flowchart TD
    A([Start]) --> B[Klient klika Złóż zamówienie]
    B --> C{Użytkownik zalogowany?}
    C -- Nie --> D[Przekierowanie do logowania]
    C -- Tak --> E{Koszyk pusty?}
    E -- Tak --> F[KB_03]
    E -- Nie --> G{Dane dostawy kompletne?}
    G -- Nie --> H[KB_07 i przejście do edycji profilu]
    G -- Tak --> I[Utworzenie Order]
    I --> J[Utworzenie OrderItem]
    J --> K[Aktualizacja stock]
    K --> L[Wyczyszczenie koszyka]
    L --> M[KS_02]
    M --> N([Koniec])
```

## BP-04 Płatność Fake BLIK

```mermaid
flowchart TD
    A([Start]) --> B[Klient otwiera zamówienie NEW]
    B --> C[Wpisuje kod BLIK]
    C --> D{Kod ma 6 cyfr?}
    D -- Nie --> E[KB_09]
    D -- Tak --> F[Zmiana statusu na PAID]
    F --> G[Zapis OrderStatusHistory]
    G --> H[Zapis AuditLog]
    H --> I[KS_06]
    I --> J([Koniec])
```

## BP-05 Wysyłka zamówienia

```mermaid
flowchart TD
    A([Start]) --> B[Pracownik otwiera zamówienie]
    B --> C{Ma uprawnienia?}
    C -- Nie --> D[KB_06]
    C -- Tak --> E{Status PAID?}
    E -- Nie --> F[KO_02]
    E -- Tak --> G[Wpisanie numeru przesyłki]
    G --> H{Numer podany?}
    H -- Nie --> I[KB_08]
    H -- Tak --> J[Status SHIPPED]
    J --> K[OrderStatusHistory]
    K --> L[AuditLog]
    L --> M[KS_07]
    M --> N([Koniec])
```

## BP-06 Dostarczenie zamówienia

```mermaid
flowchart TD
    A([Start]) --> B[Pracownik otwiera zamówienie]
    B --> C{Ma uprawnienia?}
    C -- Nie --> D[KB_06]
    C -- Tak --> E{Status SHIPPED?}
    E -- Nie --> F[KO_03]
    E -- Tak --> G[Status DELIVERED]
    G --> H[OrderStatusHistory]
    H --> I[AuditLog]
    I --> J[KS_08]
    J --> K([Koniec])
```

## BP-07 Obsługa kuponu

```mermaid
flowchart TD
    A([Start]) --> B[Użytkownik wpisuje kod kuponu]
    B --> C{Kupon istnieje i aktywny?}
    C -- Nie --> D[KB_10]
    C -- Tak --> E[Zapis kodu w sesji]
    E --> F[Przeliczenie koszyka]
    F --> G[KS_09]
    G --> H([Koniec])
```

## BP-08 Dodanie opinii

```mermaid
flowchart TD
    A([Start]) --> B[Klient otwiera produkt]
    B --> C[Wpisuje ocenę i komentarz]
    C --> D{Czy opinia już istnieje?}
    D -- Tak --> E[KB_11]
    D -- Nie --> F[Zapis Review]
    F --> G[Aktualizacja średniej oceny]
    G --> H[KS_11]
    H --> I([Koniec])
```
