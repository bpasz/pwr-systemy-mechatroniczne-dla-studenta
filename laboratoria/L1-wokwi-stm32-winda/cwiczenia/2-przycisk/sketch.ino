// Ćwiczenie 2: przycisk, drgania styków i przerwanie EXTI.
// Przycisk na D2 (do GND), wewnętrzny pull-up. Dioda na D10.
// Program liczy zbocza opadające na dwa sposoby:
//   - w przerwaniu (surowe zbocza, razem z drganiami),
//   - w pętli loop() z programowym tłumieniem drgań (20 ms).

#include <Arduino.h>

const uint8_t PIN_PRZYCISK = D2;
const uint8_t PIN_LED = D10;
const uint32_t CZAS_DEBOUNCE_MS = 20;

volatile uint32_t zboczaSurowe = 0;   // modyfikowane w ISR -> volatile

void naZbocze() {                     // procedura obsługi przerwania (EXTI)
  zboczaSurowe++;
}

void setup() {
  Serial.begin(115200);
  pinMode(PIN_PRZYCISK, INPUT_PULLUP);
  pinMode(PIN_LED, OUTPUT);
  attachInterrupt(digitalPinToInterrupt(PIN_PRZYCISK), naZbocze, FALLING);
  Serial.println("Wcisnij przycisk kilka razy.");
}

void loop() {
  static bool stabilny = HIGH, ostatniOdczyt = HIGH;
  static uint32_t zmianaMs = 0, wcisniecia = 0;

  const bool odczyt = digitalRead(PIN_PRZYCISK);
  if (odczyt != ostatniOdczyt) {       // zmiana odczytu: zacznij odliczać czas
    ostatniOdczyt = odczyt;
    zmianaMs = millis();
  }
  if (millis() - zmianaMs >= CZAS_DEBOUNCE_MS && stabilny != odczyt) {
    stabilny = odczyt;                 // stan stabilny przez 20 ms: akceptujemy
    if (stabilny == LOW) {
      wcisniecia++;
      digitalWrite(PIN_LED, !digitalRead(PIN_LED));

      noInterrupts();                  // spójna kopia zmiennej z ISR
      const uint32_t surowe = zboczaSurowe;
      interrupts();

      Serial.print("Wcisniecia (z debounce): ");
      Serial.print(wcisniecia);
      Serial.print("   zbocza w przerwaniu: ");
      Serial.println(surowe);
    }
  }
}
