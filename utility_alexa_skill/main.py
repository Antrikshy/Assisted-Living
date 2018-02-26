from enum import Enum, auto
import json

import boto3

class SqsMessageTypes(Enum):
    TURN_ON_BATTLESTATION = auto()

def generate_alexa_response(output_speech):
    return {
        'version': '1.0',
        'response': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': output_speech
            }
        }
    }
    
def generate_sqs_message(sqs_message_type):
    if sqs_message_type is SqsMessageTypes.TURN_ON_BATTLESTATION:
        message = {
            'intent': 'SmartHomeAction',
            'action': 'TurnOn',
            'entity': 'Battlestation'
        }
        return json.dumps(message)

def handle_request(event, context):
    sqs = boto3.resource('sqs')
    utility_q = sqs.get_queue_by_name(QueueName=os.environ['UTILITY_Q_NAME'])

    if event['request']['intent']['name'] == 'TurnOnBattlestation':
        message = generate_sqs_message(SqsMessageTypes.TURN_ON_BATTLESTATION)
        utility_q.send_message(MessageBody=message)
        return generate_alexa_response('Battlestation going up!')
