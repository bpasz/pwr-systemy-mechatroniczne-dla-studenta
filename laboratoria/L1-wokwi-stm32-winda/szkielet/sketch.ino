// =============================================================================
// L1: Winda na STM32 (Nucleo-C031C6) w symulatorze Wokwi
// SZKIELET DLA STUDENTÓW: uzupełnij fragmenty oznaczone TODO(1)...TODO(6).
// Program kompiluje się od początku, ale winda nie działa, dopóki nie uzupełnisz TODO.
//
// Sprzęt (patrz diagram.json):
//   D2, D3, D4  przyciski wezwań: piętro 0, 1, 2 (do GND, wewnętrzny pull-up)
//   D5, D6, D7  sterownik A4988: STEP, DIR, EN (EN aktywne stanem niskim)
//   D8          przełącznik STOP (stan niski = zatrzymanie awaryjne)
//   D9  (PC7)   serwo drzwi, PWM 50 Hz z TIM3_CH2
//   D10-D12     diody: winda na piętrze 0, 1, 2
//   D13 (PA5)   dioda LD4 na płytce: miga podczas jazdy / awarii
//   A1  (PA1)   dzwonek (brzęczyk piezo): gong po przyjeździe, alarm w stanie AWARIA
//   Serial      logi przez wirtualny port ST-LINK (USART2: PA2/PA3)
// =============================================================================

#include <Arduino.h>

// ---------------------------------------------------------------- konfiguracja
const uint8_t LICZBA_PIETER = 3;
const uint8_t PIN_PRZYCISK[LICZBA_PIETER] = {D2, D3, D4};
const uint8_t PIN_LED_PIETRO[LICZBA_PIETER] = {D10, D11, D12};
const uint8_t PIN_STEP = D5;
const uint8_t PIN_DIR = D6;
const uint8_t PIN_EN = D7;
const uint8_t PIN_STOP = D8;
const uint8_t PIN_SERWO = D9;
const uint8_t PIN_DZWONEK = A1;

const int32_t KROKI_NA_PIETRO = 400;     // 2 obroty silnika (200 kroków/obr.)
const uint32_t CZESTOTLIWOSC_TIMERA = 800; // [Hz] -> 400 kroków/s (1 krok = 2 przerwania)
const uint32_t CZAS_DRZWI_MS = 3000;
const uint32_t CZAS_DEBOUNCE_MS = 20;
const uint32_t SERWO_ZAMKNIETE_US = 1000; // szerokość impulsu serwa [us]
const uint32_t SERWO_OTWARTE_US = 2000;
const uint32_t CZAS_GONGU_MS = 300;      // sygnał po przyjeździe na piętro
const uint32_t OKRES_ALARMU_MS = 250;    // alarm w stanie AWARIA: 250 ms dźwięk, 250 ms cisza

// UWAGA: typy (enum, struct) definiujemy przed pierwszą funkcją. Środowisko
// Arduino wstawia automatycznie prototypy funkcji właśnie w tym miejscu.
// ------------------------------------------------------------- automat stanów
enum Stan { POSTOJ, JAZDA, DRZWI_OTWARTE, AWARIA };
const char *NAZWA_STANU[] = {"POSTOJ", "JAZDA", "DRZWI_OTWARTE", "AWARIA"};

Stan stan = POSTOJ;
uint32_t wejscieDoStanuMs = 0;
int8_t kierunek = 0;                 // +1 w górę, -1 w dół, 0 brak
uint8_t pietroCel = 0;
bool wezwanie[LICZBA_PIETER] = {false, false, false};

// ------------------------------------------------------- przyciski z debounce
struct Przycisk {
  uint8_t pin;
  bool stabilny;       // ostatni stabilny stan (true = wciśnięty)
  bool surowy;         // ostatni odczyt
  uint32_t zmianaMs;   // czas ostatniej zmiany odczytu

  // Zwraca true dokładnie raz, w chwili stabilnego wciśnięcia.
  bool wcisniety(uint32_t teraz) {
    const bool odczyt = digitalRead(pin) == LOW; // pull-up: wciśnięty = LOW
    // TODO(1): tłumienie drgań styków (patrz ćwiczenie 2).
    //  - gdy odczyt różni się od `surowy`: zapamiętaj go w `surowy` i czas w `zmianaMs`,
    //  - gdy od zmiany minęło >= CZAS_DEBOUNCE_MS i `stabilny` != `surowy`:
    //    przepisz `surowy` do `stabilny` i zwróć true, jeśli nowy stan to "wciśnięty".
    (void)odczyt;
    (void)teraz;
    return false;
  }
};
Przycisk przyciski[LICZBA_PIETER];

// -------------------------------------------------- stan współdzielony z ISR
// Zmienne modyfikowane w przerwaniu muszą być `volatile`.
volatile int32_t pozycja = 0;     // aktualna pozycja kabiny [kroki]
volatile int32_t pozycjaCel = 0;  // pozycja docelowa [kroki]
volatile bool silnikWlaczony = false;
volatile bool dzwonekWlaczony = false; // ISR generuje ton, gdy true

bool gongAktywny = false;           // gong po przyjeździe trwa
uint32_t gongStartMs = 0;

HardwareTimer *timerKrokow = nullptr; // TIM14: generowanie impulsów STEP
HardwareTimer *timerSerwa = nullptr;  // TIM3: PWM 50 Hz dla serwa
uint32_t kanalSerwa = 0;

// Przerwanie od przepełnienia TIM14. Krótkie i bez Serial.print()!
void przerwanieKrokow() {
  // Dzwonek: zmiana stanu pinu w każdym przerwaniu daje falę prostokątną
  // 800 Hz / 2 = 400 Hz. Brzęczyk piezo zamienia ją na dźwięk.
  static bool dzwonekWysoki = false;
  if (dzwonekWlaczony || dzwonekWysoki) {
    dzwonekWysoki = dzwonekWlaczony && !dzwonekWysoki;
    digitalWrite(PIN_DZWONEK, dzwonekWysoki ? HIGH : LOW);
  }

  static bool stepWysoki = false;
  // TODO(2): generator kroków (patrz ćwiczenie 3 i wykład W03).
  //  - jeśli STEP jest w stanie wysokim: ustaw LOW i zakończ,
  //  - jeśli silnik wyłączony albo pozycja == pozycjaCel: nic nie rób,
  //  - w przeciwnym razie: ustaw DIR (w górę, gdy pozycjaCel > pozycja),
  //    ustaw STEP na HIGH i zwiększ lub zmniejsz `pozycja` o 1.
  (void)stepWysoki;
}

// ------------------------------------------------------------ elementy wykonawcze
void ustawDrzwi(bool otwarte) {
  timerSerwa->setCaptureCompare(kanalSerwa, otwarte ? SERWO_OTWARTE_US : SERWO_ZAMKNIETE_US,
                                MICROSEC_COMPARE_FORMAT);
}

void ustawSilnik(bool wlaczony) {
  silnikWlaczony = wlaczony;
  digitalWrite(PIN_EN, wlaczony ? LOW : HIGH);
}

int32_t odczytajPozycje() {
  noInterrupts();                   // spójny odczyt zmiennej współdzielonej z ISR
  const int32_t p = pozycja;
  interrupts();
  return p;
}

// Piętro, na którym stoi kabina (albo -1, gdy jest między piętrami).
int8_t pietroKabiny() {
  const int32_t p = odczytajPozycje();
  return (p % KROKI_NA_PIETRO == 0) ? p / KROKI_NA_PIETRO : -1;
}

void pokazPietro() {
  const int8_t pietro = pietroKabiny();
  for (uint8_t i = 0; i < LICZBA_PIETER; i++) {
    digitalWrite(PIN_LED_PIETRO[i], pietro == i ? HIGH : LOW);
  }
}

// --------------------------------------------------- algorytm wyboru celu
// Wersja naiwna: jedź do najniższego piętra z wezwaniem.
// TODO(4): zaimplementuj algorytm "zbiorczy" jak w prawdziwej windzie:
//   jedź dalej w bieżącym kierunku (`kierunek`), jeśli są tam wezwania,
//   a dopiero potem zawróć. Zapisz kierunek jazdy w zmiennej `kierunek`.
//   Sprawdź na scenariuszu: kabina na 0, wezwania kolejno 2 i 1 w trakcie jazdy.
int8_t wybierzCel(uint8_t p) {
  for (uint8_t i = 0; i < LICZBA_PIETER; i++) {
    if (wezwanie[i] && i != p) return (int8_t)i;
  }
  return -1;   // brak wezwań
}

// ------------------------------------------------------------------ przejścia
void zmienStan(Stan nowy) {
  Serial.print('[');
  Serial.print(millis());
  Serial.print(" ms] ");
  Serial.print(NAZWA_STANU[stan]);
  Serial.print(" -> ");
  Serial.print(NAZWA_STANU[nowy]);
  Serial.print("  (pietro ");
  Serial.print(pietroKabiny());
  Serial.println(')');
  stan = nowy;
  wejscieDoStanuMs = millis();
}

void rozpocznijJazde(uint8_t cel) {
  pietroCel = cel;
  noInterrupts();
  pozycjaCel = (int32_t)cel * KROKI_NA_PIETRO;
  interrupts();
  ustawSilnik(true);
  zmienStan(JAZDA);
}

void otworzDrzwi() {
  ustawSilnik(false);
  ustawDrzwi(true);
  // TODO(6a): uruchom gong: gongAktywny = true, gongStartMs = bieżący czas.
  zmienStan(DRZWI_OTWARTE);
}

void krokAutomatu(uint32_t teraz) {
  const bool stop = digitalRead(PIN_STOP) == LOW;

  if (stop && stan != AWARIA) {
    ustawSilnik(false);
    zmienStan(AWARIA);
    return;
  }

  switch (stan) {
    case POSTOJ: {
      const int8_t pk = pietroKabiny();
      if (pk < 0) break;                 // nie powinno się zdarzyć: postój tylko na piętrze
      const uint8_t p = (uint8_t)pk;
      if (wezwanie[p]) {                 // wezwanie z bieżącego piętra
        wezwanie[p] = false;
        otworzDrzwi();
        break;
      }
      const int8_t cel = wybierzCel(p);
      if (cel >= 0) {
        kierunek = cel > p ? +1 : -1;
        rozpocznijJazde((uint8_t)cel);
      }
      break;
    }

    case JAZDA: {
      // TODO(5) (rozszerzenie): zatrzymanie "po drodze". Jeśli kabina właśnie
      //   mija piętro z wezwaniem, zmień `pietroCel` i `pozycjaCel` na to piętro.
      //   Uwaga na współbieżność z ISR (noInterrupts / interrupts).

      // TODO(3a): gdy pozycja kabiny == pietroCel * KROKI_NA_PIETRO:
      //   skasuj wezwanie[pietroCel] i wywołaj otworzDrzwi().
      break;
    }

    case DRZWI_OTWARTE:
      // TODO(3b): po CZAS_DRZWI_MS od wejścia do stanu (`wejscieDoStanuMs`)
      //   zamknij drzwi (ustawDrzwi(false)) i przejdź do stanu POSTOJ.
      //   Bez delay()! Ponowne wezwanie z tego piętra przedłuża otwarcie.
      (void)teraz;   // usuń tę linię po uzupełnieniu TODO(3b)
      break;

    case AWARIA:
      if (!stop) {
        // Kabina mogła stanąć między piętrami: dojedź do najbliższego w dół.
        const int32_t p = odczytajPozycje();
        const uint8_t pietro = p / KROKI_NA_PIETRO;
        if (p % KROKI_NA_PIETRO != 0) {
          kierunek = -1;
          rozpocznijJazde(pietro);
        } else {
          zmienStan(POSTOJ);
        }
      }
      break;
  }
}

// --------------------------------------------------------------------- dzwonek
void obsluzDzwonek(uint32_t teraz) {
  // TODO(6b): sterowanie dzwonkiem (bez delay()!). Ustaw `dzwonekWlaczony`:
  //  - true przez CZAS_GONGU_MS od `gongStartMs`, gdy `gongAktywny` (potem wyzeruj `gongAktywny`),
  //  - w stanie AWARIA: sygnał przerywany, OKRES_ALARMU_MS dźwięk i OKRES_ALARMU_MS cisza,
  //  - w pozostałych przypadkach false.
  //  Ton 400 Hz generuje już przerwanie timera (przerwanieKrokow).
  (void)teraz;
}

// ----------------------------------------------------------------------- setup
void setup() {
  Serial.begin(115200);

  for (uint8_t i = 0; i < LICZBA_PIETER; i++) {
    pinMode(PIN_PRZYCISK[i], INPUT_PULLUP);
    pinMode(PIN_LED_PIETRO[i], OUTPUT);
    przyciski[i] = {PIN_PRZYCISK[i], false, false, 0};
  }
  pinMode(PIN_STOP, INPUT_PULLUP);
  pinMode(PIN_STEP, OUTPUT);
  pinMode(PIN_DIR, OUTPUT);
  pinMode(PIN_EN, OUTPUT);
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(PIN_DZWONEK, OUTPUT);
  ustawSilnik(false);

  // Serwo: PWM 50 Hz na TIM3, kanał i timer odczytane z mapy pinów wariantu.
  const PinName pinSerwa = digitalPinToPinName(PIN_SERWO);
  TIM_TypeDef *instancja = (TIM_TypeDef *)pinmap_peripheral(pinSerwa, PinMap_PWM);
  kanalSerwa = STM_PIN_CHANNEL(pinmap_function(pinSerwa, PinMap_PWM));
  timerSerwa = new HardwareTimer(instancja);
  timerSerwa->setPWM(kanalSerwa, pinSerwa, 50, 5); // 50 Hz, wypełnienie startowe 5%
  ustawDrzwi(false);

  // Generator kroków: przerwanie od przepełnienia TIM14.
  timerKrokow = new HardwareTimer(TIM14);
  timerKrokow->setOverflow(CZESTOTLIWOSC_TIMERA, HERTZ_FORMAT);
  timerKrokow->attachInterrupt(przerwanieKrokow);
  timerKrokow->resume();

  Serial.println("Winda gotowa. Kabina na pietrze 0.");
}

// ------------------------------------------------------------------------ loop
void loop() {
  const uint32_t teraz = millis();

  for (uint8_t i = 0; i < LICZBA_PIETER; i++) {
    if (przyciski[i].wcisniety(teraz)) {
      wezwanie[i] = true;
      Serial.print("Wezwanie na pietro ");
      Serial.println(i);
    }
  }

  krokAutomatu(teraz);
  pokazPietro();
  obsluzDzwonek(teraz);

  // LD4: miga w czasie jazdy (2 Hz) i awarii (8 Hz), zgaszona w pozostałych stanach.
  const bool miga = stan == JAZDA || stan == AWARIA;
  const uint32_t okres = stan == AWARIA ? 125 : 500;
  digitalWrite(LED_BUILTIN, miga && ((teraz / okres) % 2) ? HIGH : LOW);
}
