# L4. Robot UR5e w Gazebo: trzy sposoby sterowania

> **Systemy mechatroniczne · Laboratorium 4 (3 h akad.)**
> Wykłady powiązane: W06, W10, W11.
> Sylabus: La3 (logika kontrolno-sterująca), La1 (modelowanie i symulacje).

## Cel

Po zajęciach potrafisz:

- uruchomić symulację robota przemysłowego w **Gazebo Harmonic** z `ros2_control` i MoveIt (ROS 2 Jazzy),
- przełączać kontrolery i wybrać interfejs sterowania: pozycja wprost, trajektoria, planowanie ruchu,
- wysłać trajektorię przez akcję `FollowJointTrajectory` i odczytać informację zwrotną,
- użyć kinematyki odwrotnej MoveIt (`/compute_ik`) dla punktów kartezjańskich,
- porównać ilościowo metody sterowania (czas, prędkości, przyspieszenia) na zarejestrowanych danych.

## Środowisko: The Construct + `ur_simulation_gz`

Używamy oficjalnej symulacji Universal Robots: [`Universal_Robots_ROS2_GZ_Simulation`](https://github.com/UniversalRobots/Universal_Robots_ROS2_GZ_Simulation) (ROS 2 Jazzy + Gazebo Harmonic). Inspiracją było repozytorium [`ur_yt_sim`](https://github.com/LearnRoboticsWROS/ur_yt_sim) (UR5 + Robotiq w Gazebo Classic), ale Gazebo Classic nie jest już wspierane, więc przenieśliśmy zadanie na nowe Gazebo.

**Rosject przygotowany przez prowadzącego** (link na ePortalu): otwórz go i kliknij *Copy* (kopia do Twojego konta). Zawiera zainstalowane pakiety i przestrzeń roboczą z `l4_sterowanie`.

Jeśli pracujesz we własnym rosjekcie ROS 2 Jazzy, zainstaluj pakiety samodzielnie:

```bash
sudo apt update
sudo apt install -y ros-jazzy-ur ros-jazzy-ur-simulation-gz
git clone https://github.com/bpasz/pwr-systemy-mechatroniczne-dla-studenta.git ~/kurs
mkdir -p ~/ros2_ws/src && cp -r ~/kurs/laboratoria/L4-gazebo-ur5e/l4_sterowanie ~/ros2_ws/src/
cd ~/ros2_ws && colcon build --symlink-install
```

W każdym nowym terminalu: `source ~/ros2_ws/install/setup.bash`.

## Zasady zajęć

- **Pracujesz indywidualnie.** Zajęcia zaczynają się od zadania wprowadzającego (część prowadzona), potem każdy realizuje własny projekt.
- **Sprawozdanie piszesz w trakcie zajęć** i dokumentujesz w nim postępy pracy na bieżąco. Prowadzący ocenia je na zajęciach, nie ma terminu oddania po zajęciach.
- Na początku zajęć prowadzący **może** przeprowadzić krótką kartkówkę (ok. 10 min) z wykładów W10–W11.
- Aby zaliczyć laboratorium, trzeba zaliczyć **wszystkie sekcje** z tabeli kryteriów oceny.

## Przed zajęciami

1. Powtórz W11: `ros2_control`, kontrolery, akcja `FollowJointTrajectory`, MoveIt.
2. Skopiuj rosject prowadzącego i uruchom `ros2 launch ur_simulation_gz ur_sim_control.launch.py ur_type:=ur5e`. W oknie Gazebo i RViz powinien pojawić się robot.

## Plan zajęć (135 min)

| Czas | Część |
|---|---|
| 0:00–0:10 | Organizacja, kopia rosjectu, uruchomienie symulacji |
| 0:10–0:30 | Część 1: uruchomienie, kontrolery, tematy i akcje |
| 0:30–1:10 | Część 2: zadanie wprowadzające: trzy sposoby sterowania tą samą sekwencją pick & place |
| 1:10–2:05 | Część 3: projekt indywidualny: własna sekwencja, pomiary i porównanie |
| 2:05–2:15 | Przedstawienie sprawozdania i ocena u prowadzącego |

## Część 1: symulacja i kontrolery (20 min)

```bash
# terminal 1: Gazebo + ros2_control + RViz
ros2 launch ur_simulation_gz ur_sim_control.launch.py ur_type:=ur5e

# terminal 2:
ros2 control list_controllers                 # które są aktywne?
ros2 control list_hardware_interfaces         # interfejsy command/state
ros2 topic echo /joint_states --once
ros2 action list -t
ros2 run tf2_ros tf2_echo base_link tool0     # MTJ efektora (W04–W05)
```

**Pytania:**

1. Jakie interfejsy *command* i *state* ma każdy przegub? Który kontroler z nich korzysta?
2. Porównaj wynik `tf2_echo` z kinematyką prostą z L2: co jest tu odpowiednikiem `robot.fkm()`?

## Część 2: trzy sposoby sterowania (40 min)

Pakiet [`l4_sterowanie`](l4_sterowanie/) zawiera jedną sekwencję pick & place (bez chwytaka: „wirtualny chwyt”) w pliku [`wspolne.py`](l4_sterowanie/l4_sterowanie/wspolne.py) i trzy węzły. Przed każdym przebiegiem uruchom **rejestrator** w osobnym terminalu:

```bash
ros2 run l4_sterowanie rejestrator --ros-args -p plik:=nazwa.csv -p use_sim_time:=true   # Ctrl+C po ruchu
```

### Sposób 1: pozycja przegubów wprost

```bash
ros2 control load_controller --set-state inactive forward_position_controller
ros2 control switch_controllers --deactivate scaled_joint_trajectory_controller \
                                --activate forward_position_controller
ros2 run l4_sterowanie pozycja_wprost --ros-args -p okres:=2.0 -p interpolacja:=false -p use_sim_time:=true
ros2 run l4_sterowanie pozycja_wprost --ros-args -p okres:=2.0 -p interpolacja:=true  -p use_sim_time:=true
```

Obserwuj ruch w Gazebo. Bez interpolacji wartość zadana skacze: robot porusza się z maksymalną prędkością dopuszczoną przez symulator, a przy dużym skoku może wybrać **inną drogę**, niż się spodziewasz (sprawdź przegub `shoulder_pan` w ostatnim ruchu).

### Sposób 2: trajektoria przez akcję

```bash
ros2 control switch_controllers --deactivate forward_position_controller \
                                --activate scaled_joint_trajectory_controller
ros2 run l4_sterowanie trajektoria --ros-args -p okres:=2.0 -p use_sim_time:=true
```

Węzeł [`trajektoria.py`](l4_sterowanie/l4_sterowanie/trajektoria.py) wysyła całą sekwencję jako jedną trajektorię. Kontroler interpoluje ruch i co ok. 1 s raportuje maksymalny błąd śledzenia.

### Sposób 3: MoveIt: kinematyka odwrotna i planowanie

```bash
# zamknij terminal 1 i uruchom symulację z MoveIt:
ros2 launch ur_simulation_gz ur_sim_moveit.launch.py ur_type:=ur5e
ros2 run l4_sterowanie ik_trajektoria --ros-args -p use_sim_time:=true
```

Węzeł [`ik_trajektoria.py`](l4_sterowanie/l4_sterowanie/ik_trajektoria.py) zamienia punkty kartezjańskie z `PUNKTY_KARTEZJANSKIE` (narzędzie skierowane w dół) na konfiguracje usługą MoveIt `/compute_ik` i wysyła je jako trajektorię. Dodatkowo w RViz, w panelu **MotionPlanning**, przeciągnij znacznik chwytaka, kliknij *Plan* i *Execute*: MoveIt zaplanuje ruch bez kolizji.

**Pytania:**

1. Dlaczego w sposobie 2 robot zatrzymuje się w każdym punkcie pośrednim? (Wskazówka: `velocities` w punktach trajektorii.)
2. Które sposoby sprawdzają kolizje? Który wymaga od programisty rozwiązania kinematyki odwrotnej?
3. Po co funkcja `najblizszy_odpowiednik()` w `ik_trajektoria.py`? Co by się stało bez niej?

## Część 3: projekt indywidualny (55 min)

**Zadanie:** zaprojektuj własną operację pick & place i porównaj metody sterowania.

1. Wybierz **dwa miejsca odbioru i dwa miejsca odłożenia** (punkty kartezjańskie w zasięgu UR5e, ok. 0,85 m). Wpisz je do `PUNKTY_KARTEZJANSKIE` i wyznacz konfiguracje:
   `ros2 run l4_sterowanie ik_trajektoria --ros-args -p tylko_ik:=true -p use_sim_time:=true`. Uzupełnij `KONFIGURACJE_IK` i `SEKWENCJA` w `wspolne.py`.
2. Wykonaj sekwencję czterema wariantami: pozycja wprost bez interpolacji, z interpolacją, trajektoria (JTC), MoveIt IK + JTC. Każdy przebieg zarejestruj do CSV.
3. Porównaj wyniki skryptem:

   ```bash
   python3 ~/ros2_ws/src/l4_sterowanie/skrypty/porownaj.py wprost.csv wprost_interp.csv trajektoria.csv ik.csv
   ```

   Skrypt wypisuje tabelę (czas ruchu, maks. prędkość, maks. przyspieszenie przegubów) i zapisuje wykres `porownanie.png`.
4. **Rozszerzenie A (dla chętnych, płynność):** w `trajektoria.py` ustaw niezerowe prędkości w punktach pośrednich (np. różnice skończone między sąsiednimi punktami). Czy czas ruchu i przyspieszenia się zmieniły?
5. **Rozszerzenie B (dla chętnych, wirtualny chwyt w MoveIt):** w RViz dodaj pudełko w scenie planowania (*Scene Objects*), dołącz je do `tool0` (*Attach*) i zaplanuj przeniesienie. MoveIt uwzględni dołączony obiekt przy sprawdzaniu kolizji.
6. **Rozszerzenie C (dla chętnych, sterowanie kinematyczne z W06):** aktywuj `forward_velocity_controller` i napisz węzeł, który realizuje ruch efektora w dół z zadaną prędkością $\dot{q} = J^{\dagger(\epsilon)}\xi_d$. Jakobian możesz liczyć numerycznie z `/compute_fk` (MoveIt).

## Sprawozdanie (na zajęciach)

Sprawozdanie piszesz na bieżąco w trakcie zajęć, w katalogu `L4/` w swoim repozytorium (albo w formie wskazanej przez prowadzącego). Po każdej części dopisz wyniki i wnioski. Przed końcem zajęć przedstawiasz prowadzącemu sprawozdanie i pomiary; prowadzący ocenia je na miejscu.

Sprawozdanie zawiera:

- odpowiedzi na pytania z części 1 i 2,
- zmieniony `wspolne.py` (Twoje punkty i konfiguracje),
- pliki CSV, `porownanie.png`, tabelę i wnioski (5–8 zdań): który sposób wybrałbyś do jakiego zastosowania i dlaczego,
- opis wybranego rozszerzenia (jeśli zrobione).

### Kryteria oceny

| Sekcja | Punkty |
|---|---|
| Części 1–2: przebiegi i odpowiedzi | 30 |
| Projekt: własna sekwencja, 4 warianty, pomiary | 40 |
| Porównanie i wnioski | 30 |
| **Razem** | **100** |

**Warunek zaliczenia:** trzeba zaliczyć wszystkie sekcje z tabeli. Rozszerzenia A–C dają do 10 punktów dodatkowych. Jeśli odbyła się kartkówka, prowadzący podaje na początku zajęć, jak uwzględnia ją w ocenie.

## Źródła

- Universal Robots, *Universal_Robots_ROS2_GZ_Simulation* (gałąź `jazzy`), <https://github.com/UniversalRobots/Universal_Robots_ROS2_GZ_Simulation>.
- ros2_control Documentation (Jazzy), <https://control.ros.org/jazzy/>: *joint_trajectory_controller*, *forward_command_controller*.
- MoveIt 2 Documentation, <https://moveit.picknik.ai>: *MoveIt Quickstart in RViz*, usługa `GetPositionIK`.
- LearnRoboticsWROS, *ur_yt_sim* (Gazebo Classic, UR5 + Robotiq, MoveIt), <https://github.com/LearnRoboticsWROS/ur_yt_sim>; materiał wideo z założeń kursu: <https://www.youtube.com/watch?v=qnuwTOB4DKw>.
- Gazebo Harmonic Documentation, <https://gazebosim.org/docs/harmonic>.
