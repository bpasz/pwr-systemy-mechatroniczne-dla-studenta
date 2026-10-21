# L1. Winda na STM32 w symulatorze Wokwi

> **Systemy mechatroniczne · Laboratorium 1 (3 h akad.)**
> Wykłady powiązane: W01, W02, W03.
> Sylabus: La1 (termin wprowadzający), La2 (moduły analogowo-cyfrowe), La3 (logika kontrolno-sterująca).

## Cel

Po zajęciach potrafisz:

- uruchomić program na mikrokontrolerze STM32 (Nucleo-C031C6) w symulatorze Wokwi,
- sterować pinami GPIO na trzech poziomach abstrakcji (rejestry, HAL, Arduino),
- obsłużyć przycisk z drganiami styków i przerwanie zewnętrzne (EXTI),
- generować impulsy dla sterownika silnika krokowego z przerwania timera i odczytywać ADC,
- zaprojektować i zaimplementować **automat skończony** sterujący windą.
- dodać sygnalizację dźwiękową, która nie blokuje programu sterującego.

## Zasady zajęć

- **Pracujesz indywidualnie.** Zajęcia zaczynają się od zadania wprowadzającego (część prowadzona), potem każdy realizuje własny projekt.
- **Sprawozdanie piszesz w trakcie zajęć** i dokumentujesz w nim postępy pracy na bieżąco. Prowadzący ocenia je na zajęciach, nie ma terminu oddania po zajęciach.
- Na początku zajęć prowadzący **może** przeprowadzić krótką kartkówkę (ok. 10 min) z wykładów W01–W03.
- Aby zaliczyć laboratorium, trzeba zaliczyć **wszystkie sekcje** z tabeli kryteriów oceny.

## Przed zajęciami

Przejrzyj slajdy W03, szczególnie: warstwy programowania, timery, przerwania, automat stanów. Konta w Wokwi i na GitHubie zakładamy na początku zajęć.

## Plan zajęć (135 min)

| Czas | Część |
|---|---|
| 0:00–0:10 | Organizacja: konta Wokwi i GitHub, repozytorium sprawozdania, zasady zajęć |
| 0:10–0:55 | Część 1: zadanie wprowadzające, ćwiczenia prowadzone 1–3 |
| 0:55–1:50 | Część 2: projekt indywidualny „Winda” |
| 1:50–2:05 | Część 3: dzwonek (sygnalizacja dźwiękowa) |
| 2:05–2:15 | Przedstawienie sprawozdania i ocena u prowadzącego |

## Jak otworzyć projekt w Wokwi

1. Otwórz nowy projekt STM32: <https://wokwi.com/projects/new/st-nucleo-c031c6>.
2. W zakładce **sketch.ino** zastąp całą treść zawartością pliku `sketch.ino` z odpowiedniego katalogu tego repozytorium.
3. W zakładce **diagram.json** zastąp treść zawartością pliku `diagram.json`.
4. Kliknij zielony przycisk ▶ (Start). Pierwsza kompilacja trwa kilkanaście sekund.
5. Zapisz projekt (**Save**, wymaga konta) i wklej link do sprawozdania.

> Wokwi kompiluje kod rdzeniem **STM32duino** (API Arduino dla STM32, rozwijane przez STMicroelectronics). Możesz w nim używać także funkcji HAL, LL i rejestrów CMSIS (W03).

## Część 1: zadanie wprowadzające (ćwiczenia prowadzone)

### Ćwiczenie 1: dioda na trzech poziomach (10 min)

Katalog: [`cwiczenia/1-blink`](cwiczenia/1-blink/)

1. Uruchom program z `#define WARIANT 1` (rejestry). Sprawdź w monitorze portu szeregowego częstotliwość zegara rdzenia.
2. Zmień na `WARIANT 2` (HAL) i `WARIANT 3` (Arduino). Efekt jest ten sam.
3. **Pytanie do sprawozdania:** co robią linie `RCC->IOPENR |= ...` i `GPIOA->MODER = ...`? Dlaczego zapis do `BSRR` jest bezpieczniejszy niż do `ODR`, gdy ten sam port obsługuje też przerwanie? (RM0490, rozdział GPIO).

### Ćwiczenie 2: przycisk, drgania styków, przerwanie (15 min)

Katalog: [`cwiczenia/2-przycisk`](cwiczenia/2-przycisk/)

1. Wciśnij przycisk 10 razy (myszą albo spacją, gdy symulacja ma fokus). Porównaj liczbę wciśnięć z tłumieniem drgań i liczbę zboczy zliczonych w przerwaniu.
2. W `diagram.json` dopisz do przycisku atrybut `"bounce": "0"` i powtórz. Co się zmieniło?
3. Zmień `CZAS_DEBOUNCE_MS` na 1 ms i na 200 ms. Opisz skutki.
4. **Pytanie:** dlaczego `zboczaSurowe` jest `volatile` i czytane między `noInterrupts()` a `interrupts()`?

### Ćwiczenie 3: silnik krokowy, timer i ADC (20 min)

Katalog: [`cwiczenia/3-silnik-krokowy`](cwiczenia/3-silnik-krokowy/)

1. Uruchom program. Kręć potencjometrem: prędkość silnika zmienia się w zakresie 50–800 kroków/s.
2. Przełącznik zmienia kierunek. Obserwuj licznik kroków na silniku i w monitorze.
3. Policz: timer TIM14 taktowany 48 MHz ma przepełniać się 1600 razy/s. Jakie PSC i ARR ustawi biblioteka? (wzór z W03).
4. Zmień odwzorowanie ADC → prędkość tak, aby w środkowym położeniu potencjometru silnik stał, a skrajne położenia dawały ±400 kroków/s z odpowiednim kierunkiem (przełącznik przestaje być potrzebny).

## Część 2: projekt indywidualny „Winda”

Punkt startu: katalog [`szkielet`](szkielet/).

### Opis układu

| Element | Pin | Uwagi |
|---|---|---|
| przyciski wezwań: piętro 0, 1, 2 | D2, D3, D4 | do GND, `INPUT_PULLUP`; w symulacji także klawisze `0`, `1`, `2` |
| sterownik A4988: STEP, DIR, EN | D5, D6, D7 | EN aktywne stanem niskim |
| silnik krokowy (kabina) | przez A4988 | 200 kroków/obr., **400 kroków = 1 piętro** |
| przełącznik STOP | D8 | przesunięty w lewo = zatrzymanie awaryjne |
| serwo drzwi | D9 (PC7, TIM3_CH2) | 1 ms = zamknięte, 2 ms = otwarte |
| diody „kabina na piętrze” | D10, D11, D12 | |
| dioda LD4 na płytce | D13 (PA5) | miga w czasie jazdy (2 Hz) i awarii (8 Hz) |
| dzwonek (brzęczyk piezo) | A1 (PA1) | część 3 |

### Wymagania

1. **W1.** Wciśnięcie przycisku piętra rejestruje wezwanie (z tłumieniem drgań styków).
2. **W2.** Winda w spoczynku jedzie do piętra z wezwaniem, z prędkością 400 kroków/s generowaną w przerwaniu timera TIM14.
3. **W3.** Po dojeździe drzwi otwierają się na 3 s, potem zamykają. Ponowne wezwanie z tego piętra przedłuża otwarcie.
4. **W4.** Przełącznik STOP w **dowolnym** stanie natychmiast zatrzymuje silnik (stan AWARIA). Po zwolnieniu STOP kabina dojeżdża do najbliższego piętra poniżej i otwiera drzwi.
5. **W5.** Wezwania zgłoszone w czasie jazdy nie giną.
6. **W6.** Program nie używa `delay()` (poza ćwiczeniem 1).
7. **W7 (rozszerzenie).** Algorytm zbiorczy: winda zatrzymuje się po drodze na piętrach z wezwaniem i nie zmienia kierunku, dopóki są wezwania w bieżącym kierunku.

### Zadania

1. Narysuj **diagram automatu stanów** (stany: POSTOJ, JAZDA, DRZWI_OTWARTE, AWARIA; przejścia z warunkami i akcjami). Porównaj z diagramem z wykładu W03.
2. Otwórz szkielet w Wokwi i uzupełnij kolejno `TODO(1)` … `TODO(3b)`. Po każdym kroku uruchom symulację i obserwuj monitor portu szeregowego (logi przejść między stanami). Zapisz w sprawozdaniu, co sprawdziłeś i z jakim wynikiem.
3. Zaimplementuj `TODO(5)` (zatrzymanie po drodze), a jeśli zostanie czas, `TODO(4)` (algorytm zbiorczy, wymaganie W7).
4. Sprawdź działanie w symulacji na scenariuszach: jazda na piętro 2; wezwanie na 0, a w trakcie jazdy na 1 (zatrzymanie po drodze); STOP między piętrami i powrót. Dla W7: kabina na 0, wezwanie na 2, a w trakcie jazdy na 0 i 1.

## Część 3: dzwonek

Winda sygnalizuje zdarzenia dźwiękiem. W `diagram.json` jest już brzęczyk piezo (`wokwi-buzzer`) podłączony do pinu A1.

### Wymagania

8. **W8.** Po przyjeździe na piętro (wejście do stanu DRZWI_OTWARTE) rozlega się gong: ton przez 300 ms (`CZAS_GONGU_MS`).
9. **W9.** W stanie AWARIA dzwonek daje sygnał przerywany: 250 ms dźwięku, 250 ms ciszy (`OKRES_ALARMU_MS`), aż do zwolnienia STOP.
10. **W10.** Dzwonek nie może zablokować programu: bez `delay()` i bez dodatkowego timera.

### Zadania

1. Przeczytaj początek funkcji `przerwanieKrokow()`. Ton generuje już przerwanie TIM14: gdy `dzwonekWlaczony` jest równe `true`, stan pinu A1 zmienia się w każdym przerwaniu. **Pytanie do sprawozdania:** jaką częstotliwość ma ten ton i dlaczego jest równa połowie częstotliwości przerwań?
2. Uzupełnij `TODO(6a)` w `otworzDrzwi()` (start gongu) i `TODO(6b)` w `obsluzDzwonek()` (czas trwania gongu i alarm przerywany).
3. Sprawdź w symulacji oba sygnały (włącz dźwięk w przeglądarce). Opisz w sprawozdaniu, jak dźwięk zmieniłby się, gdyby częstotliwość TIM14 zmieniała się w czasie jazdy (rampa przyspieszenia z rozszerzeń poniżej) i jak temu zaradzić.

### Rozszerzenia dla chętnych

- **Rampa przyspieszenia** (W10): zmieniaj częstotliwość TIM14 tak, aby kabina łagodnie ruszała i hamowała (profil trapezowy).
- **Bazowanie:** dodaj krańcówkę dolną (przycisk) i procedurę bazowania po resecie zamiast założenia, że kabina startuje na piętrze 0.
- **Wyświetlacz:** pokaż numer piętra na wyświetlaczu 7-segmentowym (`wokwi-7segment`) albo TM1637 (biblioteka w `libraries.txt`).
- **Sterowanie z komputera (W09):** przyjmuj wezwania z portu szeregowego (znaki `0`, `1`, `2`).
- **Melodia dzwonka:** zamiast jednego tonu zagraj na przemian dwa tony (400 Hz i 200 Hz) generowane z tego samego przerwania: dla niższego tonu zmieniaj stan pinu co drugie przerwanie.

## Sprawozdanie (na zajęciach)

Sprawozdanie piszesz na bieżąco w trakcie zajęć, w pliku `L1/README.md` w swoim repozytorium (albo w formie wskazanej przez prowadzącego). Po każdej części dopisz, co zrobiłeś i z jakim wynikiem. Przed końcem zajęć przedstawiasz prowadzącemu sprawozdanie i działającą symulację; prowadzący ocenia je na miejscu.

Sprawozdanie zawiera:

- link do projektu Wokwi z Twoją windą (albo `sketch.ino` i `diagram.json`),
- diagram automatu stanów (zdjęcie rysunku lub rysunek, np. z <https://app.diagrams.net>),
- odpowiedzi na pytania z ćwiczeń 1–3 i obliczenie PSC/ARR z ćwiczenia 3,
- opis sprawdzonych scenariuszy windy (co działa, czego nie udało się zrobić),
- odpowiedzi z części 3 (dzwonek).

### Kryteria oceny

| Sekcja | Punkty |
|---|---|
| Część 1: ćwiczenia 1–3, odpowiedzi i obliczenia | 25 |
| Diagram automatu stanów | 15 |
| Winda: wymagania W1–W6 (symulacja) | 35 |
| Część 3: dzwonek, wymagania W8–W10 | 15 |
| Jakość kodu i sprawozdania | 10 |
| **Razem** | **100** |

**Warunek zaliczenia:** trzeba zaliczyć wszystkie sekcje z tabeli. Rozszerzenia (W7 i zadania dla chętnych) dają do 10 punktów dodatkowych, ale nie zastępują żadnej sekcji. Jeśli odbyła się kartkówka, prowadzący podaje na początku zajęć, jak uwzględnia ją w ocenie.

## Źródła

- Wokwi Docs: [board-st-nucleo-c031c6](https://docs.wokwi.com/parts/board-st-nucleo-c031c6), [wokwi-a4988](https://docs.wokwi.com/parts/wokwi-a4988), [wokwi-stepper-motor](https://docs.wokwi.com/parts/wokwi-stepper-motor), [wokwi-servo](https://docs.wokwi.com/parts/wokwi-servo), [wokwi-pushbutton](https://docs.wokwi.com/parts/wokwi-pushbutton).
- STM32duino: [HardwareTimer library](https://github.com/stm32duino/Arduino_Core_STM32/wiki/HardwareTimer-library), wariant `NUCLEO_C031C6` w [Arduino_Core_STM32](https://github.com/stm32duino/Arduino_Core_STM32).
- STMicroelectronics, *RM0490: STM32C0x1 reference manual* (GPIO, TIM, EXTI).
- Wokwi Docs: [wokwi-buzzer](https://docs.wokwi.com/parts/wokwi-buzzer).


------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Sprawozdanie - Laboratorium 1
## Część 1
### Ćwiczenie 1 - Dioda na trzech poziomach
1. Co robią linie RCC->IOPENR |= ... i GPIOA->MODER = ...?
RCC->IOPENR |= ... włącza sygnał zegarowy (taktowanie) dla portu GPIOA. Bez tego układ peryferyjny portu jest wyłączony i nie przyjmuje poleceń.

GPIOA->MODER = ... konfiguruje pin PA5 jako wyjście cyfrowe (najpierw maskuje/zeruje jego stare bity konfiguracyjne, a potem wpisuje wartość 01 oznaczającą tryb wyjścia).

2. Dlaczego zapis do BSRR jest bezpieczniejszy niż do ODR, gdy ten sam port obsługuje też przerwanie?
Zapis do rejestru BSRR jest bezpieczniejszy, bo to operacja wykonująca się w jednym takcie zegara, zapobiega to zepsuciu stanu innych pinów, jeśli podczas modyfikacji ODR wtrąciłoby się przerwanie.

### Ćwiczenie 2 - przycisk, drgania styków, przerwanie
1. Liczba zboczy zliczonych w przerwaniu (np. blisko 500) jest znacznie większa niż rzeczywista liczba wciśnięć (10), ponieważ styki mechaniczne przycisku drgają. Szybkie przerwanie sprzętowe rejestruje każde takie drgnięcie jako osobne zbocze.
2. Dodanie "bounce": "0" spowodowało zrównanie się liczby przerwań z liczbą wciśnięć. Atrybut ten eliminuje drgania.
3. Przy wartości 1 ms przycisk wyłapuję krótkie kliknięcia, natomiast przy wartości 200 ms, aby kliknięcie zostało wykryte trzeba przytrzymać przycisk.
4. Zmienna zboczaSurowe jest volatile, bo zmienia ją przerwanie, a nie zwykły kod w loop(). Kompilator o tym nie wie, więc bez volatile mógłby zapamiętać starą wartość i jej nie odświeżać.
Odczyt jest między noInterrupts() a interrupts(), żeby przerwanie nie wpadło w trakcie czytania zmiennej i nie zmieniło jej w połowie. Dzięki temu dostajemy poprawną, spójną wartość.

### Ćwiczenie 3 - silnik krokowy, timer i ADC
Policz: timer TIM14 taktowany 48 MHz ma przepełniać się 1600 razy/s. Jakie PSC i ARR ustawi biblioteka? (wzór z W03).
f_update = f_TIM / (PSC+1)(ARR+1)
1600 = 48000000/(PSC+1)(ARR+1)
(PSC+1)(ARR+1)=30000
PSC = 47+1
ARR+1 = 30000/49 = 625
ARR = 624

