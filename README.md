# Systemy mechatroniczne (MID010706): laboratoria

Instrukcje i pliki startowe do laboratoriów z kursu **Systemy mechatroniczne**, Politechnika Wrocławska, Wydział Elektroniki Mikrosystemów i Fotoniki (W12N), kierunek Inżynieria Mikrosystemów Mechatronicznych, studia I stopnia.

> **To repozytorium jest generowane automatycznie** z repozytorium kursu przy każdej aktualizacji materiałów. Nie wprowadzaj tu zmian bezpośrednio: zostaną nadpisane. Pracuj na własnej kopii (*fork*) albo w GitHub Codespaces. Uwagi i poprawki zgłaszaj prowadzącemu.

## Zasady zajęć

- Laboratoria są **indywidualne**: zadanie wprowadzające, potem własny projekt.
- Sprawozdanie piszesz **na zajęciach**, dokumentując postępy na bieżąco. Prowadzący ocenia je w trakcie zajęć; trzeba zaliczyć wszystkie sekcje z tabeli kryteriów.
- Na początku zajęć możliwa jest krótka kartkówka z wykładów powiązanych z danym laboratorium.

## Laboratoria

| # | Temat | Narzędzie |
|---|---|---|
| [L1](laboratoria/L1-wokwi-stm32-winda/) | Winda na STM32: GPIO, przerwania, timery, automat stanów, dzwonek | Wokwi (Nucleo-C031C6) |
| [L2](laboratoria/L2-uaibot-kinematyka/) | Kinematyka i sterowanie kinematyczne manipulatora | UAIbot (Python, Colab lub Codespaces) |
| [L3](laboratoria/L3-ros2-podstawy/) | ROS 2: węzły, tematy, usługi, regulator | ROS 2 Jazzy (The Construct) |
| [L4](laboratoria/L4-gazebo-ur5e/) | UR5e w Gazebo: trzy sposoby sterowania | Gazebo Harmonic + ros2_control + MoveIt (The Construct) |
| [L5](laboratoria/L5-lerobot-wizja-akcja/) | Polityki wizja → akcja, uczenie z demonstracji | LeRobot (Colab, GPU) |

Każde laboratorium ma instrukcję (`README.md`) oraz pliki startowe: szkielety programów, pakiety ROS 2, notatniki.

## Gdzie pracować

Wszystkie zajęcia odbywają się w przeglądarce; nie musisz niczego instalować.

- **L1:** <https://wokwi.com> (symulator STM32).
- **L2:** Google Colab (przycisk „Open in Colab” w instrukcji) albo **GitHub Codespaces**: przycisk *Code → Codespaces → Create codespace on main*. Codespace ma Pythona z Jupyterem i biblioteką UAIbot; otwórz notatnik `laboratoria/L2-uaibot-kinematyka/L2_uaibot.ipynb`.
- **L3, L4:** The Construct (<https://app.theconstruct.ai>), obraz ROS 2 Jazzy. Pliki pakietów kopiujesz poleceniem `git clone` z instrukcji.
- **L5:** Google Colab z GPU (przycisk „Open in Colab” w instrukcji).
