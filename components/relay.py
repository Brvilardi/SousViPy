from components.hardware.SRD_05VDS_SL_C import SRD_05VDS_SL_C


class Relay:

    def __init__(self):
        self.relay = SRD_05VDS_SL_C(15)

    def turn_on(self):
        self.relay.turn_on()

    def turn_off(self):
        self.relay.turn_off()
