import time

from components.relay import Relay
from components.temperature_sensor import TemperatureSensor
from components.display import Display

# sensor = TemperatureSensor(16)
# relay = Relay(15)

# disp = Display(ic2_id=0, sda=16, scl=17, i2c_freq=200_000)
# cont = 0

# while True:
#     disp.display.clear()
#     disp.make_headers(time=cont)
#     disp.update_display({
#                 "Target": "XC",
#                 "Current": "YC"
#             })
#     cont += 1
#     time.sleep(1)
#     print(cont)
#     print("{}".format(disp.calculate_time_string(cont)))
from software.sous_vipy import SousVipy

sous_vipy = SousVipy()
