from fastapi import FastAPI, Header, HTTPException
from typing import Dict, Any
import os
import json
from loguru import logger
import requests
from requests.auth import HTTPBasicAuth
from pydantic import BaseModel

env = os.environ.get("ENV", "prod")
alerted_users_file = os.getenv("ALERTED_USERS_FILE", "alerted-users.json")
endpoint_bot_ws = os.getenv("ENDPOINT_BOT_WS", "http://localhost:3008/v1/messages")
endpoint_bot_ws_basic_auth_usr = os.getenv("ENDPOINT_BOT_WS_BASIC_AUTH_USR", "")
endpoint_bot_ws_basic_auth_pwd = os.getenv("ENDPOINT_BOT_WS_BASIC_AUTH_PWD", "")
SECURITY_TOKEN = os.getenv("SECURITY_TOKEN", "tu_token_de_seguridad")

enable_endpoint_bot_ws_basic_auth: bool = len(endpoint_bot_ws_basic_auth_usr) > 0 and len(endpoint_bot_ws_basic_auth_pwd) > 0

if env == 'dev':
    app = FastAPI()
else:
    app = FastAPI(docs_url=None, redoc_url=None)

logger.info(f"""
            
Configurations:      
ENV:                        {env}
ALERTED_USERS_FILE:         {alerted_users_file}
ENDPOINT_BOT_WS:            {endpoint_bot_ws}
ENDPOINT_BOT_WS_BASIC_AUTH: {enable_endpoint_bot_ws_basic_auth}  
SECURITY_TOKEN:             ***************
""")

class Heartbeat(BaseModel):
    localDateTime: str
    msg: str

class Monitor(BaseModel):
    name: str
    url: str

class Event(BaseModel):
    heartbeat: Heartbeat
    monitor: Monitor
    msg: str


@app.post("/events/")
async def receive_event(event: Event, authorization: str = Header(...), list2use: str = Header(None)):
    # print headers
    if env == 'dev':
        logger.warning(f"Authorization:    {authorization}")
        logger.warning(f"List to use:      {list2use}")

    if authorization != f"Bearer {SECURITY_TOKEN}":
        raise HTTPException(status_code=403, detail="error")

    if not send_msg_to_ws(event, list2use):
        logger.error("Error sending message to WS")

    return {"msg": "ok"}


def send_msg_to_ws(msg, list2use) -> bool:
    logger.info(f"nombre del servicio:      {msg.monitor.name}")
    logger.info(f"mensaje principal:        {msg.msg}")
    logger.info(f"hora de reporte:          {msg.heartbeat.localDateTime}")
    logger.info(f"url:                      {msg.monitor.url}")
    logger.info(f"mensaje del servicio:     {msg.heartbeat.msg}")
    msg = f"mensaje principal:\n*{msg.msg}*\n\nnombre del servicio:\n*{msg.monitor.name}*\n\nhora de reporte:\n*{msg.heartbeat.localDateTime}*\n\nurl:\n*{msg.monitor.url}*\n\nmensaje del servicio:\n*{msg.heartbeat.msg}*"
    alerted_users: list = None
    if list2use:
        alerted_users = read_alerted_users(list2use)
    else:
        alerted_users = read_alerted_users()

    logger.info(f"Usuarios alertados: {alerted_users}")
    logger.info(alerted_users)

    if not alerted_users:
        logger.warning("No users alerted")
        return False
    
    # send message to ws
    if enable_endpoint_bot_ws_basic_auth: # if basic auth is set
        for user in alerted_users:
            try:
                response = requests.post(endpoint_bot_ws, json={
                    "number": user["phone"],
                    "message": msg
                }, auth=HTTPBasicAuth(endpoint_bot_ws_basic_auth_usr, endpoint_bot_ws_basic_auth_pwd))
                if response.status_code != 200:
                    logger.error(f"Error sending message to WS: {response.text}")
                    return False
            except Exception as e:
                logger.error(f"{user["phone"]} - Error sending message to WS: {e}")
                return False
    else: # no auth
        for user in alerted_users:
            print(endpoint_bot_ws)
            try:
                response = requests.post(endpoint_bot_ws, json={
                    "number": user["phone"],
                    "message": msg
                })
                if response.status_code != 200:
                    logger.error(f"Error sending message to WS: {response.text}")
                    return False
            except Exception as e:
                logger.error(f"{user["phone"]} - Error sending message to WS: {e}")
                return False
    
    return True


def read_alerted_users(list_users="list") -> None:
    if env == 'dev':
        logger.warning(list_users)
    try:
        with open(alerted_users_file, "r") as f:
            return json.load(f)[list_users]
    except Exception as e:
        logger.error(f"Error reading alerted users file: {e}")
        return None
