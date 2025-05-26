# Maintainer Web Hook API

A FastAPI-based backend service for managing maintenance web hooks configuration.

## Features

- Secure API endpoints for managing alerted users
- File-based configuration with JSON schema validation
- Concurrent access control with file locking
- Structured logging with rotation
- Health check endpoint
- API documentation (in development mode)

## Prerequisites

- Python 3.11+
- Docker and Docker Compose (for containerized deployment)

## Configuration

1. Update `config.json` with your settings:
   ```json
   {
     "apiKey": "your-secure-api-key-here",
     "hooksFilePath": "./alerted-users.json",
     "schemaFilePath": "./schema.json",
     "logFilePath": "./logs/app.log",
     "logMaxSizeMB": 50,
     "dev": true
   }
   ```

2. Ensure `schema.json` and `alerted-users.json` exist with the correct structure.

## Running the Application

### Using Docker

1. Build the Docker image:
   ```bash
   docker build -t maintainer-webhook .
   ```

2. Run the container:
   ```bash
   docker run -p 8000:8000 maintainer-webhook
   ```

### Local Development

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

## API Endpoints

### GET /alerted-users
Retrieves the current list of alerted users.

**Headers Required:**
- `X-API-Key`: Your API key

### POST /alerted-users
Updates the list of alerted users.

**Headers Required:**
- `X-API-Key`: Your API key

**Request Body:**
```json
{
  "list": [
    { "name": "Matias Araya", "phone": "+56950997093" }
  ],
  "gerencia": [],
  "lideresdev": [],
  "syt": []
}
```

### GET /health
Health check endpoint that returns the service status.

## Development Mode

When `dev` is set to `true` in `config.json`, the following endpoints are available:
- `/docs`: Swagger UI documentation
- `/redoc`: ReDoc documentation

## Security

- All endpoints require API key authentication
- The `list` section in the JSON configuration is immutable
- File locking prevents concurrent write operations
- Logs are rotated to prevent disk space issues

## Logging

Logs are stored in `./logs/app.log` and rotated when they reach the configured size limit.

## Ejemplos de uso con curl

#### GET /alerted-users

```bash
curl -X GET "http://localhost:8000/alerted-users" -H "x-api-key: your-secure-api-key-here"
```

#### POST /alerted-users

```bash
curl -X POST "http://localhost:8000/alerted-users" \
  -H "Content-Type: application/json" \
  -H "x-api-key: your-secure-api-key-here" \
  -d '{
    "list": [
      { "name": "Matias Araya", "phone": "+56950997093" }
    ],
    "gerencia": [],
    "lideresdev": [],
    "syt": []
  }'
```