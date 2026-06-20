from django.contrib import messages


APP_MESSAGES = {
    "KS_01": ("success", "Dodano produkt do koszyka."),
    "KS_02": ("success", "Zamówienie zostało złożone."),
    "KS_03": ("success", "Profil został zaktualizowany."),
    "KS_04": ("success", "Konto zostało utworzone."),
    "KS_05": ("success", "Wylogowano."),
    "KS_06": ("success", "Zamówienie zostało opłacone."),
    "KS_07": ("success", "Zamówienie zostało wysłane."),
    "KS_08": ("success", "Zamówienie zostało dostarczone."),
    "KS_09": ("success", "Kupon został zastosowany."),
    "KS_10": ("success", "Kupon został usunięty."),
    "KS_11": ("success", "Opinia została dodana."),

    "KB_01": ("error", "Ilość musi być większa od zera."),
    "KB_02": ("error", "Nie można dodać produktu. Przekroczono dostępny stan magazynowy."),
    "KB_03": ("error", "Koszyk jest pusty."),
    "KB_04": ("error", "Jeden z produktów w koszyku nie istnieje."),
    "KB_05": ("error", "Nie można złożyć zamówienia. Brak wystarczającej liczby sztuk."),
    "KB_06": ("error", "Brak uprawnień."),
    "KB_07": ("error", "Brak wymaganych danych dostawy."),
    "KB_08": ("error", "Brak numeru przesyłki."),
    "KB_09": ("error", "Nieprawidłowy kod BLIK."),
    "KB_10": ("error", "Kupon nie istnieje albo jest nieaktywny."),
    "KB_11": ("error", "Nie można dodać drugiej opinii do tego produktu."),

    "KI_01": ("info", "Wyniki zostały przefiltrowane."),
    "KI_02": ("info", "Koszyk został zaktualizowany."),

    "KO_01": ("warning", "Opłacić można tylko nowe zamówienie."),
    "KO_02": ("warning", "Wysłać można tylko opłacone zamówienie."),
    "KO_03": ("warning", "Nie można dostarczyć zamówienia w aktualnym statusie."),
}


LEVEL_MAP = {
    "success": messages.SUCCESS,
    "error": messages.ERROR,
    "info": messages.INFO,
    "warning": messages.WARNING,
}


def add_app_message(request, code, details=""):
    level_name, text = APP_MESSAGES[code]
    full_text = f"{code}: {text}"

    if details:
        full_text = f"{full_text} {details}"

    messages.add_message(
        request,
        LEVEL_MAP[level_name],
        full_text,
        extra_tags=level_name,
    )
