import time

from components.relay import Relay
from components.temperature_sensor import TemperatureSensor
from software.modules.simple_pid import PID


class SousVipy:
    sample_time: float = 15.0  # seconds
    max_temp: float = 100.0  # degrees Celsius
    min_temp: float = 0.0 # degrees Celsius
    max_pid_output: float = 1000.0
    min_pid_output: float = -max_pid_output

    def __init__(self, desired_temperature: float = 65):
        # imporant variables to consider: desired_temperature, superficie contato (area da panela), faixa de temperatura (0-100), temperatura ambiente

        # Initialize components
        self.temperature_sensor = TemperatureSensor(data_pin=16)
        self.relay = Relay(pin_number=15)
        self.pid_controller = PID(Kp=1.0, Ki=3.0, Kd=0.2, setpoint=desired_temperature, sample_time=SousVipy.sample_time, output_limits=(SousVipy.min_pid_output, SousVipy.max_pid_output))

        # Make sure the relay is off
        self.relay.turn_off()

        # Set up the Initial temperatures
        self.desired_temperature = desired_temperature
        self.current_temperature = self.temperature_sensor.get_temperature()

        # Initialize the log variables
        self.log_desired_temperature = []
        self.log_current_temperature = []
        self.log_pid_output = []
        self.log_relay_state = []
        self.time = []

    def update_system(self):
        # Update system
        self.current_temperature = self.temperature_sensor.get_temperature()
        pid_output = self.pid_controller(self.current_temperature)

        # Update the log variables
        self.log_desired_temperature.append(self.desired_temperature)
        self.log_current_temperature.append(self.current_temperature)
        self.log_pid_output.append(pid_output)
        self.log_relay_state.append(self.relay.get_state())
        self.time.append(self.time[-1] + SousVipy.sample_time) if len(self.time) > 0 else self.time.append(0)

        return self.current_temperature, pid_output, self.relay.get_state()

    def calculate_time_on_ratio(self, pid_output: float) -> float:
        """
        Calculate the time the relay should be on/off ratio based on the current temperature, pid_output, min_temp and max_temp.
        :param pid_output:
        :return: ratio 0.0-1.0
        """
        # Min / Max temperature
        if self.current_temperature <= SousVipy.min_temp:  # Too cold
            return 1.0
        elif self.current_temperature >= SousVipy.max_temp:  # Too hot
            return 0.0

        # Calculate the time the relay should be on/off ratio
        if pid_output < 0:
            return 0.0

        # pid_output is between 0 and max_pid_output
        return pid_output / SousVipy.max_pid_output

    def get_setup_relay_timer(self, time_on_ratio: float):
        """
        Setup the relay timer.
        :param time_on_ratio: float - The time the relay should be on/off ratio.
        """
        def func():
            self.relay.turn_on()
            time.sleep(time_on_ratio * SousVipy.sample_time)
            self.relay.turn_off()
            time.sleep(SousVipy.sample_time - time_on_ratio * SousVipy.sample_time)

        return func



    def run_loop(self):
        # TODO implement a way to save the logs
        while True:
            current_status = self.update_system()
            time_on_ratio = self.calculate_time_on_ratio(self.pid_controller(self.current_temperature))
            print("Time on ration: {}".format(time_on_ratio))
            scheduler = self.get_setup_relay_timer(time_on_ratio)
            scheduler()
            print("{} {} {}".format(current_status[0], current_status[1], current_status[2]))








