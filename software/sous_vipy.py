import time

from components.display import Display
from components.hardware.linear_potentiometer import LinearPotentiometer
from components.hardware.o_led_display import OLedDisplay_I2C, OLedDisplay_SPI
from software.temperature_control import TemperatureControl


class SousVipy:
    max_temp = 100
    min_temp = 0

    def __init__(self):
        # Initialize the components

        # displayI2C = OLedDisplay_I2C(ic2_id=0, sda=16, scl=17, i2c_freq=200_000)
        display_spi = OLedDisplay_SPI(sck=18, mosi=19, dc=17, res=20, cs=16)
        self.display = Display(display_spi)

        self.temperature_control = TemperatureControl(temperature_sensor_pin=15, relay_pin=14)
        self.potentiometer = LinearPotentiometer(data_pin=26)


        # Update the display
        self.current_temperature = self.temperature_control.get_current_temperature()
        self.desired_temperature = 60 #todo remove this

        self.display.make_headers(system_status="on", heater_status="off", time=0)
        self.display.update_display(
            [
                ("Target", self.desired_temperature),
                ("Current", self.current_temperature),
                ("Status", "set temp")
            ]
        )

        self.init()

    def init(self):
        print("System starting, getting target temperature...")
        if (self.desired_temperature is None):
            self.desired_temperature = self.wait_temperature_input()

        print("Desired temp: {}".format(self.desired_temperature))

        time.sleep(1)

        self.display.update_display(
            [
                ("Target", self.desired_temperature),
                ("Current", self.current_temperature),
                ("Status", "ready")
            ]
        )

        print("System initiating temperature controller")
        self.temperature_control.init(desired_temperature=self.desired_temperature)
        print("System ready!")


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

    def main_loop(self): #todo implement time update
        # takes the temperature to half of the desired temperature
        # self.display.update_display(
        #     [
        #         ("Target", self.desired_temperature),
        #         ("Current", self.current_temperature),
        #         ("On/off", "{:.2f}%".format(100)),
        #         ("status", "warming"),
        #         ("Warm till", "{:.2f}".format(0.8 * self.desired_temperature))
        #     ]
        # )
        # print("Warming up...")
        # self.temperature_control.warm_up()
        # print("Warm up finished")

        while True:
            self.current_temperature, time_on_ration = self.temperature_control()
            self.display.update_display(
                [
                    ("Target", "{:.1f}C".format(self.desired_temperature)),
                    ("Current", "{:.1f}C".format(self.current_temperature)),
                    ("On/off", "{:.1f}%".format(time_on_ration*100)),
                    ("status", "PID")
                ]
            )



