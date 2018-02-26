import json, os

import boto3
from awake import wol

battlestation_mac_address = os.environ['DESKTOP_MAC_ADDR']

sqs = boto3.client('sqs')
utility_q_url = os.environ['UTILITY_Q_URL']

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
            if body['intent'] == 'SmartHomeAction' and body['action'] == 'TurnOn' and body['entity'] == 'Battlestation':
                print ("TURNING ON BATTLESTATION")
                wol.send_magic_packet(battlestation_mac_address)
            messages_to_delete.append({'Id':
             message['MessageId'], 'ReceiptHandle': message['ReceiptHandle']})
    if messages_to_delete:
        sqs.delete_message_batch(
            QueueUrl=utility_q_url,
            Entries=messages_to_delete
        )
