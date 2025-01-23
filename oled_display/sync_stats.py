from gps3 import gps3

import time
import json
import subprocess
import threading


def get_chrony_stats():
    try:
        lines = subprocess.check_output(["chronyc", "-c", "sources"]).decode()
    except subprocess.CalledProcessError:
        return None, 0.0, 0

    lines = lines.split("\n")
    sync_method = None
    sync_level = 0.0
    ntp_servers = 0
    for line in lines:
        fields = line.split(",")
        if len(fields) < 8:
            continue
        if fields[1] == "*":
            sync_level = float(fields[9]) * 1e6
            if fields[0] == "#":
                sync_method = "pps"
            elif fields[0] == "^":
                sync_method = "ntp"
        if fields[0] == "^" and fields[1] == "+":
            ntp_servers += 1
    return sync_method, sync_level, ntp_servers

class SyncStatsListener:
    def __init__(self):
        self.satellites_in_use = 0
        self.sync_method = None
        self.sync_level = 0.0
        self.ntp_servers = 0
        self.thread = threading.Thread(target=self.run)
        self.thread.daemon = True
        self.thread.start()

    def run(self):
        gps_socket = gps3.GPSDSocket()
        data_stream = gps3.DataStream()
        gps_socket.connect()
        gps_socket.watch()
        for gps_data in gps_socket:
            self.sync_method, self.sync_level, self.ntp_servers = get_chrony_stats()
            if gps_data:
                data_stream.unpack(gps_data)
                gps_data = json.loads(gps_data)
                if gps_data["class"] == "SKY":
                    self.satellites_in_use = sum(1 for sat in gps_data["satellites"] if sat.get("used"))
                    print("Sync method: %s, sync level: %.3fus, satellites in use: %d" % (self.sync_method, self.sync_level, self.satellites_in_use))
            time.sleep(0.1)

