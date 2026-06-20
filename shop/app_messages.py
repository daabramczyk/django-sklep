from django.contrib import messages


APP_MESSAGES = {
    "KS_01": ("success", "Dodano produkt do koszyka."),
    "KS_02": ("success", "Zamówienie zostało złożone."),
    "KS_03": ("success", "Profil został zaktualizowany."),
    "KS_04": ("success", "Konto zostało utworzone."),
    "KS_05": ("success", "Wylogowano."),
    "KS_07": ("success", "Zamówienie zostało wysłane."),
    "KB_06": ("error", "Brak uprawnień."),
    "KB_01": ("error", "Ilość musi być większa od zera."),
    "KB_02": ("error", "Nie można dodać produktu. Przekroczono dostępny stan magazynowy."),
    "KB_03": ("error", "Koszyk jest pusty."),
    "KB_04": ("error", "Jeden z produktów w koszyku nie istnieje."),
    "KB_05": ("error", "Nie można złożyć zamówienia. Brak wystarczającej liczby sztuk."),
    "KS_06": ("success", "Zamówienie zostało opłacone."),

    "KI_01": ("info", "Wyniki zostały przefiltrowane."),
    "KI_02": ("info", "Koszyk został zaktualizowany."),

    "KO_01": ("warning", "Wybrana ilość została ograniczona."),
    "KO_02": ("warning", "Produkt ma niski stan magazynowy."),
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
