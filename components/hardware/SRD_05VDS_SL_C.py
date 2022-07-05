from machine import Pin

class SRD_05VDS_SL_C:


    def __init__(self, data_pin: int):
        self.pin = Pin(data_pin, mode=Pin.OUT)
        self.state = False
        self.pin.value(self.state)

    def get_state(self):
        return self.state

    def set_state(self, state: bool):
        self.state = state
        self.pin.value(self.state)

    def turn_on(self):
        self.set_state(True)

    def turn_off(self):
        self.set_state(False)

    def toggle(self):
        self.set_state(not self.get_state())

