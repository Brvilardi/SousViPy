from machine import ADC


class Potentiometer:
    """
    Class for potentiometer.
    """
    min_pot = 0
    max_pot = 65535

    def __init__(self, data_pin: int):
        self.adc = ADC(data_pin)

    def get_value(self) -> float:
        """
        Get the value of the potentiometer.
        :return: value 0.0-1.0
        """

        # round to 2 decimals
        return round(self.adc.read_u16() / self.max_pot, 2)






