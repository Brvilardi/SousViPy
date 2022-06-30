from components.hardware.DS18B20 import DS18B20


class TemperatureSensor:
    """
    Interface to use the TemperatureSensor DS18b20.
    """
    data_pin: int = 16


    def __init__(self):
        """
        Initialize the TemperatureSensor.
        :param data_pin: int - The pin number to set up.
        """
        self.DS18B20 = DS18B20(self.data_pin)

    def get_temperature(self):
        """
        Get the temperature from the sensor.
        :return: float - The temperature in Celsius.
        """
        return self.DS18B20.get_temperature()





