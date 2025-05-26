import json
import time
from pathlib import Path
from typing import Dict, Any
import fcntl
from loguru import logger
from .config import settings
from .models import AlertedUsers, User

class FileLock:
    def __init__(self, filename):
        self.filename = filename
        self.lockfile = f"{filename}.lock"
        self.lock_fd = None

    def __enter__(self):
        self.lock_fd = open(self.lockfile, 'w')
        fcntl.flock(self.lock_fd, fcntl.LOCK_EX)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        fcntl.flock(self.lock_fd, fcntl.LOCK_UN)
        self.lock_fd.close()
        Path(self.lockfile).unlink(missing_ok=True)

class AlertedUsersService:
    def __init__(self):
        self.start_time = time.time()
        self._setup_logging()

    def _setup_logging(self):
        logger.add(
            settings.logFilePath,
            rotation=f"{settings.logMaxSizeMB} MB",
            format="{time} {level} {message}",
            level="INFO"
        )

    def _log_operation(self, operation: str, data: Dict[str, Any]):
        logger.info(f"Operation: {operation}, Data: {json.dumps(data)}")

    def get_alerted_users(self) -> AlertedUsers:
        try:
            with open(settings.hooksFilePath, 'r') as f:
                data = json.load(f)
            self._log_operation("READ", data)
            return AlertedUsers(**data)
        except Exception as e:
            logger.error(f"Error reading alerted users: {str(e)}")
            raise

    def update_alerted_users(self, users: AlertedUsers) -> AlertedUsers:
        try:
            with FileLock(settings.hooksFilePath):
                # Read current data
                with open(settings.hooksFilePath, 'r') as f:
                    current_data = json.load(f)
                
                # Ensure list section remains unchanged
                users_dict = users.dict()
                users_dict['list'] = current_data['list']
                
                # Write updated data
                with open(settings.hooksFilePath, 'w') as f:
                    json.dump(users_dict, f, indent=2)
                
                self._log_operation("WRITE", users_dict)
                return AlertedUsers(**users_dict)
        except Exception as e:
            logger.error(f"Error updating alerted users: {str(e)}")
            raise

    def get_health_status(self) -> Dict[str, Any]:
        try:
            # Check if files are accessible
            Path(settings.hooksFilePath).exists()
            Path(settings.schemaFilePath).exists()
            
            return {
                "status": "ok",
                "uptime": int(time.time() - self.start_time),
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            }
        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            return {
                "status": "error",
                "uptime": int(time.time() - self.start_time),
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            } 