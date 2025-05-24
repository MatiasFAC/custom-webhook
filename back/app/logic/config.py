import json
import os

CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')

with open(CONFIG_PATH, 'r') as f:
    _config = json.load(f)

ENV = _config.get('ENV', 'prod')
ALERTED_USERS_FILE = _config.get('ALERTED_USERS_FILE', 'alerted-users.json')
ENDPOINT_BOT_WS = _config.get('ENDPOINT_BOT_WS', 'http://localhost:3008/v1/messages')
ENDPOINT_BOT_WS_BASIC_AUTH_USR = _config.get('ENDPOINT_BOT_WS_BASIC_AUTH_USR', '')
ENDPOINT_BOT_WS_BASIC_AUTH_PWD = _config.get('ENDPOINT_BOT_WS_BASIC_AUTH_PWD', '')
SECURITY_TOKEN = _config.get('SECURITY_TOKEN', 'tu_token_de_seguridad')
