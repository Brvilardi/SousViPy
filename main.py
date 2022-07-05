import time

from components.relay import Relay
from components.temperature_sensor import TemperatureSensor

sensor = TemperatureSensor(16)
relay = Relay(15)

while True:
    # print(sensor.get_temperature())
    relay.turn_on()
    time.sleep(1)

