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
# import spidev

class Max31855:
    def Max31855(self, bus=0, device=0):
        # self._spi = spidev.SpiDev()
        # self._spi.open(bus, device)
        # self._spi.max_speed_hz = 5000
        # self._spi.mode = 0b01
        pass
        
    def take_reading(self):
        """
        Reads the sensor and stores its measurements internal to this object.
        After calling, use accessors to read data.
        """
        data = self._spi.xfer2([0, 0, 0, 0])
        self.parse_data(data)

    def _parse_data(self, arr):
        """
        Takes a 4B string from the Max31855 and
        breaks out its constituents.
        Argument must be an array of 4 byte values.
        """
        # See datasheet for explanation        
        first_half = (arr[0]<<8) + arr[1]
        second_half = (arr[2]<<8) + arr[3]
        self._thermocouple_temp_c = ((first_half >> 2) & 0x1fff) * 0.25
        if(((first_half >> 2) & 0x2000) > 0):
            self._thermocouple_temp_c *= -1
        self._internal_temp_c = ((second_half >> 4) & 0x7ff) * 0.0625
        if(((second_half >> 4) & 0x800) > 0):
            self._internal_temp_c *= -1
        self._fault = ((first_half & 0x0001) > 0)
        self._short_to_vcc = ((second_half & 0x0004) > 0)
        self._short_to_gnd = ((second_half & 0x0002) > 0)
        self._open_circuit = ((second_half & 0x0001) > 0)
    
    