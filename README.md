# Systemy mechatroniczne (MID010706): materiały dla studentów

Materiały do kursu **Systemy mechatroniczne**, Politechnika Wrocławska, Wydział Elektroniki Mikrosystemów i Fotoniki (W12N), kierunek Inżynieria Mikrosystemów Mechatronicznych, studia I stopnia.

> **To repozytorium jest generowane automatycznie** z repozytorium kursu przy każdej aktualizacji materiałów. Nie wprowadzaj tu zmian bezpośrednio: zostaną nadpisane. Uwagi i poprawki zgłaszaj prowadzącemu.

**Wszystkie zajęcia odbywają się w przeglądarce:** Wokwi (STM32), Google Colab (UAIbot, LeRobot), The Construct (ROS 2, Gazebo). Nie musisz niczego instalować.

- Strona kursu ze slajdami i instrukcjami: <https://bpasz.github.io/pwr-systemy-mechatroniczne/>.
- Karta przedmiotu: [`w12n_..._sylabus_2022_2023-pages.pdf`](w12n_inzynieria_mikrosystemow_mechatronicznych_i_st_pl_sylabus_2022_2023-pages.pdf). Źródła zewnętrzne: [`ZRODLA.md`](ZRODLA.md).

## Zasady zaliczenia

- Wykład i laboratorium to **dwie niezależne oceny**. Ocena z wykładu wynika z kolokwium na ostatnim wykładzie (W15).
- Laboratoria są **indywidualne**: zadanie wprowadzające, potem własny projekt.
- Sprawozdanie piszesz **na zajęciach**, dokumentując postępy na bieżąco. Prowadzący ocenia je w trakcie zajęć; trzeba zaliczyć wszystkie sekcje z tabeli kryteriów.
- Na początku zajęć laboratoryjnych możliwa jest krótka kartkówka z wykładów powiązanych z danym laboratorium.

## Wykłady

Slajdy w katalogu [`wyklady/`](wyklady/) (Markdown; wygodniej czytać je na stronie kursu).

| # | Temat |
|---|---|
| [W01](wyklady/W01-wprowadzenie.md) | Czym jest system mechatroniczny |
| [W02](wyklady/W02-elektronika.md) | Elektronika analogowo-cyfrowa |
| [W03](wyklady/W03-stm32.md) | Mikrokontroler STM32 |
| [W04](wyklady/W04-opis-przestrzenny.md) | Opis przestrzenny |
| [W05](wyklady/W05-kinematyka.md) | Kinematyka prosta i odwrotna |
| [W06](wyklady/W06-sterowanie-kinematyczne.md) | Kinematyka różniczkowa i sterowanie kinematyczne |
| [W07](wyklady/W07-inzynieria-oprogramowania.md) | Inżynieria oprogramowania w systemach mechatronicznych |
| [W08](wyklady/W08-ros2.md) | ROS 2: architektura oprogramowania robota |
| [W09](wyklady/W09-komunikacja.md) | Moduły i układy komunikacyjne |
| [W10](wyklady/W10-napedy-pid.md) | Napędy elektryczne i regulator PID |
| [W11](wyklady/W11-sterowanie-robotem-ros2.md) | Sterowanie robotem w ROS 2 |
| [W12](wyklady/W12-uczenie-maszynowe.md) | Uczenie maszynowe: podstawy |
| [W13](wyklady/W13-wizja-akcja.md) | Od obrazu do ruchu: uczenie robotów z demonstracji |
| [W14](wyklady/W14-integracja.md) | Integracja systemu, trendy, powtórka |
| [W15](wyklady/W15-kolokwium.md) | Kolokwium zaliczeniowe |

## Laboratoria

| # | Temat | Narzędzie |
|---|---|---|
| [L1](laboratoria/L1-wokwi-stm32-winda/) | Winda na STM32: GPIO, przerwania, timery, automat stanów, dzwonek | Wokwi (Nucleo-C031C6) |
| [L2](laboratoria/L2-uaibot-kinematyka/) | Kinematyka i sterowanie kinematyczne manipulatora | UAIbot (Python, Colab) |
| [L3](laboratoria/L3-ros2-podstawy/) | ROS 2: węzły, tematy, usługi, regulator | ROS 2 Jazzy (The Construct) |
| [L4](laboratoria/L4-gazebo-ur5e/) | UR5e w Gazebo: trzy sposoby sterowania | Gazebo Harmonic + ros2_control + MoveIt |
| [L5](laboratoria/L5-lerobot-wizja-akcja/) | Polityki wizja → akcja, uczenie z demonstracji | LeRobot (Colab, GPU) |

Każde laboratorium ma instrukcję (`README.md`) oraz pliki startowe: szkielety programów, pakiety ROS 2, notatniki Colab.
