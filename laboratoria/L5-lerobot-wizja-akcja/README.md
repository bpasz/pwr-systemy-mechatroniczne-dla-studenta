# L5. Od obrazu do ruchu: polityki LeRobot w symulacji PushT

> **Systemy mechatroniczne · Laboratorium 5 (3 h akad.) + termin uzupełniający**
> Wykłady powiązane: W12, W13.
> Sylabus: La5 (implementacja technik uczenia maszynowego w systemach mechatronicznych; termin uzupełniający).

[![Otwórz w Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/bpasz/pwr-systemy-mechatroniczne-dla-studenta/blob/main/laboratoria/L5-lerobot-wizja-akcja/L5_lerobot.ipynb)

## Cel

Po zajęciach potrafisz:

- opisać zbiór demonstracji robota w formacie LeRobotDataset (obserwacje, stany, akcje, epizody),
- uruchomić gotową politykę wizja → akcja (Diffusion Policy) w symulatorze i ocenić ją ilościowo,
- wytrenować własną politykę metodą uczenia z demonstracji i porównać ją z modelem gotowym,
- wskazać ograniczenia polityk uczonych (dane, kumulacja błędów, obliczenia) i ich miejsce w systemie mechatronicznym.

## Środowisko

- **Google Colab z GPU** (T4 w darmowym planie): przycisk „Open in Colab” powyżej, potem *Środowisko wykonawcze → Zmień typ → GPU*.
- Instalacja w notatniku: `pip install 'lerobot[pusht,diffusion,training]'` (LeRobot 0.6.x, Python ≥ 3.12). Dodatki: `pusht` = symulator, `diffusion` = Diffusion Policy, `training` = trening.
- Darmowy Colab ma limity czasu GPU. Jeśli GPU jest niedostępne, notatnik działa na CPU z mniejszą liczbą epizodów i kroków (wyniki poglądowe). Wtedy w części 3–4 prowadzący ocenia przygotowanie i uruchomienie treningu oraz analizę, a nie skuteczność wytrenowanej polityki.

## Zasady zajęć

- **Pracujesz indywidualnie.** Zajęcia zaczynają się od zadania wprowadzającego (część prowadzona), potem każdy realizuje własny projekt.
- **Sprawozdanie piszesz w trakcie zajęć** i dokumentujesz w nim postępy pracy na bieżąco. Prowadzący ocenia je na zajęciach, nie ma terminu oddania po zajęciach.
- Na początku zajęć prowadzący **może** przeprowadzić krótką kartkówkę (ok. 10 min) z wykładów W12–W13.
- Aby zaliczyć laboratorium, trzeba zaliczyć **wszystkie sekcje** z tabeli kryteriów oceny.

## Przed zajęciami

1. Powtórz W12–W13: klonowanie zachowań, ACT, Diffusion Policy.
2. Otwórz notatnik w Colab, włącz GPU, uruchom pierwsze dwie komórki (instalacja trwa ok. 2–3 min).
3. Obejrzyj zbiór w przeglądarce: [LeRobot Dataset Visualizer: lerobot/pusht](https://huggingface.co/spaces/lerobot/visualize_dataset?path=%2Flerobot%2Fpusht%2Fepisode_0).

## Plan zajęć (135 min)

| Czas | Część |
|---|---|
| 0:00–0:10 | Organizacja, uruchomienie notatnika z GPU |
| 0:10–0:30 | 1. Zadanie wprowadzające: zbiór demonstracji `lerobot/pusht` |
| 0:30–0:55 | 2. Gotowa Diffusion Policy: migracja, ewaluacja, filmy |
| 0:55–1:40 | 3. Trening własnej polityki (w tle) + analiza filmów polityki gotowej |
| 1:40–2:05 | 4. Projekt indywidualny: ewaluacja własnej polityki, porównanie, eksperyment |
| 2:05–2:15 | Przedstawienie sprawozdania i ocena u prowadzącego |

**Termin uzupełniający:** osoby odrabiające zajęcia L1–L4 pracują równolegle na swoich materiałach (Wokwi, Colab, The Construct działają w tej samej sali).

## Przebieg

Instrukcja krok po kroku jest w notatniku [`L5_lerobot.ipynb`](L5_lerobot.ipynb):

1. **Zbiór**: 206 epizodów, 25 650 klatek, 10 fps, obraz 96×96, stan i akcja 2D. Kadry z epizodu, trajektoria stanu i akcji.
2. **Polityka gotowa**: migracja `lerobot/diffusion_pusht` do formatu LeRobot 0.6 skryptem [`migruj_polityke.py`](migruj_polityke.py), `lerobot-eval` na 20 epizodach, filmy.
3. **Trening**: `lerobot-train --policy.type=diffusion` na 4000 kroków. W trakcie treningu analizujesz filmy z części 2.
4. **Porównanie i eksperyment**: tabela skuteczności; jeden eksperyment do wyboru (ACT zamiast Diffusion, mniej demonstracji, dłuższy trening).

## Sprawozdanie (na zajęciach)

Sprawozdanie piszesz na bieżąco w trakcie zajęć, w katalogu `L5/` w swoim repozytorium (albo w formie wskazanej przez prowadzącego). Po każdej części dopisz wyniki i wnioski. Przed końcem zajęć przedstawiasz prowadzącemu sprawozdanie i notatnik z wynikami; prowadzący ocenia je na miejscu.

Sprawozdanie zawiera:

- wykonany notatnik z wynikami,
- odpowiedzi na pytania z części 1,
- tabelę porównawczą (polityka gotowa, własna, eksperyment) i opis typowych porażek (zrzuty klatek z filmów),
- wnioski (5–8 zdań) z odniesieniem do W13: kumulacja błędów, wielomodalność, ilość danych, miejsce polityki w architekturze systemu.

### Kryteria oceny

| Sekcja | Punkty |
|---|---|
| Część 1: analiza zbioru, odpowiedzi | 20 |
| Część 2: ewaluacja polityki gotowej, analiza porażek | 25 |
| Część 3–4: trening, porównanie, eksperyment | 35 |
| Wnioski | 20 |
| **Razem** | **100** |

**Warunek zaliczenia:** trzeba zaliczyć wszystkie sekcje z tabeli. Jeśli odbyła się kartkówka, prowadzący podaje na początku zajęć, jak uwzględnia ją w ocenie.

## Źródła

- R. Cadène i in., *LeRobot*, <https://github.com/huggingface/lerobot>; dokumentacja: <https://huggingface.co/docs/lerobot> (*Installation*, *Cheat Sheet*, *LeRobotDataset*).
- C. Chi i in., *Diffusion Policy: Visuomotor Policy Learning via Action Diffusion*, RSS 2023 (zadanie PushT).
- T. Z. Zhao i in., *Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware* (ACT), RSS 2023.
- Hugging Face, *gym-pusht*, <https://github.com/huggingface/gym-pusht>.
