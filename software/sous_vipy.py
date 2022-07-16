import time

from components.display import Display
from components.hardware.linear_potentiometer import LinearPotentiometer
from software.temperature_control import TemperatureControl


class SousVipy:
    max_temp = 100
    min_temp = 0

    def __init__(self):
        # Initialize the components
        self.display = Display(ic2_id=0, sda=16, scl=17, i2c_freq=200_000)
        self.temperature_control = TemperatureControl(temperature_sensor_pin=15, relay_pin=14)
        self.potentiometer = LinearPotentiometer(data_pin=26)


        # Update the display
        self.current_temperature = self.temperature_control.temperature_sensor.get_temperature()
        self.desired_temperature = 35

        self.display.make_headers(system_status="on", heater_status="off", time=0)
        self.display.update_display(
            [
                ("Target", self.desired_temperature),
                ("Current", self.current_temperature),
                ("Next", "Pres button...")
            ]
        )

        self.init()

    def init(self):
        print("Desired temp: {}".format(self.desired_temperature))
        if (self.desired_temperature is None):
            self.desired_temperature = self.wait_temperature_input()

        time.sleep(3)

        self.display.update_display(
            [
                ("Target", self.desired_temperature),
                ("Current", self.current_temperature),
                ("Next", "System starting")
            ]
        )

        self.temperature_control.init(desired_temperature=self.desired_temperature,
                                      current_temperature=self.temperature_control.temperature_sensor.get_temperature())

    def wait_temperature_input(self):
        pot = self.parse_pot(self.potentiometer.get_value())

        time_to_wait = 10 # s
        cont = 0

        self.display.update_display(
            [
                ("Select", "temperature"),
                ("Current", pot),
                ("Status", "slide pot...")
            ]
        )

        time.sleep(1.5)

        while True:
            new_pot = self.parse_pot(self.potentiometer.get_value())
            if (new_pot == pot):
                cont += 1
                self.display.update_display(
                    [
                        ("Select", "temperature"),
                        ("Current", new_pot),
                        ("Status", "hold"),
                        ("Hold more", time_to_wait - cont)


                    ]
                )
                if (cont >= time_to_wait):
                    self.display.update_display(
                        [
                            ("Select", "temperature"),
                            ("Current", pot),
                            ("Status", "temp selected")

                        ]
                    )
                    return pot
            else:
                pot = new_pot
                cont = 0
                self.display.update_display(
                    [
                        ("Select", "temperature"),
                        ("Current", pot),
                        ("Status", "slide pot...")
                    ]
                )
            time.sleep(1)



    def parse_pot(self, pot_value):
        pot = round(pot_value / 5) * 5
        return ((pot - SousVipy.min_temp) * 100) / (SousVipy.max_temp - SousVipy.min_temp)

    def main_loop(self):
        while True:
            self.current_temperature, time_on_ration = self.temperature_control()
            self.display.update_display(
                [
                    ("Target", self.desired_temperature),
                    ("Current", self.current_temperature),
                    ("On/off", "{}%".format(time_on_ration*100))
                ]
            )



