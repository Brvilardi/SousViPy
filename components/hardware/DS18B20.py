from machine import Pin
import onewire
import ds18x20


class DS18B20:
    """
    Class that represents the usage of the Temperature Sensor DS18B20
    Datasheet: https://datasheets.maximintegrated.com/en/ds/DS18B20.pdf
    """

    def __init__(self, pin_number: int):
        """
        Initialize the Temperature Sensor.
        :param pin_number: int - The pin number to set up.
        """

        self.pin = Pin(pin_number, mode=Pin.IN, pull=Pin.PULL_UP)
        self.sensor = ds18x20.DS18X20(onewire.OneWire(self.pin))
        roms = self.sensor.scan()
        if len(roms) == 0:
            raise Exception("No DS18B20 found on pin {}".format(pin_number))
        elif len(roms) > 1:
            raise Exception("More than one DS18B20 found on pin {}".format(pin_number))
        else:
            self.rom = roms[0]
        self.sensor.convert_temp()

    def get_temperature(self):
        """
        Get the temperature from the sensor.
        :return: float - The temperature in Celsius.
        """
        self.sensor.convert_temp()
        return round(self.sensor.read_temp(self.rom), 2) # Resolution is 0.5°C, so there is no point in more than 2 decimals.
