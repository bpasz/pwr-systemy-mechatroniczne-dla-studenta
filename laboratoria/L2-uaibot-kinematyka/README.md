# L2. Kinematyka i sterowanie kinematyczne manipulatora w UAIbot

> **Systemy mechatroniczne · Laboratorium 2 (3 h akad.)**
> Wykłady powiązane: [W04](../../wyklady/W04-opis-przestrzenny.md), [W05](../../wyklady/W05-kinematyka.md), [W06](../../wyklady/W06-sterowanie-kinematyczne.md).
> Sylabus: La1 (modelowanie i symulacje interdyscyplinarne systemów mechatronicznych).

[![Otwórz w Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/bpasz/pwr-systemy-mechatroniczne/blob/main/laboratoria/L2-uaibot-kinematyka/L2_uaibot.ipynb)

## Cel

Po zajęciach potrafisz:

- złożyć transformacje jednorodne i zinterpretować wynik (układ vs operator),
- policzyć kinematykę prostą robota 6-osiowego z parametrów DH i zweryfikować ją,
- policzyć Jakobian geometryczny, rozpoznać konfigurację osobliwą,
- zaimplementować sterowanie kinematyczne pozą i śledzenie trajektorii z członem feedforward,
- ocenić wpływ parametrów $K$ i $\epsilon$ na zbieżność i prędkości przegubów.

## Środowisko

- **Google Colab** (zalecane): kliknij przycisk „Open in Colab” powyżej i zaloguj się kontem Google. Pierwsza komórka instaluje `uaibot` (ok. 30 s).
- Alternatywnie dowolny Jupyter z Pythonem ≥ 3.10: `pip install uaibot`.
- Symulacje 3D UAIbot wyświetlają się w przeglądarce (Three.js). Obracaj widok myszą, animację odtwarzasz paskiem na dole okna.

## Zasady zajęć

- **Pracujesz indywidualnie.** Zajęcia zaczynają się od zadania wprowadzającego (część prowadzona), potem każdy realizuje własny projekt.
- **Sprawozdanie piszesz w trakcie zajęć** i dokumentujesz w nim postępy pracy na bieżąco. Prowadzący ocenia je na zajęciach, nie ma terminu oddania po zajęciach.
- Na początku zajęć prowadzący **może** przeprowadzić krótką kartkówkę (ok. 10 min) z wykładów W04–W06.
- Aby zaliczyć laboratorium, trzeba zaliczyć **wszystkie sekcje** z tabeli kryteriów oceny.

## Przed zajęciami

1. Powtórz slajdy W04–W06, zwłaszcza: składanie MTJ, parametry DH, Jakobian, prawo sterowania kinematycznego.
2. Otwórz notatnik w Colab i uruchom dwie pierwsze komórki (instalacja i import), żeby sprawdzić, że działa.
3. Opcjonalnie: przejrzyj oryginalne slajdy UAIbot (EN): <https://uaibot.github.io/class_presentations/>.

## Plan zajęć (135 min)

| Czas | Część |
|---|---|
| 0:00–0:05 | Organizacja, uruchomienie notatnika |
| 0:05–0:25 | A1: MTJ, składanie, oś i kąt obrotu |
| 0:25–0:45 | A2: kinematyka prosta KUKA KR5 z DH, weryfikacja z `fkm()` |
| 0:45–1:05 | A3: Jakobian, różnice skończone, osobliwości, tłumiona pseudoodwrotność |
| 1:05–2:05 | B: projekt indywidualny: sterowanie pozą (B1), funkcja nasycenia (B2), śledzenie okręgu (B3) |
| 2:05–2:15 | Przedstawienie sprawozdania i ocena u prowadzącego |

## Przebieg

Cała instrukcja krok po kroku jest w notatniku [`L2_uaibot.ipynb`](L2_uaibot.ipynb). W skrócie:

### Część A: zadanie wprowadzające (prowadzone)

- **A1.** Złożenie $R_x(\pi/4)D_y(-0{,}25)R_z(\pi/2)D_x(1)$ z W04, sprawdzenie warunków macierzy obrotu, wizualizacja układów. Nieprzemienność obrotów: oś i kąt dla $R_xR_y$ i $R_yR_x$.
- **A2.** Własna funkcja `kinematyka_prosta(robot, q)` z łańcucha $R_z(\theta_i)D_z(d_i)R_x(\alpha_i)D_x(a_i)$. Porównanie z `robot.fkm()` (oczekiwany błąd rzędu $10^{-7}$).
- **A3.** Jakobian `robot.jac_geo()` kontra różnice centralne. Wartości szczególne w konfiguracji początkowej (osobliwej!) i w konfiguracji ogólnej. Tłumiona pseudoodwrotność `Utils.dp_inv`.

### Część B: projekt indywidualny

- **B1.** Sterowanie pozą efektora (kod z W06). Tabela: czas zbieżności i $\max|u|$ dla $K \in \{0{,}5;\ 2;\ 8\}$ i $\epsilon \in \{10^{-4};\ 10^{-3};\ 10^{-1}\}$.
- **B2.** Funkcja $F(r)$ z nasyceniem zamiast $F(r) = Kr$: porównanie przebiegów.
- **B3.** Śledzenie okręgu z członem feedforward $\partial r / \partial t$. Porównanie błędu z feedforward i bez.

## Sprawozdanie (na zajęciach)

Sprawozdanie piszesz na bieżąco w trakcie zajęć, w katalogu `L2/` w swoim repozytorium (albo w formie wskazanej przez prowadzącego). Po każdej części dopisz wyniki i wnioski. Przed końcem zajęć przedstawiasz prowadzącemu sprawozdanie i notatnik z wynikami; prowadzący ocenia je na miejscu.

Sprawozdanie zawiera:

- wykonany notatnik (File → Download → .ipynb) z wynikami wszystkich komórek,
- `README.md` z odpowiedziami na pytania A1–A3, tabelą B1 i wnioskami, wykresami B2 i B3 z komentarzem.

### Kryteria oceny

| Sekcja | Punkty |
|---|---|
| A1–A3: poprawne wyniki i odpowiedzi | 30 |
| B1: tabela i wnioski (odniesienie do reguły $5/K$ i roli $\epsilon$) | 25 |
| B2: implementacja i porównanie | 15 |
| B3: śledzenie okręgu, porównanie z/bez feedforward | 20 |
| Jakość wykresów i sprawozdania | 10 |
| **Razem** | **100** |

**Warunek zaliczenia:** trzeba zaliczyć wszystkie sekcje z tabeli. Jeśli odbyła się kartkówka, prowadzący podaje na początku zajęć, jak uwzględnia ją w ocenie.

## Źródła

- V. M. Gonçalves i in., **UAIbot: Robotic Manipulators**, Class 2–5: <https://uaibot.github.io/class_presentations/> (przykłady sterowania kinematycznego w części B pochodzą z Class 5, tłumaczenie i adaptacja).
- UAIbot, dokumentacja i repozytorium Pythona: <https://uaibot.github.io/>, <https://github.com/UAIbot/UAIbotPy>.
- B. Siciliano i in., *Robotics: Modelling, Planning and Control*, Springer, 2009, rozdz. 2–3.
