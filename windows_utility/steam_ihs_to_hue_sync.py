import time
import subprocess
from datetime import datetime
from pathlib import Path

streaming_log_path = 'C:\Program Files (x86)\Steam\logs\streaming_log.txt'
hue_sync_ext_path = 'C:\Program Files\Hue Sync\HueSync.exe'
inactivity_threshold = 60


class OpenHueSyncOnSteamInHomeStreaming:
    def __init__(self):
        self.actionable_diff_last_detected = None
        self.prev_size = None
        self.process = None

    def start_hue_sync(self):
        # TODO: Check file contents
        if self.process is not None:
            return
        print("Starting Hue Sync...")
        self.process = subprocess.Popen(hue_sync_ext_path)

    def stop_hue_sync(self):
        # TODO: Check file contents
        if self.process is not None:
            self.process.terminate()

    def run(self):
        while True:
            time.sleep(5)
            try:
                log_file_size = Path(streaming_log_path).stat().st_size
                if self.prev_size == None:
                    self.prev_size = log_file_size
                elif log_file_size > self.prev_size:
                    self.start_hue_sync()
                    self.actionable_diff_last_detected = datetime.now()
                    self.prev_size = log_file_size
                elif log_file_size == self.prev_size:
                    if self.process is not None and self.actionable_diff_last_detected is not None:
                        if (datetime.now() - self.actionable_diff_last_detected).seconds > inactivity_threshold:
                            self.stop_hue_sync()
                elif log_file_size < self.prev_size:
                    self.prev_size = log_file_size
            except FileNotFoundError:
                continue
