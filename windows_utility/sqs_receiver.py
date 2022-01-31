import http.client
import json
import os
import subprocess
from datetime import date, datetime, timezone

import boto3

sqs = boto3.client('sqs')
utility_q_url = os.environ['UTILITY_Q_URL']

def is_after_sunset():
    conn = http.client.HTTPSConnection('api.sunrise-sunset.org')
    # This is only my vague location, you GitHub snooper 🤨
    conn.request('GET', f'/json?lat=47.612324&lng=-122.32084&formatted=0&date={date.today().isoformat()}')
    raw_data = json.loads(conn.getresponse().read())
    sunset_time = datetime.fromisoformat(raw_data['results']['sunset'])
    return datetime.now(timezone.utc) > sunset_time

class SQSReceiver:
    def run(self):
        while True:
            response = sqs.receive_message(
                QueueUrl=utility_q_url,
                MaxNumberOfMessages=10,
                MessageAttributeNames=[
                    'All'
                ],
                WaitTimeSeconds=5
            )
            messages_to_delete = []
            if 'Messages' in response:
                for message in response['Messages']:
                    body = json.loads(message['Body'])
                    print('Received message with body: {}'.format(body))
                    if body['target'] != 'Battlestation':
                        print('Not intended for this system, ignoring...')
                        continue
                    else:
                        print('Intended for this system, processing...')
                    if body['intent'] == 'WindowsAction':
                        if body['action'] == 'ShutDown':
                            os.system(r'shutdown /p')
                        if body['action'] == 'Restart':
                            os.system(r'shutdown /r /t 5')
                        if body['action'] == 'OpenApplication':
                            if body['entity'] == 'Hue Sync':
                                subprocess.Popen(r'C:\Program Files\Hue Sync\HueSync.exe')
                            if body['entity'] == 'Steam':
                                subprocess.Popen(r'C:\Program Files (x86)\Steam\steam.exe')
                            if body['entity'] == 'Battle.net':
                                subprocess.Popen(r'C:\Program Files (x86)\Battle.net\Battle.net.exe')
                            if body['entity'] == 'Discord':
                                subprocess.Popen([r'C:\Users\Antriksh\AppData\Local\Discord\Update.exe', '--processStart', 'Discord.exe'])
                            if body['entity'] == 'Beat Saber':
                                subprocess.Popen(r'D:\Steam Library\steamapps\common\Beat Saber\Beat Saber.exe')
                            if body['entity'] == 'Pistol Whip':
                                subprocess.Popen(r'D:\Steam Library\steamapps\common\Pistol Whip\Pistol Whip.exe')
                        if body['action'] == 'RunScriptAction':
                            if body['entity'] == 'StartCouchGamingMode':
                                # Open Hue Sync if it's past sunset
                                if is_after_sunset():
                                    subprocess.Popen(r'C:\Program Files\Hue Sync\HueSync.exe')
                                # Switch to external display (assumed to be TV)
                                subprocess.Popen(['displayswitch.exe', '/external'])
                                # Open Steam in Big Picture mode, or switch to it
                                subprocess.Popen([r'C:\Program Files (x86)\Steam\steam.exe', '-start', 'steam://open/bigpicture'])
                        if body['action'] == 'RunScriptAction':
                            if body['entity'] == 'StopCouchGamingMode':
                                # Stop Hue Sync if running
                                subprocess.Popen(['taskkill', '/IM', 'HueSync.exe', '/F'])
                                # Switch to main display
                                subprocess.Popen(['displayswitch.exe', '/internal'])
                                # Shut down Steam if running
                                subprocess.Popen([r'C:\Program Files (x86)\Steam\steam.exe', '-shutdown'])
                        messages_to_delete.append({'Id': message['MessageId'], 'ReceiptHandle': message['ReceiptHandle']})
            if messages_to_delete:
                sqs.delete_message_batch(
                    QueueUrl=utility_q_url,
                    Entries=messages_to_delete
                )
