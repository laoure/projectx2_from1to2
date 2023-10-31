import time
import platform
import psutil
import threading
import random


class DummySensor:
    def __init__(self):
        self.env_values = {}

    def set_env(self):
        self.env_values['mars_base_internal_temperature'] = round(random.uniform(18, 30), 1)
        self.env_values['mars_base_external_temperature'] = round(random.uniform(0, 21), 1)
        self.env_values['mars_base_internal_humidity'] = round(random.uniform(50, 60), 1)
        self.env_values['mars_base_external_illuminance'] = round(random.uniform(500, 715), 1)
        self.env_values['mars_base_internal_co2'] = round(random.uniform(0.02, 0.1), 2)
        self.env_values['mars_base_internal_oxygen'] = round(random.uniform(4, 7), 1)

    def get_env(self):
        return self.env_values


class MissionComputer:
    def __init__(self, sensor):
        self.env_values = {}
        self.sensor = sensor
        self.data_count = 0
        self.total_values = {}

    def update_tot_values(self, current_data):
        for key, value in current_data.items():
            if key not in self.total_values:
                self.total_values[key] = value
            else:
                self.total_values[key] += value
        self.data_count += 1

    def get_average(self):
        env_avg = {}
        for key, value in self.total_values.items():
            avg_value = round(value / self.data_count, 4)
            env_avg[key] = avg_value

        json_str = "{\n"
        for key, value in env_avg.items():
            json_str += f'    "{key}": '
            if isinstance(value, str):
                json_str += f'"{value}",\n'
            else:
                json_str += f'{value},\n'
        json_str = json_str.rstrip(",\n")
        json_str += "\n}"
        print("5분 동안의 평균값은...\n", json_str)

    def reset_data(self):
        self.env_values = {}
        self.data_count = 0

    @staticmethod
    def get_mission_computer_info():
        while True:
            system_info = {
                'Operating System': platform.system(),
                'OS Version': platform.release(),
                'CPU Type': platform.processor(),
                'CPU Cores': psutil.cpu_count(logical=False),
                'Total Memory (GB)': round(psutil.virtual_memory().total / (1024 ** 3), 2)
            }

            json_str = "{\n"
            for key, value in system_info.items():
                json_str += f'    "{key}": '
                if isinstance(value, str):
                    json_str += f'"{value}",\n'
                else:
                    json_str += f'{value},\n'
            json_str = json_str.rstrip(",\n")
            json_str += "\n}"

            print("mission-computer info...\n", json_str)
            time.sleep(20)

    @staticmethod
    def get_mission_computer_load():
        while True:
            cpu_percent = psutil.cpu_percent(interval=1)

            memory = psutil.virtual_memory()
            memory_percent = memory.percent

            load_info = {
                'CPU Usage (%)': cpu_percent,
                'Memory Usage (%)': memory_percent
            }

            json_str = "{\n"
            for key, value in load_info.items():
                json_str += f'    "{key}": {value},\n'
            json_str = json_str.rstrip(",\n")
            json_str += "\n}"

            print("Real-time Load Info...\n", json_str)
            time.sleep(20)

    def get_sensor_data(self):
        while True:
            self.sensor.set_env()
            current_data = self.sensor.get_env()
            self.env_values = current_data
            self.update_tot_values(current_data)

            json_str = "{\n"
            for key, value in self.env_values.items():
                json_str += f'    "{key}": '
                if isinstance(value, str):
                    json_str += f'"{value}",\n'
                else:
                    json_str += f'{value},\n'
            json_str = json_str.rstrip(",\n")
            json_str += "\n}"
            print("센서에서 정보를 읽어왔습니다...\n", json_str)

            if self.data_count >= 3:
                self.get_average()
                self.reset_data()

            time.sleep(5)


ds = DummySensor()
runComputer = MissionComputer(ds)

info_thread = threading.Thread(target=runComputer.get_mission_computer_info)
load_thread = threading.Thread(target=runComputer.get_mission_computer_load)
sensor_thread = threading.Thread(target=runComputer.get_sensor_data)

info_thread.start()
load_thread.start()
sensor_thread.start()

info_thread.join()
load_thread.join()
sensor_thread.join()
