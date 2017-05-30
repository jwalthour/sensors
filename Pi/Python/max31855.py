#!/usr/bin/env python

# Be sure to enable SPI on your Pi before running.
# See the following resources:
# http://raspberrypi-aa.github.io/session3/spi.html
# https://learn.sparkfun.com/tutorials/raspberry-pi-spi-and-i2c-tutorial

# Requires py-spidev, please run the following:
#    sudo apt-get update sudo apt-get install python-dev
#    git clone git://github.com/doceme/py-spidev
#    cd py-spidev
#    sudo python setup.py install
import spidev

class Max31855:
    def __init__(self, bus=0, device=0):
        self._spi = spidev.SpiDev()
        self._spi.open(bus, device)
        self._spi.max_speed_hz = 5000
        self._spi.mode = 0b00
        self._have_reading = False

    def take_reading(self):
        """
        Reads the sensor and stores its measurements internal to this object.
        After calling, use accessors to read data.
        """
        data = self._spi.xfer([0xFF, 0xFF, 0xFF, 0xFF])
        self._parse_data(data)
        self._have_reading = True;

    def thermocouple_temp_c(self):
        """ Returns the temperature measured at the end of the thermocouple """
        if(not self._have_reading):
            raise Exception("Need to take a reading first")
        else:
            return self._thermocouple_temp_c
    def thermocouple_temp_f(self):
        """ Returns the temperature measured at the end of the thermocouple """
        return self._c_to_f(self.thermocouple_temp_c())

    def internal_temp_c(self):
        """ Returns the temperature of the Max31855 die """
        if(not self._have_reading):
            raise Exception("Need to take a reading first")
        else:
            return self._internal_temp_c
    def internal_temp_f(self):
        """ Returns the temperature of the Max31855 die """
        return self._c_to_f(self.internal_temp_c())

    def is_faulted(self):
        """
        Returns true if the Max31855 reports a problem with
        the thermocouple connection
        """
        if(not self._have_reading):
            raise Exception("Need to take a reading first")
        else:
            return self._fault

    def fault_reason(self):
        """
        Return a human-readable string describing the
        fault reported by the Max31855
        """
        if(not self._have_reading):
            raise Exception("Need to take a reading first")
        else:
            if not self._fault:
                return "No fault"
            elif self._short_to_vcc:
                return "Short to Vcc"
            elif self._short_to_gnd:
                return "Short to Gnd"
            elif self._open_circuit:
                return "Open circuit"
            else:
                return "Unknown"

    @classmethod
    def _c_to_f(cls, c_temp):
        return c_temp * 9.0/5.0 + 32.0

    def _parse_data(self, arr):
        """
        Takes a 4B string from the Max31855 and
        breaks out its constituents.
        Argument must be an array of 4 byte values.
        """
        # See datasheet for explanation
        print(" ".join(["%02X"%b for b in arr]))
        first_half = (arr[0]<<8) + arr[1]
        second_half = (arr[2]<<8) + arr[3]
        unsigned = ((first_half >> 2) & 0x3fff)
        if(unsigned & 0x2000 > 0):
                signed = ~unsigned + 1
                signed *= -1.0
        else:
                signed = unsigned
        print("tc raw = %04x"%signed)
        self._thermocouple_temp_c = signed * 0.25

        unsigned = ((second_half >> 4) & 0x7ff)
        if(unsigned & 0x400 > 0):
                signed = ~unsigned + 1
                signed *= -1.0
        else:
                signed = unsigned
        print("int raw = %04x"%signed)
        self._internal_temp_c = ((second_half >> 4) & 0x7ff) * 0.0625

        self._fault = ((first_half & 0x0001) > 0)
        self._short_to_vcc = ((second_half & 0x0004) > 0)
        self._short_to_gnd = ((second_half & 0x0002) > 0)
        self._open_circuit = ((second_half & 0x0001) > 0)


