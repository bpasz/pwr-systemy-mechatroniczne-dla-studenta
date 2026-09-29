// Ćwiczenie 3: silnik krokowy (A4988) sterowany z przerwania timera TIM14.
// Potencjometr na A0 (ADC, 12 bitów) zadaje prędkość 50...800 kroków/s.
// Przełącznik na D8 wybiera kierunek.

#include <Arduino.h>

const uint8_t PIN_STEP = D5, PIN_DIR = D6, PIN_EN = D7, PIN_KIERUNEK = D8;

HardwareTimer *timer = nullptr;
volatile int32_t kroki = 0;
volatile bool kierunekWGore = true;

void przerwanie() {                      // każde przerwanie = pół okresu sygnału STEP
  static bool wysoki = false;
  wysoki = !wysoki;
  digitalWrite(PIN_STEP, wysoki);
  if (wysoki) kroki += kierunekWGore ? 1 : -1;
}

void setup() {
  Serial.begin(115200);
  pinMode(PIN_STEP, OUTPUT);
  pinMode(PIN_DIR, OUTPUT);
  pinMode(PIN_EN, OUTPUT);
  pinMode(PIN_KIERUNEK, INPUT_PULLUP);
  digitalWrite(PIN_EN, LOW);             // A4988 włączony (EN aktywne stanem niskim)
  analogReadResolution(12);

  timer = new HardwareTimer(TIM14);
  timer->setOverflow(400, HERTZ_FORMAT); // 400 przerwań/s = 200 kroków/s
  timer->attachInterrupt(przerwanie);
  timer->resume();
}

void loop() {
  const uint32_t kod = analogRead(A0);                     // 0 ... 4095
  const uint32_t krokowNaS = 50 + kod * (800 - 50) / 4095;  // odwzorowanie liniowe
  timer->setOverflow(2 * krokowNaS, HERTZ_FORMAT);          // 2 przerwania na krok

  kierunekWGore = digitalRead(PIN_KIERUNEK) == HIGH;
  digitalWrite(PIN_DIR, kierunekWGore ? HIGH : LOW);

  static uint32_t ostatni = 0;
  if (millis() - ostatni >= 500) {
    ostatni = millis();
    noInterrupts();
    const int32_t k = kroki;
    interrupts();
    Serial.print("ADC=");
    Serial.print(kod);
    Serial.print("  predkosc=");
    Serial.print(krokowNaS);
    Serial.print(" krokow/s  pozycja=");
    Serial.println(k);
  }
}
