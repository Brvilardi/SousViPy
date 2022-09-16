from machine import Pin


class PushButton:
    """
    Class for Push Button. Use with 10k ohm resistor.
    https://microcontrollerslab.com/push-button-raspberry-pi-pico-tutorial/
    """

    def __init__(self, pin: int):
        self.pin = Pin(pin, Pin.IN, Pin.PULL_UP)

    def is_pressed(self) -> bool:
        return bool(self.pin.value())






