# Alternatywa dla L3 i L4: ROS 2 i Gazebo w GitHub Codespaces

> **Systemy mechatroniczne · środowisko alternatywne dla [L3](../L3-ros2-podstawy/README.md) i [L4](../L4-gazebo-ur5e/README.md)**
> Zamiast The Construct możesz pracować w GitHub Codespaces: ten sam ROS 2 Jazzy i Gazebo Harmonic, okna graficzne na pulpicie w przeglądarce.

## Cel

Środowisko do wyboru, nie obowiązek. Przyda się, gdy:

- skończył się miesięczny limit godzin w The Construct albo rosject długo się uruchamia,
- chcesz mieć kod i sprawozdanie od razu w repozytorium Git (własny *fork*),
- chcesz pracować tak samo jak w L2 (Codespaces), bez kolejnego konta.

Instrukcje L3 i L4 obowiązują bez zmian; różnice opisuje sekcja [„Różnice względem instrukcji L3 i L4”](#różnice-względem-instrukcji-l3-i-l4). Zasady zajęć, sprawozdanie i kryteria oceny są takie same.

## Środowisko

Konfiguracja `.devcontainer/ros2/` w repozytorium dla studentów:

| Element | Zawartość |
|---|---|
| Obraz | `osrf/ros:jazzy-desktop` (Ubuntu 24.04, ROS 2 Jazzy, RViz, rqt, turtlesim) |
| Dodatkowe pakiety | `ros_gz` (Gazebo Harmonic), `ur`, `ur_simulation_gz` (UR5e z `ros2_control` i MoveIt), matplotlib |
| Pulpit | cecha `desktop-lite`: lekki pulpit (Fluxbox) przez VNC, w przeglądarce przez **noVNC na porcie 6080**, bez hasła |
| Maszyna | co najmniej **4 rdzenie, 16 GB RAM**; do L4 zalecane **8 rdzeni** |
| Grafika | renderowanie programowe na procesorze (Mesa llvmpipe, OpenGL 4.5), Codespaces nie mają GPU |

### Limity GitHub Codespaces

Darmowe konto GitHub ma miesięcznie **120 rdzeniogodzin** i 15 GB miejsca. Maszyna 4-rdzeniowa zużywa 4 rdzeniogodziny na godzinę pracy, więc wystarcza na ok. **30 h**, a 8-rdzeniowa na ok. 15 h. Z pakietem [GitHub Education](https://education.github.com/pack) (konto Pro) limit wynosi 180 rdzeniogodzin (ok. 45 h na 4 rdzeniach).

- **Zatrzymuj codespace po zajęciach** (*Code → Codespaces → … → Stop codespace*). Bezczynny zatrzymuje się sam po 30 min, ale do tego czasu zużywa limit.
- Po zakończeniu L4 usuń codespace (*Delete*), żeby nie zajmował miejsca. Wcześniej zacommituj sprawozdanie.

## Przed zajęciami

1. Zaloguj się do GitHub (konto zakładamy na zajęciach L2) i otwórz repozytorium dla studentów.
2. Utwórz codespace z konfiguracją ROS 2, jednym z dwóch sposobów:
   - kliknij: [**Otwórz w Codespaces (ROS 2)**](https://codespaces.new/bpasz/pwr-systemy-mechatroniczne-dla-studenta?devcontainer_path=.devcontainer/ros2/devcontainer.json), wybierz *Machine type* (4-core do L3, 8-core do L4) i *Create codespace*,
   - albo: *Code → Codespaces → … → New with options*, w polu *Dev container configuration* wybierz **ROS 2 Jazzy + Gazebo (L3, L4)**.
3. Pierwsze uruchomienie buduje obraz i trwa kilka do kilkunastu minut. Kolejne (po *Stop* i ponownym otwarciu) trwają kilkadziesiąt sekund. Dlatego najlepiej utwórz codespace **przed zajęciami**.
4. Sprawdź pulpit i ROS 2: wykonaj kroki z sekcji [„Pulpit w przeglądarce”](#pulpit-w-przeglądarce) i uruchom w terminalu `ros2 run turtlesim turtlesim_node`. Okno żółwia pojawi się na pulpicie.

## Pulpit w przeglądarce

1. W VS Code otwórz zakładkę **Ports** (panel dolny, obok *Terminal*). Port **6080** ma etykietę *Pulpit (noVNC)*.
2. Kliknij ikonę globusa (*Open in Browser*). Otworzy się nowa karta z noVNC.
3. Najwygodniej dopisz do adresu `vnc.html?autoconnect=true&resize=remote`: pulpit połączy się sam i dopasuje rozdzielczość do okna karty. Bez tego kliknij *Connect* (hasło nie jest wymagane).
4. Polecenia wpisujesz w **terminalu VS Code** (*Terminal → New Terminal*, możesz otworzyć kilka). Programy graficzne (turtlesim, `rqt_graph`, Gazebo, RViz) otwierają się na pulpicie, bo zmienna `DISPLAY=:1` jest już ustawiona.
5. Schowek: wysuwany panel noVNC po lewej stronie ma pole *Clipboard* do przenoszenia tekstu między przeglądarką a pulpitem.

> **Port 6080 jest prywatny:** widzisz go tylko Ty, po zalogowaniu do GitHub. Nie zmieniaj jego widoczności na *Public*: pulpit nie ma hasła.

## Różnice względem instrukcji L3 i L4

| Instrukcja (The Construct) | Codespaces |
|---|---|
| rosject ROS 2 Jazzy, rosject prowadzącego do L4 | codespace z konfiguracją **ROS 2 Jazzy + Gazebo (L3, L4)**; pakiety do L4 są już zainstalowane |
| *Graphical Tools* | pulpit noVNC (port 6080) |
| *Terminal*, *Code Editor* | terminal i edytor VS Code |
| `git clone https://github.com/bpasz/pwr-systemy-mechatroniczne-dla-studenta.git ~/kurs` | **pomiń**: `~/kurs` wskazuje już na repozytorium otwarte w codespace (`/workspaces/...`) |
| `source /opt/ros/jazzy/setup.bash` | ładowane automatycznie w każdym terminalu; po zbudowaniu `~/ros2_ws` także `install/setup.bash` |

Pozostałe polecenia (`cp -r ~/kurs/laboratoria/... ~/ros2_ws/src/`, `colcon build`, `ros2 launch`, `ros2 run`) wpisujesz dokładnie tak, jak w instrukcjach.

### Gdzie zapisywać pracę

- `~/ros2_ws` przetrwa zatrzymanie i ponowne uruchomienie codespace, ale **nie** jego przebudowę (*Rebuild Container*) ani usunięcie.
- Sprawozdanie, pliki CSV i wykresy zapisuj w repozytorium (`~/kurs`, czyli `/workspaces/...`), np. w katalogu `sprawozdania/L3/`. Zmienione pliki pakietu skopiuj tam przed końcem zajęć.
- Commit z codespace otwartego na repozytorium dla studentów: VS Code zaproponuje utworzenie *forka* i wypchnie zmiany do Twojej kopii.

### Wydajność (L4)

Gazebo i RViz rysują scenę na procesorze, więc działają wolniej niż w The Construct z GPU. Symulacja korzysta z czasu symulacji (`use_sim_time:=true` w poleceniach L4), więc spowolnienie nie psuje pomiarów, tylko wydłuża przebiegi.

- Wybierz maszynę **8-rdzeniową** (zmiana typu: *Code → Codespaces → … → Change machine type*).
- Jeśli obraz się tnie, uruchom symulację bez okna Gazebo, a robota oglądaj w RViz:
  `ros2 launch ur_simulation_gz ur_sim_control.launch.py ur_type:=ur5e gazebo_gui:=false`.
- Zamykaj okna, których nie potrzebujesz (`rqt`, drugi RViz).

## Rozwiązywanie problemów

| Objaw | Co zrobić |
|---|---|
| Nie ma portu 6080 w zakładce *Ports* | Poczekaj, aż codespace skończy się uruchamiać (pulpit startuje razem z kontenerem). Jeśli dalej brak: *Ports → Forward a Port → 6080*. |
| `cannot open display` przy uruchamianiu okna | W terminalu: `echo $DISPLAY` ma pokazać `:1`. Terminal otwarty przed startem pulpitu: zamknij go i otwórz nowy. |
| `Package 'l3_regulator' not found` | Nie wykonano `source ~/ros2_ws/install/setup.bash` po `colcon build` (albo otwórz nowy terminal). |
| Codespace nie tworzy się z powodu limitu | Sprawdź zużycie: *GitHub → Settings → Billing and plans → Codespaces*. Wróć do The Construct na resztę miesiąca. |

## Źródła

- GitHub Docs, *Codespaces: billing* i *Setting your default machine type*, <https://docs.github.com/en/codespaces>.
- Dev Containers, cecha *desktop-lite* (Light-weight Desktop, noVNC), <https://github.com/devcontainers/features/tree/main/src/desktop-lite>.
- Open Robotics, obrazy Docker `osrf/ros`, <https://hub.docker.com/r/osrf/ros>.
- Universal Robots, *Universal_Robots_ROS2_GZ_Simulation*, <https://github.com/UniversalRobots/Universal_Robots_ROS2_GZ_Simulation>.
