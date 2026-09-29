---
title: "W07. Inżynieria oprogramowania w systemach mechatronicznych"
subtitle: "Architektura, kontrola wersji, testy, ciągła integracja, powtarzalne środowiska"
author: "Systemy mechatroniczne · PWr W12N"
---

## Plan wykładu

1. Specyfika oprogramowania mechatronicznego
2. Architektura warstwowa i modułowa
3. Kontrola wersji: git i przegląd kodu
4. Testowanie: od testu jednostkowego do HIL
5. Ciągła integracja (CI)
6. Powtarzalne środowiska: kontenery i środowiska w chmurze
7. Normy i bezpieczeństwo funkcjonalne


# Specyfika


## Czym różni się oprogramowanie mechatroniczne

- **Działa w pętli z fizyką**: błąd to nie tylko zły wynik, ale ruch maszyny, uszkodzenie, zagrożenie dla człowieka.
- **Czas rzeczywisty**: liczy się nie tylko *co*, ale *kiedy*. Spóźniony wynik sterownika bywa gorszy niż brak wyniku.
- **Ograniczone zasoby**: STM32C031 ma 32 KB Flash i 12 KB RAM. Program windy z L1 zajmuje ok. 70% pamięci programu.
- **Różne platformy** w jednym systemie: mikrokontroler (C/C++), komputer z ROS 2 (Python/C++), chmura (uczenie maszynowe).
- **Trudne testowanie**: sprzęt jest drogi, jeden, zajęty. Stąd symulacja: Wokwi, UAIbot, Gazebo.


## Czas rzeczywisty

| Pojęcie | Znaczenie | Przykład |
|---|---|---|
| **twardy** czas rzeczywisty | przekroczenie terminu = awaria | pętla prądowa napędu (kHz), poduszka powietrzna |
| **miękki** czas rzeczywisty | przekroczenie pogarsza jakość | wideo, interfejs użytkownika |
| **jitter** | zmienność opóźnienia | ±50 µs w pętli 1 kHz |
| **RTOS** | system operacyjny z deterministycznym szeregowaniem | FreeRTOS, Zephyr |

- Na mikrokontrolerze: przerwania timera (L1) albo RTOS.
- W ROS 2: jądro Linux z łatką PREEMPT_RT, `ros2_control` z pętlą o stałym okresie (W11).


# Architektura


## Warstwy oprogramowania sterownika

| Warstwa | Odpowiedzialność | Przykład z kursu |
|---|---|---|
| Aplikacja / zadanie | co robot ma zrobić | kolejka wezwań windy, sekwencja pick & place |
| Sterowanie | jak to osiągnąć | automat stanów, prawo sterowania kinematycznego |
| Sterowniki urządzeń | jak rozmawiać ze sprzętem | generator impulsów STEP, obsługa serwa |
| HAL / BSP | abstrakcja mikrokontrolera | STM32 HAL, `HardwareTimer` |
| Sprzęt | | Nucleo-C031C6, A4988, silnik |

::: def
**Zasada:** każda warstwa korzysta tylko z warstwy pod sobą. Logikę sterowania można wtedy uruchomić na PC z atrapą sprzętu (*mock*) i przetestować bez płytki.
:::


## Modułowość: interfejsy zamiast zależności

- Moduł ma **wąski, jawny interfejs**: `rozpocznijJazde(cel)`, `ustawDrzwi(otwarte)`, a nie „globalną zmienną, którą wszyscy piszą”.
- W ROS 2 modułem jest **węzeł**, a interfejsem **temat, usługa lub akcja** z typem wiadomości (W08).
- Korzyści: praca zespołowa (w przemyśle każdy odpowiada za swój blok), wymienność (inny silnik, ta sama logika), testowalność.
- Wzorce przydatne w sterowaniu:
  - **automat stanów** (W03),
  - **pętla sterowania o stałym okresie**: odczyt → oblicz → zapis,
  - **publikuj/subskrybuj** (W08).


# Kontrola wersji


## Git w pigułce

:::: columns
::: {.column width="50%"}
```bash
git clone https://github.com/uczelnia/winda.git
git switch -c poprawka-debounce   # nowa gałąź
# ... edycja plików ...
git add sketch.ino
git commit -m "Debounce przycisków: 20 ms"
git push -u origin poprawka-debounce
# na GitHubie: Pull Request + przegląd kodu
```
:::
::: {.column width="50%"}
- **Commit**: migawka projektu z opisem *dlaczego* zmieniono.
- **Gałąź**: równoległa linia prac; `main` zawsze działa.
- **Pull Request**: propozycja zmiany + dyskusja + automatyczne testy.
- **Przegląd kodu**: najtańszy sposób znajdowania błędów.
- Wersjonuj **wszystko**: kod, `diagram.json`, URDF, konfiguracje.
:::
::::

::: uwaga
Na laboratoriach sprawozdanie prowadzisz w swoim repozytorium na GitHubie: commit po każdej części zajęć to naturalny dziennik postępów.
:::


# Testowanie


## Piramida testów w mechatronice

| Poziom | Co testujemy | Gdzie | Koszt i czas |
|---|---|---|---|
| test jednostkowy | funkcja, klasa, automat stanów | PC, milisekundy | najtańszy |
| test integracyjny | kilka modułów razem, np. węzły ROS 2 | PC / kontener | tani |
| **SIL** (*software-in-the-loop*) | pełny program + model obiektu | symulator: Wokwi, Gazebo | średni |
| **HIL** (*hardware-in-the-loop*) | prawdziwy sterownik + symulowany obiekt | stanowisko testowe | drogi |
| test na obiekcie | cały system | laboratorium, hala | najdroższy, ryzykowny |

Im niżej w piramidzie, tym więcej testów i tym wcześniej je uruchamiamy.


## Przykład: test logiki windy na PC

:::: columns
::: {.column width="50%"}
Program windy z L1 skompilowaliśmy **na zwykłym komputerze** z atrapą API Arduino:

- `digitalRead`/`digitalWrite` czytają i piszą tablicę,
- `millis()` zwraca symulowany czas,
- przerwanie timera wywołujemy „ręcznie” 800 razy na symulowaną sekundę,
- skrypt testowy wciska przyciski i sprawdza stany.
:::
::: {.column width="50%"}
```text
Wezwanie na pietro 2
[125 ms] POSTOJ -> JAZDA  (pietro 0)
[2124 ms] JAZDA -> DRZWI_OTWARTE  (pietro 2)
[5124 ms] DRZWI_OTWARTE -> POSTOJ  (pietro 2)
Wezwanie na pietro 0
[7125 ms] POSTOJ -> JAZDA  (pietro 2)
Wezwanie na pietro 1
[8124 ms] JAZDA -> DRZWI_OTWARTE  (pietro 1)
...
[16601 ms] JAZDA -> AWARIA  (pietro -1)
[17001 ms] AWARIA -> JAZDA  (pietro -1)
```
:::
::::

Wynik: sprawdzone zatrzymanie „po drodze”, awaria między piętrami i powrót. Bez płytki i bez symulatora.


## Ciągła integracja (CI)

:::: columns
::: {.column width="55%"}
- Każdy `push` uruchamia automatycznie: kompilację, testy, analizę statyczną, budowę dokumentacji.
- Błąd wykryty w minutę po commicie, a nie tydzień później na obiekcie.
- Narzędzia: **GitHub Actions**, GitLab CI, Jenkins.
- W mechatronice CI może też uruchamiać symulację: Wokwi CLI dla mikrokontrolerów, Gazebo w trybie bez okna (*headless*).
:::
::: {.column width="45%"}
```yaml
# .github/workflows/strona.yml (ten kurs!)
on: [push]
jobs:
  build:
    runs-on: ubuntu-24.04
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: pip install -r requirements-site.txt
      - run: python tools/build_site.py
      # ... publikacja na GitHub Pages
```
:::
::::

::: przyklad
Slajdy, które oglądasz, są plikami Markdown. Po każdym `push` GitHub Actions buduje je (pandoc + reveal.js) i publikuje na GitHub Pages.
:::


# Środowiska


## „U mnie działa”: powtarzalne środowiska

- Problem: różne wersje kompilatora, bibliotek, ROS 2, systemu operacyjnego.
- **Kontener** (Docker): obraz z dokładnie zadanymi wersjami. To samo środowisko u każdego i w CI.
- **Devcontainer** / **GitHub Codespaces**: kontener + edytor w przeglądarce.
- **The Construct** (L3, L4): gotowe środowiska ROS 2 + Gazebo w przeglądarce (*rosject*).
- **Google Colab** (L2, L5): notatnik Pythona z GPU w przeglądarce.
- Zasada: plik z wersjami (`requirements.txt`, `package.json`, `package.xml`) jest częścią repozytorium.


## Normy i bezpieczeństwo funkcjonalne

| Norma | Zakres |
|---|---|
| IEC 61508 | bezpieczeństwo funkcjonalne systemów E/E/PE (norma ogólna, poziomy SIL) |
| ISO 13849 | bezpieczeństwo układów sterowania maszyn (poziomy PL) |
| ISO 10218 | bezpieczeństwo robotów przemysłowych |
| ISO/TS 15066 | roboty współpracujące (koboty) |
| IEC 61131-3 | języki programowania sterowników PLC |
| MISRA C/C++ | zasady bezpiecznego stylu kodu w systemach wbudowanych |

- Wniosek praktyczny: funkcje bezpieczeństwa (STOP awaryjny) projektujemy **najpierw** i sprawdzamy **zawsze**, niezależnie od stanu automatu. Tak jest w programie windy.


## Podsumowanie

- Warstwy i wąskie interfejsy pozwalają testować logikę bez sprzętu.
- Git + przegląd kodu + CI to standard pracy zespołowej, także w mechatronice.
- Symulacja (SIL) i powtarzalne środowiska w chmurze skracają drogę od pomysłu do działającego systemu.
- Następny wykład: **ROS 2**, czyli architektura modułowa w praktyce robotyki.


## Źródła i dalsza lektura

- S. Chacon, B. Straub, *Pro Git*, 2nd ed., Apress, 2014, <https://git-scm.com/book/pl/v2> (wersja polska).
- GitHub Docs, *GitHub Actions*, <https://docs.github.com/actions>.
- Wokwi Docs, *Wokwi CI*, <https://docs.wokwi.com/wokwi-ci/getting-started>.
- J. W. Grenning, *Test Driven Development for Embedded C*, Pragmatic Bookshelf, 2011.
- E. A. Lee, S. A. Seshia, *Introduction to Embedded Systems: A Cyber-Physical Systems Approach*, 2nd ed., MIT Press, 2017 (wolna wersja online).
- ISO 10218-1/-2:2025 *Robotics: Safety requirements*; IEC 61508 *Functional safety of E/E/PE safety-related systems*.

