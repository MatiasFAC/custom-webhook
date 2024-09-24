# Event Monitor with FastAPI

## Description

This project implements an intermediary service for Uptime Kuma that helps prevent messages via BuilderBot through the webhook.

## Usage

The service is designed to receive structured events, validate authorization, and send messages to a previously configured list of users. It can be deployed in either development (dev) or production (prod) environments, adjusting its configuration based on the defined environment variables.

### Workflow

1. **Event Reception**: The service exposes an endpoint `/events/` where it receives events in JSON format.
2. **Authorization Validation**: It checks that the request includes a valid security token.
3. **Event Processing**: It extracts the relevant event information and formats it for delivery.
4. **Notification Delivery**: It sends messages to the alerted users via the configured WebSocket endpoint.

## Environment Variables

The service can be configured using the following environment variables:

| Variable | Description | Valor por Default Value |
|-|-|-|
| `ENV` | Defines the service's execution environment. Can be `dev` for development or `prod` for production. | `prod` |
| `ALERTED_USERS_FILE` | Path to the JSON file containing the list of alerted users. | `alerted-users.json` |
| `ENDPOINT_BOT_WS` | WebSocket endpoint URL where alert messages will be sent. | `http://localhost:3008/v1/messages` |
| `ENDPOINT_BOT_WS_BASIC_AUTH_USR` | Username for basic authentication at the WebSocket endpoint (if applicable). | `""` (empty) |
| `ENDPOINT_BOT_WS_BASIC_AUTH_PWD` | Password for basic authentication at the WebSocket endpoint (if applicable). | `""` (empty) |
| `SECURITY_TOKEN` | Security token used to authenticate requests to the `/events/` endpoint. | `tu_token_de_seguridad` |

> **Note:** The environment variables related to basic authentication (`ENDPOINT_BOT_WS_BASIC_AUTH_USR` and `ENDPOINT_BOT_WS_BASIC_AUTH_PWD`) are optional. If not provided, the service will send notifications without authentication.

## Structure of `alerted-users.json`

The `alerted-users.json` file contains lists of users who should receive alerts. It's organized in the mandatory `list` section, and additional lists with custom names can be added.

### JSON Format

```json
{
    "list": [
        {"name": "user1", "phone": "+5622233451"},
        {"name": "user2", "phone": "+5622233452"},
        {"name": "user3", "phone": "+5622233453"}
        
    ],
    "custom1": [
        {"name": "usr_c1", "phone": "+456799983"},
        {"name": "usr_c2", "phone": "+456799984"},
        {"name": "usr_c3", "phone": "+456799985"}
    ],
    "managers": [
        {"name": "manager1", "phone": "+5622233454"},
        {"name": "manager2", "phone": "+5622233455"},
        {"name": "manager3", "phone": "+5622233456"}
    ],
    "developers": [
        {"name": "dev1", "phone": "+5622233457"},
        {"name": "dev2", "phone": "+5622233458"},
        {"name": "dev3", "phone": "+5622233459"}
    ]
}
```
