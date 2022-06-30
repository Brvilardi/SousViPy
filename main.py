import time

from components.temperature_sensor import TemperatureSensor

sensor = TemperatureSensor()

while True:
    print(sensor.get_temperature())
    time.sleep(1)

