#!/usr/bin/python

import smbus

"""
Class to interface with the Melexis MLX90614 family of infrared thermometers.
"""
class MLX90614:
    _TEMP_RESOLUTION_K = 0.02
    _K_TO_C = 273.15
    
    _AMBIENT_TEMP_REGISTER = 0x06
    _OBJECT_1_TEMP_REGISTER = 0x07
    _OBJECT_2_TEMP_REGISTER = 0x08 # Only present in dual-zone models
    
    
    def __init__(self, bus = 1, addr = 0x5a):
        """
        bus: I2C bus number - eg 1 means /dev/i2c-1, etc
        addr: I2C device address for the sensor
        """
        self._bus = smbus.SMBus(bus)
        self._addr = addr

    @staticmethod
    def _c_to_f(c_temp):
        """
        c: temperature in celsius
        returns: temperature in fahrenheit
        """
        return c_temp * 9.0/5.0 + 32.0
        
    @staticmethod
    def _word_to_c(word):
        """
        Convert a word from the MLX90614 to a temperature
        word: an integer as read from a temperature register on the device
        returns: indicated temperature in celsius
        """
        temp_k = MLX90614._TEMP_RESOLUTION_K * word
        return temp_k - MLX90614._K_TO_C
        
    def read_ambient_temp_f(self):
        """
        returns: ambient temperature (case of sensor) in Fahrenheit
        """
        return MLX90614._c_to_f(self.read_ambient_temp_c())
        
    def read_ambient_temp_c(self):
        """
        returns: ambient temperature (case of sensor) in Celsius
        """
        return MLX90614._word_to_c(self._bus.read_word_data(self._addr, MLX90614._AMBIENT_TEMP_REGISTER))
        
    def read_object1_temp_f(self):
        """
        returns: temperature in first zone of sensor, in Fahrenheit
        """
        return MLX90614._c_to_f(self.read_object1_temp_c())
        
    def read_object1_temp_c(self):
        """
        returns: temperature in first zone of sensor, in Celsius
        """
        return MLX90614._word_to_c(self._bus.read_word_data(self._addr, MLX90614._OBJECT_1_TEMP_REGISTER))
        
    def read_object2_temp_f(self):
        """
        returns: temperature in second zone of sensor, in Fahrenheit - or 0K if this is a single-zone sensor.
        """
        return MLX90614._c_to_f(self.read_object2_temp_c())
        
    def read_object2_temp_c(self):
        """
        returns: temperature in second zone of sensor, in Celsius - or 0K if this is a single-zone sensor.
        """
        return MLX90614._word_to_c(self._bus.read_word_data(self._addr, MLX90614._OBJECT_1_TEMP_REGISTER))

    