#!/usr/bin/env python3
"""Driver for the IADIY LRF140M20PD laser rangefinder (LRFX0M20PD series).

Protocol reference: Doc/LRF200M20PD.md (covers LRF80/140/200M20PD).
Defaults: 9600 bps, 8N1, module address 0x80.
"""
import re
import time

import serial
import serial.tools.list_ports

# Distance replies are ASCII, e.g. b"123.456" (1 mm) or b"123.4567" (0.1 mm).
_DISTANCE_RE = re.compile(rb"(\d+\.\d+)")
_ERROR_RE = re.compile(rb"ERR")


class LRF140M20PD:
    """Single/continuous distance measurement over UART."""

    DEFAULT_BAUDRATE = 9600
    DEFAULT_ADDRESS = 0x80
    BROADCAST_ADDRESS = 0xFA

    # Set Frequency parameter values (Doc/LRF200M20PD.md).
    FREQUENCIES = {3: 0x00, 5: 0x05, 10: 0x0A, 20: 0x14}

    def __init__(self, port, baudrate=DEFAULT_BAUDRATE,
                 address=DEFAULT_ADDRESS, timeout=1.0):
        self.port = port
        self.baudrate = baudrate
        self.address = address
        self.timeout = timeout
        self._uart = None
        self._buffer = bytearray()

    # --- UART port ---------------------------------------------------------

    @staticmethod
    def available_ports():
        """Return a list of serial port device names found on the system."""
        return [p.device for p in serial.tools.list_ports.comports()]

    def open(self):
        """Open the selected UART port."""
        if self._uart is None:
            self._uart = serial.Serial(
                self.port, self.baudrate, timeout=self.timeout,
                write_timeout=self.timeout,
                bytesize=8, parity="N", stopbits=1,
                xonxoff=False, rtscts=False, dsrdtr=False,
            )
            self._buffer.clear()
        return self

    def close(self):
        """Close the UART port."""
        if self._uart is not None:
            self._uart.close()
            self._uart = None

    def __enter__(self):
        return self.open()

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    # --- Frames ------------------------------------------------------------

    @staticmethod
    def checksum(payload):
        """Two's complement of the sum of all preceding bytes."""
        return (-sum(payload)) & 0xFF

    def _frame(self, *payload):
        frame = bytearray((self.address, *payload))
        frame.append(self.checksum(frame))
        return bytes(frame)

    def _require_open(self):
        if self._uart is None:
            raise RuntimeError("Port is not open; call open() first.")

    def _send(self, *payload):
        self._require_open()
        self._uart.write(self._frame(*payload))
        self._uart.flush()

    def _read_distance(self, timeout):
        """Read one ASCII distance reply.

        Returns the distance in metres, or None if the module answered ERR
        or sent nothing within `timeout` seconds.
        """
        deadline = time.monotonic() + timeout
        while True:
            # Read group() before trimming: a match on a bytearray is a view
            # into it, so mutating the buffer first would empty the group.
            match = _DISTANCE_RE.search(self._buffer)
            if match:
                distance = float(match.group(1))
                del self._buffer[:match.end()]
                return distance
            error = _ERROR_RE.search(self._buffer)
            if error:
                del self._buffer[:error.end()]
                return None
            if time.monotonic() >= deadline:
                return None
            chunk = self._uart.read(self._uart.in_waiting or 1)
            if chunk:
                self._buffer += chunk
            elif len(self._buffer) > 64:
                # Keep only a possible partial reading, drop stale bytes.
                del self._buffer[:-16]

    # --- Measurement -------------------------------------------------------

    def single_measurement(self):
        """Trigger one measurement: ADD 06 02 CHK.

        Returns the distance in metres, or None on ERR/timeout.
        """
        self._require_open()
        self._buffer.clear()
        self._uart.reset_input_buffer()
        self._send(0x06, 0x02)
        return self._read_distance(self.timeout)

    def continuous_measurement(self, callback, max_errors=5):
        """Start continuous measurement: ADD 06 03 CHK.

        `callback(distance_in_metres)` is invoked for every successful
        reading; returning False stops the loop. Stops after `max_errors`
        consecutive failed reads. Stop Measurement is always sent on exit.
        """
        self._require_open()
        self._buffer.clear()
        self._uart.reset_input_buffer()
        self._send(0x06, 0x03)
        errors = 0
        try:
            while errors < max_errors:
                distance = self._read_distance(self.timeout)
                if distance is None:
                    errors += 1
                    continue
                errors = 0
                if callback(distance) is False:
                    return
        finally:
            self.stop_measurement()

    def stop_measurement(self):
        """Halt continuous measurement: ADD 04 02 CHK."""
        self._send(0x04, 0x02)
        time.sleep(0.1)
        self._uart.reset_input_buffer()
        self._buffer.clear()

    # --- Configuration -----------------------------------------------------

    def laser_on(self):
        """Turn the targeting beam on: ADD 06 05 01 CHK."""
        self._send(0x06, 0x05, 0x01)

    def laser_off(self):
        """Turn the targeting beam off: ADD 06 05 00 CHK."""
        self._send(0x06, 0x05, 0x00)

    def set_frequency(self, hz):
        """Set the continuous measurement rate: ADD 04 0A FREQ CHK.

        Supported values: 3, 5, 10, 20 Hz.
        """
        if hz not in self.FREQUENCIES:
            raise ValueError(
                f"Unsupported frequency {hz} Hz; "
                f"use one of {sorted(self.FREQUENCIES)}"
            )
        self._send(0x04, 0x0A, self.FREQUENCIES[hz])


if __name__ == "__main__":
    import sys

    device = sys.argv[1] if len(sys.argv) > 1 else "/dev/ttyUSB0"
    print(f"Available ports: {LRF140M20PD.available_ports()}")
    with LRF140M20PD(device) as lrf:
        print(f"Single: {lrf.single_measurement()} m")

        readings = []

        def on_reading(distance):
            readings.append(distance)
            print(f"Continuous: {distance} m")
            return len(readings) < 5

        lrf.continuous_measurement(on_reading)
