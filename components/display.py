from components.hardware.o_led_display import OLedDisplay


class Display:

    def __init__(self, ic2_id: int = 1, sda: int = 26, scl: int = 27, i2c_freq: int = 200_000):
        self.display = OLedDisplay(ic2_id=ic2_id, sda=sda, scl=scl, i2c_freq=i2c_freq)
        self.display.clear()
        self.make_headers("on", "off", 0)
        self.update_display(
            [
                ("Target", "XC"),
                ("Current", "YC")
            ]
        )

    def make_headers(self, system_status: str = "on", heater_status: str = "off", time: int = 0):
        self.header_1 = "S: {} | H: {}".format(system_status, heater_status)
        self.header_2 = "Time: {}".format(self.calculate_time_string(time))


    def update_display(self, body):
        self.display.clear()
        self.display.show_text(self.header_1, 0, 0)
        self.display.show_text(self.header_2, 0, 9)
        self.draw_body(body)


    def draw_body(self, body_list: dict):
        cont = 0
        for i in body_list:
            self.display.show_text("{}: {}".format(i[0], i[1]), 0, (cont+2) * 9)
            cont += 1

    def calculate_time_string(self, time_since_begining: int):
        hour = time_since_begining // 60 // 60 if (time_since_begining // 60 // 60 > 10) else "0{}".format(time_since_begining // 60 // 60)
        min = time_since_begining // 60 if (time_since_begining // 60 > 10) else "0{}".format(time_since_begining // 60)
        sec = time_since_begining % 60 if (time_since_begining % 60 > 10) else "0{}".format(time_since_begining % 60)

        return "{}:{}:{}".format(hour, min, sec)


