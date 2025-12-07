# Instrukcja Integracji Frontendu z Systemem Wieloagentowym SWZ

## Przegląd
System backendowy udostępnia inteligentnego asystenta, który prowadzi użytkownika przez proces tworzenia SWZ. Komunikacja odbywa się za pomocą jednego endpointu `/chat`.

Kluczową cechą systemu jest **Template Engine**:
1.  Backend generuje szablony Markdown z placeholderami (np. `{{ nip }}`).
2.  Backend przechowuje dane w strukturze `SWZData`.
3.  Backend renderuje finalny dokument przed wysłaniem do frontendu.
4.  Frontend otrzymuje wyrenderowany tekst ORAZ surowe dane, co pozwala na budowę formularzy edycyjnych.

## Endpoint API

### `POST /chat`

#### Żądanie (Request)
```json
{
  "message": "Treść wiadomości od użytkownika"
}
```

#### Odpowiedź (Response)
```json
{
  "response": "Treść odpowiedzi od agenta (Markdown)",
  "to_render": true,
  "active_section": "basic_data",
  "swz_data": {
    "organization_name": "Urząd Gminy",
    "nip": "123-456-78-90",
    ...
  }
}
```

## Logika Frontendu

### 1. Obsługa Czatu
- Wyświetlaj `response` w oknie czatu.
- Obsługuj Markdown (nagłówki, listy, pogrubienia).

### 2. Flaga `to_render`
- Jeśli `to_render` jest `true`:
  - Oznacza to, że sekcja została zakończona i wygenerowana.
  - Weź treść z pola `response` i wyświetl ją w panelu **Podglądu Dokumentu**.
  - Zaktualizuj widok, aby użytkownik widział postęp.

### 3. Obsługa Danych (`swz_data`) i Formularzy
- W odpowiedzi otrzymujesz obiekt `swz_data` zawierający wszystkie zebrane dotychczas dane.
- **Wykorzystanie**: Możesz użyć tych danych do automatycznego uzupełnienia formularza edycji po stronie frontendu.
- **Przykład**:
  - Jeśli `active_section` to `basic_data`, wyświetl formularz z polami "Nazwa", "NIP", "Adres".
  - Wypełnij te pola wartościami z `swz_data.organization_name`, `swz_data.nip` itd.

### 4. Edycja Danych
- Obecnie system działa w trybie konwersacyjnym. Aby zmienić dane, użytkownik może napisać do czatu: "Zmień NIP na 111-222-33-44".
- **Planowana funkcja**: W przyszłości dodamy endpoint `/update_data`, który pozwoli na bezpośrednie przesłanie zaktualizowanego JSON-a z formularza, co automatycznie przeliczy szablon bez konieczności rozmowy z AI.

## Przykład Przepływu (Flow)

1.  **Użytkownik**: "Chcę przygotować SWZ dla Urzędu Gminy X, NIP 123..."
2.  **Backend**: Przetwarza dane, ekstrahuje NIP i Nazwę.
3.  **Backend Response**:
    ```json
    {
      "response": "# I. ZAMAWIAJĄCY\n\n**Nazwa:** Urząd Gminy X...",
      "to_render": true,
      "active_section": "basic_data",
      "swz_data": { "organization_name": "Urząd Gminy X", "nip": "123..." }
    }
    ```
4.  **Frontend**:
    - Wyświetla wiadomość w czacie.
    - Wykrywa `to_render: true` -> Aktualizuje podgląd dokumentu po prawej stronie.
    - (Opcjonalnie) Aktualizuje formularz w panelu bocznym danymi z `swz_data`.
