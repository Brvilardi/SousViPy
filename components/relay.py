from components.hardware.SRD_05VDS_SL_C import SRD_05VDS_SL_C


class Relay:
    """
    Interface to use the 5VDC to 110AC Relay (SRD-05VDS-SL-C).
    """

    def __init__(self, pin_number: int):
        """
        Initialize the Relay.
        :param pin_number:
        """

        self.relay = SRD_05VDS_SL_C(pin_number)

    def turn_on(self):
        self.relay.turn_on()

    def turn_off(self):
        self.relay.turn_off()
