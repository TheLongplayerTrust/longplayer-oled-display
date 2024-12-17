from gps3 import gps3

import time
import json
import subprocess
import threading


def get_pps_sync_us():
    lines = subprocess.check_output(["chronyc", "-c", "sources"]).decode()
    lines = lines.split("\n")
    for line in lines:
        fields = line.split(",")
        if len(fields) >= 8 and fields[2] == "PPS":
            sync_level = float(fields[9]) * 1e6
            return sync_level

class SyncStatsListener:
    def __init__(self):
        self.satellites_in_use = 0
        self.pps_sync = 0
        self.thread = threading.Thread(target=self.run)
        self.thread.daemon = True
        self.thread.start()

    def run(self):
        gps_socket = gps3.GPSDSocket()
        data_stream = gps3.DataStream()
        gps_socket.connect()
        gps_socket.watch()
        for gps_data in gps_socket:
            if gps_data:
                data_stream.unpack(gps_data)
                gps_data = json.loads(gps_data)
                if gps_data["class"] == "SKY":
                    self.satellites_in_use = sum(1 for sat in gps_data["satellites"] if sat.get("used"))
                    self.pps_sync = get_pps_sync_us()
                    print("Satellites in use: %d, PPS sync: %.3f" % (self.satellites_in_use, self.pps_sync))

