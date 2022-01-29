from enum import Enum, auto
import json
import os

import boto3

class SqsMessageTypes(Enum):
    TURN_ON_BATTLESTATION = auto()
    OPEN_APPLICATION_ON_BATTLESTATION = auto()
    RUN_SCRIPT_ACTION_ON_BATTLESTATION = auto()
    SHUT_DOWN_BATTLESTATION = auto()
    RESTART_BATTLESTATION = auto()

class BattlestationApplications(Enum):
    STEAM = 'Steam'
    BATTLE_NET = 'Battle.net'
    DISCORD = 'Discord'
    BEAT_SABER = 'Beat Saber'
    PISTOL_WHIP = 'Pistol Whip'
    HUE_SYNC = 'Hue Sync'

class BattlestationScriptActions(Enum):
    START_COUCH_GAMING_MODE = 'StartCouchGamingMode'
    STOP_COUCH_GAMING_MODE = 'StopCouchGamingMode'

def generate_alexa_response(output_speech):
    return {
        'version': '1.0',
        'response': {
            'outputSpeech': {
                'type': 'SSML',
                'ssml': output_speech
            }
        }
    }
    
def generate_sqs_message(sqs_message_type, entity=None):
    if sqs_message_type is SqsMessageTypes.TURN_ON_BATTLESTATION:
        message = {
            'intent': 'SmartHomeAction',
            'target': 'RaspberryPi',
            'action': 'TurnOn',
            'entity': 'Battlestation'
        }
        return json.dumps(message)
    if sqs_message_type is SqsMessageTypes.OPEN_APPLICATION_ON_BATTLESTATION:
        if entity is None:
            raise RuntimeError()
        message = {
            'intent': 'WindowsAction',
            'target': 'Battlestation',
            'action': 'OpenApplication',
            'entity': entity
        }
        return json.dumps(message)
    if sqs_message_type is SqsMessageTypes.RUN_SCRIPT_ACTION_ON_BATTLESTATION:
        if entity is None:
            raise RuntimeError()
        message = {
            'intent': 'WindowsAction',
            'target': 'Battlestation',
            'action': 'RunScriptAction',
            'entity': entity
        }
        return json.dumps(message)
    if sqs_message_type is SqsMessageTypes.SHUT_DOWN_BATTLESTATION:
        message = {
            'intent': 'WindowsAction',
            'target': 'Battlestation',
            'action': 'ShutDown'
        }
        return json.dumps(message)
    if sqs_message_type is SqsMessageTypes.RESTART_BATTLESTATION:
        message = {
            'intent': 'WindowsAction',
            'target': 'Battlestation',
            'action': 'Restart'
        }
        return json.dumps(message)

def handle_request(event, context):
    sqs = boto3.resource('sqs')
    utility_q = sqs.get_queue_by_name(QueueName=os.environ['UTILITY_Q_NAME'])
    if event['request']['intent']['name'] == 'TurnOnBattlestation':
        message = generate_sqs_message(SqsMessageTypes.TURN_ON_BATTLESTATION)
        utility_q.send_message(MessageBody=message)
        return generate_alexa_response('<speak><amazon:emotion name="excited" intensity="medium">Battlestation going up!</amazon:emotion></speak>')
    if event['request']['intent']['name'] == 'ShutDownBattlestation':
        message = generate_sqs_message(SqsMessageTypes.SHUT_DOWN_BATTLESTATION)
        utility_q.send_message(MessageBody=message)
        return generate_alexa_response('<speak>Battlestation going down.</speak>')
    if event['request']['intent']['name'] == 'RestartBattlestation':
        message = generate_sqs_message(SqsMessageTypes.RESTART_BATTLESTATION)
        utility_q.send_message(MessageBody=message)
        return generate_alexa_response('<speak>Battlestation coming right back.</speak>')
    if event['request']['intent']['name'] == 'OpenHueSyncOnBattlestation':
        message = generate_sqs_message(SqsMessageTypes.TURN_ON_BATTLESTATION)
        utility_q.send_message(MessageBody=message)
        message = generate_sqs_message(SqsMessageTypes.OPEN_APPLICATION_ON_BATTLESTATION, BattlestationApplications.HUE_SYNC.value)
        utility_q.send_message(MessageBody=message)
        return generate_alexa_response('<speak>Opening Hue Sync</speak>')
    if event['request']['intent']['name'] == 'OpenSteamOnBattlestation':
        message = generate_sqs_message(SqsMessageTypes.TURN_ON_BATTLESTATION)
        utility_q.send_message(MessageBody=message)
        message = generate_sqs_message(SqsMessageTypes.OPEN_APPLICATION_ON_BATTLESTATION, BattlestationApplications.STEAM.value)
        utility_q.send_message(MessageBody=message)
        return generate_alexa_response('<speak><amazon:emotion name="excited" intensity="low">Opening Steam.</amazon:emotion></speak>')
    if event['request']['intent']['name'] == 'OpenBattleNetOnBattlestation':
        message = generate_sqs_message(SqsMessageTypes.TURN_ON_BATTLESTATION)
        utility_q.send_message(MessageBody=message)
        message = generate_sqs_message(SqsMessageTypes.OPEN_APPLICATION_ON_BATTLESTATION, BattlestationApplications.BATTLE_NET.value)
        utility_q.send_message(MessageBody=message)
        return generate_alexa_response('<speak><amazon:emotion name="excited" intensity="medium">Opening Battle dot net.</amazon:emotion></speak>')
    if event['request']['intent']['name'] == 'OpenDiscordOnBattlestation':
        message = generate_sqs_message(SqsMessageTypes.TURN_ON_BATTLESTATION)
        utility_q.send_message(MessageBody=message)
        message = generate_sqs_message(SqsMessageTypes.OPEN_APPLICATION_ON_BATTLESTATION, BattlestationApplications.DISCORD.value)
        utility_q.send_message(MessageBody=message)
        return generate_alexa_response('<speak><amazon:emotion name="excited" intensity="medium">Opening Discord</amazon:emotion></speak>')
    if event['request']['intent']['name'] == 'OpenBeatSaberOnBattlestation':
        message = generate_sqs_message(SqsMessageTypes.TURN_ON_BATTLESTATION)
        utility_q.send_message(MessageBody=message)
        message = generate_sqs_message(SqsMessageTypes.OPEN_APPLICATION_ON_BATTLESTATION, BattlestationApplications.BEAT_SABER.value)
        utility_q.send_message(MessageBody=message)
        return generate_alexa_response('<speak><amazon:emotion name="excited" intensity="medium">Opening Beat Saber</amazon:emotion></speak>')
    if event['request']['intent']['name'] == 'OpenPistolWhipOnBattlestation':
        message = generate_sqs_message(SqsMessageTypes.TURN_ON_BATTLESTATION)
        utility_q.send_message(MessageBody=message)
        message = generate_sqs_message(SqsMessageTypes.OPEN_APPLICATION_ON_BATTLESTATION, BattlestationApplications.PISTOL_WHIP.value)
        utility_q.send_message(MessageBody=message)
        return generate_alexa_response('<speak><amazon:emotion name="excited" intensity="medium">Opening Pistol Whip</amazon:emotion></speak>')
    if event['request']['intent']['name'] == 'RunScriptStartCouchGamingModeOnBattlestation':
        message = generate_sqs_message(SqsMessageTypes.TURN_ON_BATTLESTATION)
        utility_q.send_message(MessageBody=message)
        message = generate_sqs_message(SqsMessageTypes.RUN_SCRIPT_ACTION_ON_BATTLESTATION, BattlestationScriptActions.START_COUCH_GAMING_MODE.value)
        utility_q.send_message(MessageBody=message)
        return generate_alexa_response('<speak><amazon:emotion name="excited" intensity="low">Entering couch gaming mode.</amazon:emotion></speak>')
    if event['request']['intent']['name'] == 'RunScriptStopCouchGamingModeOnBattlestation':
        message = generate_sqs_message(SqsMessageTypes.TURN_ON_BATTLESTATION)
        utility_q.send_message(MessageBody=message)
        message = generate_sqs_message(SqsMessageTypes.RUN_SCRIPT_ACTION_ON_BATTLESTATION, BattlestationScriptActions.STOP_COUCH_GAMING_MODE.value)
        utility_q.send_message(MessageBody=message)
        return generate_alexa_response('<speak>Ending couch gaming mode.</speak>')
