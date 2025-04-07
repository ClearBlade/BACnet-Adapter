class BACnetSensors:
    def __init__(self):
        print("init bacnet sensors")

    def add_new_sensors_from_device(self, sensors, device_info):
    # first filter out any trendLogs, since we don't need them
        print(device_info)
        filtered_sensors = []