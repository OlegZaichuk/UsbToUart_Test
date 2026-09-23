# Documentation: LRFX0M20PD Laser Rangefinder Series

Quick reference guide for **LRF80M20PD**, **LRF140M20PD**, and **LRF200M20PD** modules by **IADIY** (ver. 2.0).

---

## 📈 Key Specifications

| Parameter | Value |
| :--- | :--- |
| **Measurement Range** | 0.05m ~ 80m / 140m / 200m (indoor) |
| **Frequency** | 1 ~ 20 Hz |
| **Accuracy** | ±1mm (@40m), ±2mm (@80m), ±7mm (@140m), ±15mm (@200m) |
| **Laser Wavelength** | 650 nm (red) |
| **Laser Safety** | Class 2 (for 80m) / Class 3R (for 140m/200m) |
| **Communication Interface** | 3.3V TTL (UART), **9600 bps** default baud rate (8N1) |
| **Power Supply** | 3.3 ~ 4.2V DC, **120 mA** consumption |
| **Dimensions & Weight** | 46.5 x 37 x 17.4 mm, 22±1 g |
| **Protection Rating** | IP40 |

*Note: When measuring targets over 100 meters away with a reflectivity below 70%, a reflective film must be applied to improve reflectivity.*

---

## 💻 Control Command List

All data bytes are expressed in hexadecimal format (**HEX**). 
* `ADD` — Module address (default is `0x80`, broadcast address is `0xFA`).
* `CHK` — Checksum (sum up all preceding bytes and take the complement).

### 1. Measurement Commands
* **Single Measurement**
  * **Command:** `ADD 06 02 CHK` (Example for address 0x80: `80 06 02 78`)
  * **Description:** Triggers and returns a single distance reading. The response data is in ASCII format (e.g., "123.456" is sent as a sequence of bytes: `31 32 33 2E 34 35 36`). Returns `ERR` text on failure.
* **Continuous Measurement**
  * **Command:** `ADD 06 03 CHK` (Example: `80 06 03 77`)
  * **Description:** Starts continuous real-time measurements based on the configured interval time.
* **Stop Measurement**
  * **Command:** `ADD 04 02 CHK` (Example: `80 04 02 7A`)
  * **Description:** Halts the continuous measurement mode.

### 2. Device Configuration Commands
* **Laser ON/OFF**
  * **Command:** `ADD 06 05 01 CHK` (ON) / `ADD 06 05 00 CHK` (OFF)
  * **Description:** Manually forces the laser targeting beam to turn on or off.
* **Set Address**
  * **Command:** `ADD_old 04 01 ADD_new CHK`
  * **Description:** Changes the current module address to a new one (valid range: `0x00` ~ `0xFF`).
* **Set Frequency**
  * **Command:** `ADD 04 0A [FREQ] CHK`
  * **Parameters:** `0x00` = 3Hz, `0x05` = 5Hz, `0x0A` = 10Hz, `0x14` = 20Hz.
* **Set Resolution**
  * **Command:** `ADD 04 0C 01 CHK` (1mm) / `ADD 04 0C 02 CHK` (0.1mm)
  * **Description:** Changes the measurement decimal precision output in responses.
* **Set Offset**
  * **Command:** `ADD 04 06 SIGN DIST CHK`
  * **Description:** Sets a custom calibration offset value. `SIGN`: `0x2B` (+), `0x2D` (-). `DIST` is the offset value.
* **Measure Upon Power-On**
  * **Command:** `ADD 04 0D 01 CHK` (Enable) / `ADD 04 0D 00 CHK` (Disable)
  * **Description:** When enabled, the module automatically starts continuous measurement immediately after powering up.
