---
title: "W09. Moduły i układy komunikacyjne"
subtitle: "UART, I²C, SPI, CAN, sieci przemysłowe i komunikacja robot–komputer"
author: "Systemy mechatroniczne · PWr W12N"
---

## Plan wykładu

1. Pojęcia podstawowe: szeregowo/równolegle, synchronicznie/asynchronicznie, topologie
2. UART i RS-485
3. I²C i SPI: magistrale na płytce
4. CAN i CANopen: magistrala pojazdów i maszyn
5. Ethernet przemysłowy: EtherCAT, PROFINET, Modbus TCP
6. Od mikrokontrolera do ROS 2: micro-ROS, `ros2_control`
7. Jak wybrać interfejs


# Podstawy


## Podstawowe pojęcia

| Pojęcie | Znaczenie |
|---|---|
| szeregowa / równoległa | bity jeden po drugim / wiele linii naraz. Dziś prawie wszystko jest szeregowe |
| synchroniczna | osobna linia zegara (SPI, I²C) |
| asynchroniczna | bez zegara, obie strony znają prędkość (UART, CAN) |
| punkt–punkt / magistrala | dwa urządzenia / wiele urządzeń na wspólnych liniach |
| niesymetryczna / różnicowa | napięcie względem masy / różnica napięć pary przewodów: odporność na zakłócenia i długie kable |
| przepływność | bit/s na linii; nie mylić z przepustowością danych użytkowych |
| determinizm | gwarantowany maksymalny czas dostarczenia (kluczowe w sterowaniu) |


# Na płytce


## UART

:::: columns
::: {.column width="55%"}
- Dwie linie: **TX → RX**, **RX ← TX**, wspólna masa.
- Ramka **8N1**: bit startu, 8 bitów danych (od najmłodszego), brak parzystości, bit stopu.
- Prędkość (*baud rate*) ustalona z góry: 9600, 115200, …
- Przy 115200 bit/s i 8N1 (10 bitów na bajt): **11 520 B/s**.
- Na Nucleo: `Serial` = USART2 (PA2/PA3) przez ST-LINK = port COM w komputerze. W Wokwi: monitor portu szeregowego.
- **RS-485**: UART + różnicowa para, do 1200 m, magistrala do 32 urządzeń. Na nim protokół **Modbus RTU**.
:::
::: {.column width="45%"}
```cpp
void setup() {
  Serial.begin(115200);
}

void loop() {
  if (Serial.available()) {
    char c = Serial.read();
    if (c >= '0' && c <= '2') {
      wezwanie[c - '0'] = true;  // wezwanie
    }                             // windy z PC
  }
}
```
:::
::::


## I²C

:::: columns
::: {.column width="55%"}
- Dwie linie: **SDA** (dane), **SCL** (zegar), wyjścia **open-drain** + rezystory podciągające (2,2–10 kΩ).
- Magistrala: jeden master (MCU), wiele urządzeń, każde ma **7-bitowy adres**.
- Prędkości: 100 kHz, 400 kHz, 1 MHz.
- Typowe urządzenia: IMU (MPU-6050, 0x68), wyświetlacz LCD z konwerterem (0x27), czujniki temperatury, pamięci EEPROM.
- Wada: krótkie połączenia (w obrębie płytki), wrażliwe na pojemność linii.
:::
::: {.column width="45%"}
```cpp
#include <Wire.h>

Wire.begin();
Wire.beginTransmission(0x68);  // adres MPU-6050
Wire.write(0x3B);              // rejestr ACCEL_XOUT_H
Wire.endTransmission(false);
Wire.requestFrom(0x68, 6);     // 6 bajtów: ax, ay, az
int16_t ax = (Wire.read() << 8) | Wire.read();
```
:::
::::

::: zrodlo
W Wokwi dla STM32C031 I²C działa w trybie master (Wokwi Docs, board-st-nucleo-c031c6).
:::


## SPI

:::: columns
::: {.column width="55%"}
- Cztery linie: **SCK** (zegar), **MOSI**, **MISO**, **CS** (wybór układu, osobny dla każdego urządzenia).
- Pełny dupleks, **dziesiątki MHz**: wyświetlacze TFT, karty SD, przetworniki ADC, enkodery absolutne, sterowniki silników (TMC2130).
- Brak adresów: urządzenie wybiera linia CS. Brak potwierdzeń.
- Cztery tryby (CPOL, CPHA): polaryzacja i faza zegara. Musi się zgadzać z notą katalogową urządzenia.
:::
::: {.column width="45%"}
| | I²C | SPI |
|---|---|---|
| linie | 2 | 3 + 1 na urządzenie |
| prędkość | ≤ 1 MHz | ≥ 10 MHz |
| adresowanie | adres 7-bit | linia CS |
| potwierdzenie | ACK | brak |
| zastosowanie | wolne czujniki | szybkie dane |
:::
::::


# Magistrale polowe


## CAN

:::: columns
::: {.column width="55%"}
- Bosch, 1986: samochody, maszyny, roboty mobilne, napędy.
- Para różnicowa **CAN_H / CAN_L**, terminatory 120 Ω, do 1 Mbit/s (CAN FD: dane do 5–8 Mbit/s).
- Ramka ma **identyfikator** wiadomości, nie adres odbiorcy.
- **Arbitraż bez strat**: przy kolizji wygrywa niższe ID (wyższy priorytet).
- Wbudowane CRC, potwierdzenia, odłączanie wadliwego węzła.
- **CANopen**: profile urządzeń, np. CiA 402 (napędy).
:::
::: {.column width="45%"}
| Pole ramki | Bity |
|---|---|
| start (SOF) | 1 |
| identyfikator | 11 / 29 |
| sterowanie (DLC) | 6 |
| dane | 0–64 (CAN FD: do 512) |
| CRC | 15 + 1 |
| ACK | 2 |
| koniec (EOF) | 7 |
:::
::::


## Ethernet przemysłowy

| Protokół | Cechy | Czas cyklu | Zastosowanie |
|---|---|---|---|
| **EtherCAT** | ramka przechodzi przez wszystkie węzły „w locie”, zegary rozproszone | ≤ 100 µs, jitter < 1 µs | napędy, roboty, CNC |
| PROFINET IRT | Siemens, zarezerwowane okna czasowe | ≈ 250 µs | automatyka fabryczna |
| EtherNet/IP | Rockwell, na TCP/UDP | ms | PLC, I/O |
| Modbus TCP | prosty, rejestry, bez gwarancji czasu | 10–100 ms | monitoring, proste urządzenia |
| **TSN** | rozszerzenia IEEE 802.1 dla Ethernetu (szeregowanie w czasie) | µs–ms | przyszły standard konwergencji |

- Robot przemysłowy wewnątrz: zwykle EtherCAT między sterownikiem a serwonapędami.
- Robot ↔ komputer (np. UR z ROS 2): Ethernet/TCP z pętlą 500 Hz, sterownik `ur_robot_driver`.


# Robot i komputer


## Od mikrokontrolera do ROS 2

:::: columns
::: {.column width="50%"}
::: maly
**Wariant 1: własny protokół szeregowy**

- MCU wysyła np. `P:400;S:1\n` przez UART/USB.
- Węzeł ROS 2 (Python + `pyserial`) tłumaczy na tematy.
- Proste, ale trzeba samemu zadbać o format, błędy i synchronizację.

**Wariant 2: micro-ROS**

- Klient micro-ROS na MCU (FreeRTOS, Zephyr, Arduino).
- Agent micro-ROS na komputerze.
- MCU jest „zwykłym” węzłem ROS 2: publikuje tematy, udostępnia usługi.
:::
:::
::: {.column width="50%"}
::: maly
**Wariant 3: `ros2_control` + interfejs sprzętowy**

- Wtyczka `hardware_interface` (C++) z metodami `read()` i `write()`.
- Wywoływana w stałej pętli (np. 100 Hz–1 kHz) przez `controller_manager`.
- Kontrolery (pozycja, trajektoria) są wymienne, a sprzęt i symulator (Gazebo) podłączają się tak samo.
- To architektura z L4 (W11).
:::
:::
::::


## Jak wybrać interfejs

| Wymaganie | Wybór |
|---|---|
| czujnik na tej samej płytce, wolny | I²C |
| szybki przetwornik, wyświetlacz, enkoder | SPI |
| debug, komunikacja z PC, moduł GPS/BT | UART (USB-CDC) |
| kilka sterowników w pojeździe lub maszynie, kable metrowe, zakłócenia | CAN / CAN FD |
| wieloosiowy napęd, synchronizacja µs | EtherCAT |
| moduły ROS 2 na różnych komputerach | Ethernet/Wi-Fi + DDS |
| MCU jako węzeł ROS 2 | micro-ROS (UART, USB, UDP) |


## Podsumowanie

- Wybór magistrali to kompromis: odległość, prędkość, liczba urządzeń, determinizm, koszt.
- Na płytce: I²C i SPI. Między modułami: UART, CAN. W maszynie: Ethernet przemysłowy.
- W ROS 2 warstwę transportową zapewnia DDS. Sprzęt podłączamy przez micro-ROS lub `ros2_control`.


## Źródła i dalsza lektura

- NXP, *UM10204: I²C-bus specification and user manual*, rev. 7, 2021.
- Bosch, *CAN Specification 2.0*, 1991; ISO 11898-1:2024 *Road vehicles: Controller area network (CAN)*.
- CAN in Automation, *CiA 301 (CANopen), CiA 402 (drives)*, <https://www.can-cia.org>.
- EtherCAT Technology Group, *EtherCAT: the Ethernet Fieldbus*, <https://www.ethercat.org>.
- STMicroelectronics, *RM0490*: rozdziały USART, I²C, SPI.
- micro-ROS, *Overview*, <https://micro.ros.org/docs/overview/>; ros2_control, *Hardware Components*, <https://control.ros.org>.

