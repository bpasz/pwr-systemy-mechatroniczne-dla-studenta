// Ćwiczenie 1: ta sama dioda LD4 (PA5 = D13) sterowana na trzech poziomach abstrakcji.
// Zmieniaj WARIANT (1, 2, 3) i obserwuj, że efekt jest identyczny.

#include <Arduino.h>

#define WARIANT 1   // 1 = rejestry (CMSIS), 2 = HAL, 3 = Arduino

void setup() {
  Serial.begin(115200);
  Serial.print("Zegar rdzenia [Hz]: ");
  Serial.println(SystemCoreClock);   // spodziewane 48000000

#if WARIANT == 1
  RCC->IOPENR |= RCC_IOPENR_GPIOAEN;                        // zegar dla portu A
  GPIOA->MODER = (GPIOA->MODER & ~GPIO_MODER_MODE5_Msk)     // wyczyść 2 bity trybu PA5
               | (1U << GPIO_MODER_MODE5_Pos);              // 01 = wyjście
#else
  pinMode(LED_BUILTIN, OUTPUT);                             // dla HAL i Arduino
#endif
}

void loop() {
#if WARIANT == 1
  GPIOA->BSRR = GPIO_BSRR_BS5;       // ustaw PA5
  delay(250);
  GPIOA->BSRR = GPIO_BSRR_BR5;       // wyzeruj PA5
  delay(250);
#elif WARIANT == 2
  HAL_GPIO_TogglePin(GPIOA, GPIO_PIN_5);
  delay(250);
#else
  digitalWrite(LED_BUILTIN, !digitalRead(LED_BUILTIN));
  delay(250);
#endif
}
