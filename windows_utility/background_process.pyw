# To be run using the "pythonw" command on Windows

from threading import Thread

from steam_ihs_to_hue_sync import OpenHueSyncOnSteamInHomeStreaming
from sqs_receiver import SQSReceiver

if __name__ == '__main__':
    for driver in [OpenHueSyncOnSteamInHomeStreaming().run, SQSReceiver().run]:
        thread = Thread(target=driver)
        thread.start()
