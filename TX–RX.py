#!/usr/bin/env python3
"""Connect TX to RX on the same adapter before running this test."""
import sys
import time

import serial

PORT = sys.argv[1] if len(sys.argv) > 1 else "/dev/ttyUSB0"
BAUD = int(sys.argv[2]) if len(sys.argv) > 2 else 921600
TESTS = 10

try:
    with serial.Serial(
        PORT, BAUD, timeout=2, write_timeout=2,
        bytesize=8, parity="N", stopbits=1,
        xonxoff=False, rtscts=False, dsrdtr=False,
    ) as uart:
        time.sleep(0.2)
        print(f"Port: {PORT}, baud: {BAUD}, 8N1")
        passed = 0
        for i in range(1, TESTS + 1):
            uart.reset_input_buffer()
            sent = f"UART_TEST_{BAUD}_{i}\n".encode("ascii")
            uart.write(sent)
            received = uart.read(len(sent))
            if received == sent:
                passed += 1
                print(f"{i}/{TESTS}: OK")
            else:
                print(f"{i}/{TESTS}: FAIL | sent={sent!r}, received={received!r}")
            time.sleep(0.1)
        print(f"Result: {passed}/{TESTS} passed")
        sys.exit(0 if passed == TESTS else 1)
except (serial.SerialException, OSError) as error:
    print(f"Error: {error}")
    sys.exit(1)
