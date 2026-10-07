#!/usr/bin/env python3
"""Turn on the aiming laser, then trigger one distance reading."""
import sys

from lrf140m20pd import LRF140M20PD

PORT = sys.argv[1] if len(sys.argv) > 1 else "/dev/ttyUSB0"
BAUD = int(sys.argv[2]) if len(sys.argv) > 2 else LRF140M20PD.DEFAULT_BAUDRATE

try:
    with LRF140M20PD(PORT, BAUD) as lrf:
        print(f"Port: {PORT}, baud: {BAUD}")
        lrf.laser_on()
        distance = lrf.single_measurement()
        if distance is None:
            print("Result: no reading (ERR or timeout)")
            sys.exit(1)
        print(f"Result: {distance} m")
        sys.exit(0)
except (OSError, RuntimeError) as error:
    print(f"Error: {error}")
    sys.exit(1)
