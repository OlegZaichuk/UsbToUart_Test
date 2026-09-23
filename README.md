# UsbToUart_Test

**UsbToUart_Test** is a utility for testing the **USB-UART** interface, verifying data transmission stability, and validating communication with the **LRFX0M20PD** laser rangefinder. The project supports both real sensor data reading and a self-diagnostic (Loopback) mode.

## 📌 Table of Contents
* [Features](#-features)
* [Supported Hardware](#-supported-hardware)
* [Hardware Setup](#-hardware-setup)
* [Testing Modes](#-testing-modes)
* [License](#-license)

## ✨ Features
* **Two Operational Modes:** Laser rangefinder data parsing or hardware Loopback (echo) testing.
* **Flexible Configuration:** Easy selection of COM ports and standard baud rates.
* **Integrity Control:** Verification of data packets received from the rangefinder.

## 🔌 Supported Hardware
The project is tested and optimized for the following TTL converters:
* **CP2102** (Silicon Labs USB-to-UART Bridge)
* **CJMCU-4232** (4-channel USB-UART bridge based on FT4232)

The primary testing device is the **LRFX0M20PD** laser rangefinder (or compatible UART-based distance modules).

## 🛠 Hardware Setup

### Option 1: Connecting the LRFX0M20PD Rangefinder
Connect the rangefinder to your TTL converter (CP2102 / CJMCU-4232) using the standard Cross-TX/RX scheme:

| LRFX0M20PD Rangefinder | TTL Converter |
| :--- | :--- |
| **VCC** (Power) | 3.3V / 5V *(depending on sensor specs)* |
| **GND** (Ground) | GND |
| **TX** (Transmit) | RX |
| **RX** (Receive) | TX |

### Option 2: Loopback Mode (Hardware Jumper)
If the rangefinder is not connected, you can test the USB-UART converter itself. To do this, **short the RX and TX pins together** using a jumper wire on your board (CP2102 or CJMCU-4232).

## 🚀 Testing Modes

1. **Rangefinder Test:** The script sends distance request commands to the LRFX0M20PD, receives the response, parses the incoming bytes, and outputs the distance in a readable format.
2. **Loopback Test (RX/TX shorted):** The application sends a test string or byte array into the port and verifies if it returns identically. This helps identify driver or hardware issues.

## 📜 License
This project is licensed under the [MIT](LICENSE) License.