from components.hardware.DS18B20 import DS18B20


class TemperatureSensor:
    """
    Interface to use the TemperatureSensor DS18b20.
    """


    def __init__(self, data_pin: int):
        """
        Initialize the TemperatureSensor.
        :param data_pin: int - The pin number to set up.
        """
        self.sensor = DS18B20(data_pin)

    def get_temperature(self):
        """
        Get the temperature from the sensor.
        :return: float - The temperature in Celsius.
        """
        return self.sensor.get_temperature()





