from machine import ADC


class LinearPotentiometer:
    min_pot = 57000
    max_pot = 65535

    def __init__(self, data_pin: int):
        self.adc = ADC(data_pin)

    def get_value(self) -> float:
        """
        Get the value of the potentiometer.
        :return: value 0.0-1.0
        """
        value = self.adc.read_u16()

        if value < LinearPotentiometer.min_pot: return 0.0
        if value > LinearPotentiometer.max_pot: return 1.0

        return ((value - LinearPotentiometer.min_pot) * 100) / (LinearPotentiometer.max_pot - LinearPotentiometer.min_pot)


