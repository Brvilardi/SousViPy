import time

from components.relay import Relay
from components.temperature_sensor import TemperatureSensor
from software.modules.simple_pid import PID


class TemperatureControl:
    sample_time: float = 5.0  # seconds
    max_temp: float = 100.0  # degrees Celsius
    min_temp: float = 0.0  # degrees Celsius
    max_pid_output: float = 100.0
    min_pid_output: float = -max_pid_output

    def __init__(self, temperature_sensor_pin: int, relay_pin: int):
        # imporant variables to consider: desired_temperature, superficie contato (area da panela), faixa de temperatura (0-100), temperatura ambiente

        # Initialize components
        self.temperature_sensor = TemperatureSensor(data_pin=temperature_sensor_pin)  # 16
        self.relay = Relay(pin_number=relay_pin)  # 15

        # Make sure the relay is off
        self.relay.turn_off()

        # Initialize the variables to be implemented on init method
        self.pid_controller = None
        self.desired_temperature = None
        self.current_temperature = None

    def init(self, desired_temperature: float):
        self.pid_controller = PID(Kp=30.0, Kd=25, setpoint=desired_temperature*1.025,
                                  sample_time=TemperatureControl.sample_time,
                                  output_limits=(TemperatureControl.min_pid_output, TemperatureControl.max_pid_output)) #ki not used and desired temperature is increased by 10% to compensate that

        # Set up the Initial temperatures
        self.desired_temperature = desired_temperature
        self.current_temperature = self.temperature_sensor.get_temperature()

    def update_system(self):
        # Update system
        self.current_temperature = self.temperature_sensor.get_temperature()
        pid_output = self.pid_controller(self.current_temperature)

        return self.current_temperature, pid_output, self.relay.get_state()

    def calculate_time_on_ratio(self, pid_output: float) -> float:
        """
        Calculate the time the relay should be on/off ratio based on the current temperature, pid_output, min_temp and max_temp.
        :param pid_output:
        :return: ratio 0.0-1.0
        """
        # Min / Max temperature
        if self.current_temperature <= TemperatureControl.min_temp:  # Too cold
            print("Too cold! Manually turning on the relay")
            return 1.0
        elif self.current_temperature >= TemperatureControl.max_temp:  # Too hot
            print("Too hot! Manually turning off the relay")
            return 0.0

        # Calculate the time the relay should be on/off ratio
        if pid_output < 0:
            return 0.0

        # pid_output is between 0 and max_pid_output
        return pid_output / TemperatureControl.max_pid_output

    def get_setup_relay_timer(self, time_on_ratio: float):
        """
        Setup the relay timer.
        :param time_on_ratio: float - The time the relay should be on/off ratio 0.1~1.0.
        """

        def func():
            if (time_on_ratio > 0.0):
                self.relay.turn_on()
                time.sleep(time_on_ratio * TemperatureControl.sample_time)
            if (time_on_ratio < 1.0):
                self.relay.turn_off()
                time.sleep(TemperatureControl.sample_time - time_on_ratio * TemperatureControl.sample_time)

        return func

    def warm_up(self):
        # warms until the current temperature is <= to 80% of the desired temperature
        while self.current_temperature <= (0.8 * self.desired_temperature):
            self.current_temperature = self.temperature_sensor.get_temperature()
            scheduler = self.get_setup_relay_timer(1.0)
            print("Warming up - curr {} | warm_target {}| final_target {}".format(self.current_temperature,
                                                                                  (0.8 * self.desired_temperature),
                                                                                  self.desired_temperature))
            scheduler()

    def __call__(self):
        # TODO implement a way to save logs
        current_status = self.update_system()
        time_on_ratio = self.calculate_time_on_ratio(self.pid_controller(self.current_temperature))
        print("cur temp {:.2f} | pid_tot {:.1f} | on/off {:.2f}% |--| PID: p {:.2f} | i {:.2f} | d {:.2f}".format(current_status[0],
                                                                                        current_status[1],
                                                                                        time_on_ratio*100,
                                                                                        self.pid_controller._proportional,
                                                                                        self.pid_controller._integral,
                                                                                        self.pid_controller._derivative)
              )

        scheduler = self.get_setup_relay_timer(time_on_ratio)
        scheduler()

        return [self.current_temperature, time_on_ratio]

    # Auxiliar funcionts

    def turn_off_relay(self):
        self.relay.turn_off()

    def get_current_temperature(self):
        return self.temperature_sensor.get_temperature()
