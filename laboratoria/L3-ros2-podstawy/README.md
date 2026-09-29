# L3. ROS 2: węzły, tematy, usługi i regulator

> **Systemy mechatroniczne · Laboratorium 3 (3 h akad.)**
> Wykłady powiązane: [W07](../../wyklady/W07-inzynieria-oprogramowania.md), [W08](../../wyklady/W08-ros2.md), [W09](../../wyklady/W09-komunikacja.md).
> Sylabus: La4 (moduły i układy komunikacyjne), La3 (logika kontrolno-sterująca).

## Cel

Po zajęciach potrafisz:

- posługiwać się narzędziami wiersza poleceń ROS 2 (`node`, `topic`, `service`, `param`, `bag`),
- utworzyć pakiet Pythona w przestrzeni roboczej i zbudować go `colcon`,
- napisać węzły publikujące i subskrybujące, z parametrami i usługą,
- uruchomić układ węzłów plikiem launch,
- zdiagnozować niezgodność QoS,
- zaimplementować prosty regulator ruchu robota mobilnego w pętli ROS 2.

## Środowisko: The Construct

- <https://app.theconstruct.ai>: ROS 2 w przeglądarce, bez instalacji.
- Utwórz **rosject** z obrazem **ROS 2 Jazzy** (Ubuntu 24.04). W rosjekcie masz terminale (*Terminal*), edytor kodu (*Code Editor*) i okno graficzne (*Graphical Tools*), w którym wyświetla się `turtlesim` i `rqt`.
- Darmowe konto ma miesięczny limit godzin. Zamykaj rosject po zajęciach.

> **Wskazówka:** w każdym nowym terminalu ROS 2 jest już załadowany. Po zbudowaniu własnego pakietu wykonaj w każdym terminalu `source ~/ros2_ws/install/setup.bash`.

## Zasady zajęć

- **Pracujesz indywidualnie.** Zajęcia zaczynają się od zadania wprowadzającego (część prowadzona), potem każdy realizuje własny projekt.
- **Sprawozdanie piszesz w trakcie zajęć** i dokumentujesz w nim postępy pracy na bieżąco. Prowadzący ocenia je na zajęciach, nie ma terminu oddania po zajęciach.
- Na początku zajęć prowadzący **może** przeprowadzić krótką kartkówkę (ok. 10 min) z wykładów W07–W09.
- Aby zaliczyć laboratorium, trzeba zaliczyć **wszystkie sekcje** z tabeli kryteriów oceny.

## Przed zajęciami

1. Załóż konto w The Construct i utwórz rosject ROS 2 Jazzy.
2. Obejrzyj pierwsze odcinki playlisty [**ROS 2 Crash Course**](https://www.youtube.com/playlist?list=PLK0b4e05LnzYNBzqXNm9vFD9YXWp6honJ) kanału The Construct (pojęcia: węzeł, temat, wiadomość).
3. Uruchom w rosjekcie `ros2 run turtlesim turtlesim_node` (okno w *Graphical Tools*) i w drugim terminalu `ros2 run turtlesim turtle_teleop_key`. Porusz żółwiem strzałkami.

## Plan zajęć (135 min)

| Czas | Część |
|---|---|
| 0:00–0:10 | Organizacja, uruchomienie rosjectu |
| 0:10–0:40 | Część 1: zadanie wprowadzające: narzędzia CLI na przykładzie `turtlesim` |
| 0:40–1:15 | Część 2: pakiet `l3_regulator`: czujnik + regulator + launch + QoS |
| 1:15–2:05 | Część 3: projekt indywidualny „Żółw objeżdża trasę” |
| 2:05–2:15 | Przedstawienie sprawozdania i ocena u prowadzącego |

## Część 1: narzędzia CLI (30 min)

Terminal 1: `ros2 run turtlesim turtlesim_node`. W terminalu 2 wykonuj kolejno i notuj odpowiedzi:

```bash
ros2 node list                                   # jakie węzły działają?
ros2 node info /turtlesim                        # jakie tematy, usługi, parametry ma węzeł?
ros2 topic list -t                               # tematy z typami wiadomości
ros2 interface show turtlesim/msg/Pose           # z jakich pól składa się wiadomość?
ros2 topic echo /turtle1/pose                    # położenie żółwia (Ctrl+C kończy)
ros2 topic hz /turtle1/pose                      # z jaką częstotliwością?
ros2 topic pub --rate 1 /turtle1/cmd_vel geometry_msgs/msg/Twist \
  "{linear: {x: 2.0}, angular: {z: 1.8}}"        # jazda po okręgu
ros2 service list
ros2 service call /spawn turtlesim/srv/Spawn "{x: 2.0, y: 2.0, theta: 0.0, name: 'zolw2'}"
ros2 service call /turtle1/teleport_absolute turtlesim/srv/TeleportAbsolute "{x: 5.5, y: 5.5, theta: 0.0}"
ros2 param list /turtlesim
ros2 param set /turtlesim background_r 150
ros2 service call /clear std_srvs/srv/Empty
ros2 bag record -o jazda /turtle1/cmd_vel /turtle1/pose   # nagraj 20 s jazdy z klawiatury, Ctrl+C
ros2 bag info jazda
```

W *Graphical Tools* uruchom `rqt_graph` i narysuj graf węzłów i tematów do sprawozdania.

**Pytania:**

1. Jakie pola ma `turtlesim/msg/Pose`? W jakich jednostkach jest `theta`?
2. Czym różni się temat `/turtle1/cmd_vel` od usługi `/spawn` (wzorzec komunikacji, kiedy używać)?
3. Odtwórz nagranie `ros2 bag play jazda` po `teleport_absolute` do punktu startu. Czy żółw powtarza trasę? Dlaczego nie idealnie?

## Część 2: pakiet `l3_regulator` (35 min)

Wirtualny czujnik mierzy odległość żółwia od prawej ściany. Regulator PI utrzymuje zadaną odległość, sterując prędkością liniową.

```text
/turtlesim --/turtle1/pose--> /czujnik --/odleglosc--> /regulator --/turtle1/cmd_vel--> /turtlesim
```

### Krok 1: przestrzeń robocza i pakiet

```bash
git clone https://github.com/bpasz/pwr-systemy-mechatroniczne.git ~/kurs   # poza ~/ros2_ws!
mkdir -p ~/ros2_ws/src
cp -r ~/kurs/laboratoria/L3-ros2-podstawy/l3_regulator ~/ros2_ws/src/
cd ~/ros2_ws
colcon build --symlink-install --packages-select l3_regulator
source install/setup.bash
```

Obejrzyj pliki: [`package.xml`](l3_regulator/package.xml) (zależności), [`setup.py`](l3_regulator/setup.py) (programy `czujnik` i `regulator`), [`czujnik.py`](l3_regulator/l3_regulator/czujnik.py), [`regulator.py`](l3_regulator/l3_regulator/regulator.py), [`uklad.launch.py`](l3_regulator/launch/uklad.launch.py).

> `--symlink-install`: zmiany w plikach `.py` działają bez ponownego budowania. Nowy program w `setup.py` wymaga ponownego `colcon build`.

### Krok 2: uruchomienie i strojenie

```bash
ros2 launch l3_regulator uklad.launch.py zadana:=3.0 Kp:=1.0
# drugi terminal:
ros2 topic echo /odleglosc
ros2 param set /regulator zadana 1.5            # zmiana wartości zadanej w locie
ros2 param set /regulator Kp 4.0
ros2 service call /regulator/wlacz std_srvs/srv/SetBool "{data: false}"   # wyłącz regulację
ros2 service call /regulator/wlacz std_srvs/srv/SetBool "{data: true}"
```

1. Zmieniaj `zadana` między 1,5 a 4,0 i obserwuj odpowiedź dla $K_p$ = 0,5; 1; 4. Uwaga na ścianę: żółw zatrzymuje się na krawędzi okna.
2. Zwiększ szum czujnika: `ros2 param set /czujnik szum 0.3`. Co widać w `cmd_vel` przy dużym $K_p$?
3. Dodaj człon I (`Ki` = 0,5). Czy potrzebny jest w tym układzie? (Wskazówka: jaki jest model żółwia od `cmd_vel` do położenia?)

### Krok 3: eksperyment z QoS

1. W `czujnik.py` zmień wydawcę na profil dla danych czujników:

   ```python
   from rclpy.qos import qos_profile_sensor_data
   self.pub = self.create_publisher(Float32, 'odleglosc', qos_profile_sensor_data)
   ```

2. Uruchom układ ponownie. Regulator przestaje reagować. Sprawdź: `ros2 topic info -v /odleglosc`. Porównaj *Reliability* wydawcy i subskrybenta.
3. Popraw subskrybenta w `regulator.py` tak, aby komunikacja działała. Wyjaśnij w sprawozdaniu, kiedy `BEST_EFFORT` jest właściwym wyborem.

## Część 3: projekt indywidualny „Żółw objeżdża trasę” (50 min)

Napisz węzeł `do_punktu`, który prowadzi żółwia kolejno przez listę punktów (domyślnie kwadrat `(8,3) → (8,8) → (3,8) → (3,3)`).

**Wymagania:**

1. Pętla sterowania z timerem 20 Hz: subskrypcja `/turtle1/pose`, publikacja `/turtle1/cmd_vel`.
2. Regulator P odległości (prędkość liniowa) i P kąta (prędkość kątowa, `angular.z`). Kąt do celu z `atan2`, błąd kąta sprowadzony do przedziału $[-\pi, \pi)$.
3. Prędkość liniowa zmniejszana, gdy żółw jest źle ustawiony (np. mnożnik $\max(0, \cos e_\theta)$), obie prędkości ograniczone parametrami `v_max`, `w_max`.
4. Punkty jako parametry `punkty_x`, `punkty_y` (listy liczb), tolerancja osiągnięcia jako parametr.
5. Po osiągnięciu punktu publikacja numeru punktu na temacie `/osiagniety_punkt` (`std_msgs/msg/Int32`) i log `get_logger().info(...)`.
6. Wpis w `setup.py` (`'do_punktu = l3_regulator.do_punktu:main'`) i ponowne `colcon build`.

**Eksperymenty do sprawozdania:**

- nagraj `/turtle1/pose` podczas jednego okrążenia: `ros2 topic echo /turtle1/pose --csv > trasa.csv`, narysuj trasę $(x, y)$ w Pythonie (matplotlib),
- porównaj trasy dla dwóch zestawów wzmocnień (np. `K_w` = 1 i 6): czas okrążenia, „ścinanie” narożników,
- (dla chętnych) zamień listę punktów na **akcję** albo usługę „jedź do punktu”, tak jak robi to MoveIt w L4.

## Sprawozdanie (na zajęciach)

Sprawozdanie piszesz na bieżąco w trakcie zajęć, w katalogu `L3/` w swoim repozytorium (albo w formie wskazanej przez prowadzącego). Po każdej części dopisz wyniki i wnioski. Przed końcem zajęć przedstawiasz prowadzącemu sprawozdanie i działający układ węzłów; prowadzący ocenia je na miejscu.

Sprawozdanie zawiera:

- odpowiedzi z części 1 i graf `rqt_graph`,
- wnioski ze strojenia regulatora i eksperymentu QoS (z poprawionym kodem),
- kod `do_punktu.py` i poprawiony `setup.py`, wykresy tras, porównanie wzmocnień.

### Kryteria oceny

| Sekcja | Punkty |
|---|---|
| Część 1: odpowiedzi, graf | 20 |
| Część 2: strojenie, QoS (diagnoza i poprawka) | 25 |
| Projekt: wymagania 1–6 | 35 |
| Eksperymenty i wykresy | 20 |
| **Razem** | **100** |

**Warunek zaliczenia:** trzeba zaliczyć wszystkie sekcje z tabeli. Zadanie dla chętnych (akcja lub usługa „jedź do punktu”) daje do 10 punktów dodatkowych. Jeśli odbyła się kartkówka, prowadzący podaje na początku zajęć, jak uwzględnia ją w ocenie.

## Źródła

- ROS 2 Documentation (Jazzy), *Beginner: CLI tools* i *Beginner: Client libraries* (tutoriale z turtlesim): <https://docs.ros.org/en/jazzy/Tutorials.html>.
- ROS 2, *About Quality of Service settings*: <https://docs.ros.org/en/jazzy/Concepts/Intermediate/About-Quality-of-Service-Settings.html>.
- The Construct, *ROS 2 Crash Course* (YouTube): <https://www.youtube.com/playlist?list=PLK0b4e05LnzYNBzqXNm9vFD9YXWp6honJ>; platforma <https://app.theconstruct.ai>.
