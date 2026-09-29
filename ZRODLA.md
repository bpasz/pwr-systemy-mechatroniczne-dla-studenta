# Wykaz wykorzystanych materiałów zewnętrznych

Materiały kursu są własne, z wyjątkiem elementów wymienionych poniżej. Każdy slajd z treścią przetłumaczoną lub zaadaptowaną ma przypis „Na podst.: …” lub „Rysunek/Animacja: …”, a każdy wykład i każda instrukcja kończy się listą źródeł.

## UAIbot: Robotic Manipulators (V. M. Gonçalves i in.)

- Źródło: <https://uaibot.github.io/class_presentations/>, repozytorium <https://github.com/UAIbot/UAIbot.github.io>.
- Wykorzystanie:
  - **tłumaczenie i skrót** treści wykładów Class 1–5 (EN) na język polski: wykłady [W04](wyklady/W04-opis-przestrzenny.md), [W05](wyklady/W05-kinematyka.md), [W06](wyklady/W06-sterowanie-kinematyczne.md), fragmenty [W01](wyklady/W01-wprowadzenie.md);
  - **rysunki** (35 plików) skopiowane do `wyklady/assets/uaibot/`; w kilku SVG etykiety portugalskie przetłumaczono na polski (np. „Força” → „Siła”, „sen” → „sin”);
  - **animacje interaktywne** osadzone przez `<iframe>` bezpośrednio ze strony uaibot.github.io (bez kopiowania);
  - **przykłady kodu** Pythona (sterowanie kinematyczne, kinematyka odwrotna 2R) w W05, W06 i notatniku [L2](laboratoria/L2-uaibot-kinematyka/), z nazwami zmiennych przetłumaczonymi na polski.
- Licencja: repozytorium strony ma plik `LICENSE` (MIT, dotyczy motywu *just-the-docs*). Kurs jest opisany przez autorów jako materiał dla prowadzących („Enhance your lectures with ready-made presentations”), ale bez osobnej licencji na treść. **Przed publikacją strony kursu warto potwierdzić zgodę autorów** (kontakt przez repozytorium UAIbot).

## LeRobot (Hugging Face)

- Źródło: <https://github.com/huggingface/lerobot> (Apache-2.0), dokumentacja <https://huggingface.co/docs/lerobot>, zbiór `lerobot/pusht` i model `lerobot/diffusion_pusht` na Hugging Face Hub.
- Wykorzystanie: polecenia CLI i API w W13 i [L5](laboratoria/L5-lerobot-wizja-akcja/). Skrypt [`migruj_polityke.py`](laboratoria/L5-lerobot-wizja-akcja/migruj_polityke.py) importuje oryginalny moduł migracji LeRobot i podmienia jedną funkcję (poprawka błędu), bez kopiowania kodu.

## Universal Robots: symulacja w Gazebo

- Źródło: <https://github.com/UniversalRobots/Universal_Robots_ROS2_GZ_Simulation> (BSD-3-Clause), pakiety `ur_description`, `ur_moveit_config`, `ur_robot_driver`.
- Wykorzystanie: środowisko L4; nazwy kontrolerów i pliki launch opisane w W11 i [L4](laboratoria/L4-gazebo-ur5e/). Kod pakietu `l4_sterowanie` jest własny.
- Inspiracja: LearnRoboticsWROS, `ur_yt_sim` (<https://github.com/LearnRoboticsWROS/ur_yt_sim>), materiał wideo <https://www.youtube.com/watch?v=qnuwTOB4DKw>.

## The Construct

- Platforma <https://app.theconstruct.ai> i playlista *ROS 2 Crash Course* (YouTube): środowisko L3–L4 i materiał do samodzielnego przygotowania. Nic nie kopiowano.

## Wokwi i STM32duino

- Wokwi Docs (<https://docs.wokwi.com>): nazwy pinów płytki `board-st-nucleo-c031c6` i części (A4988, silnik krokowy, serwo, przycisk), tabela symulowanych peryferiów w W03.
- STM32duino (<https://github.com/stm32duino/Arduino_Core_STM32>): API `HardwareTimer`, mapa pinów wariantu `NUCLEO_C031C6` (timery i kanały PWM).

## Oprogramowanie budujące stronę

- reveal.js 5.2.1 (MIT), KaTeX 0.16 (MIT), pandoc (GPL, używany jako narzędzie, nie dystrybuowany).

## Literatura

Pełne opisy bibliograficzne są na ostatnim slajdzie każdego wykładu. Podstawowe pozycje: Siciliano i in. *Robotics: Modelling, Planning and Control*; Lynch, Park *Modern Robotics*; Isermann *Mechatronic Systems*; Bolton *Mechatronics*; Horowitz, Hill *The Art of Electronics*; Åström, Murray *Feedback Systems*; Goodfellow i in. *Deep Learning*; dokumentacje ROS 2, ros2_control, MoveIt, Gazebo, LeRobot oraz RM0490 (STM32C0).
