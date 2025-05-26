from pydantic_settings import BaseSettings
import json
from pathlib import Path
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    apiKey: str
    hooksFilePath: str
    schemaFilePath: str
    logFilePath: str
    logMaxSizeMB: int
    dev: bool
    cors: Optional[list] = None

    @classmethod
    def load_from_json(cls, config_path: str = "config.json") -> "Settings":
        with open(config_path, "r") as f:
            config_data = json.load(f)
        return cls(**config_data)

    def validate_schema(self) -> bool:
        try:
            with open(self.schemaFilePath, "r") as f:
                schema = json.load(f)
            
            # Validate that list section exists and is immutable
            if not isinstance(schema, dict):
                logger.error("Schema must be a JSON object")
                return False
                
            if "list" not in schema:
                logger.error("Schema must contain a 'list' section")
                return False
                
            if not isinstance(schema["list"], list):
                logger.error("'list' section must be an array")
                return False
                
            # Validate each user in the list section
            for user in schema["list"]:
                if not isinstance(user, dict):
                    logger.error("Each user in 'list' must be an object")
                    return False
                if "name" not in user or "phone" not in user:
                    logger.error("Each user must have 'name' and 'phone' fields")
                    return False
                    
            return True
        except FileNotFoundError:
            logger.error(f"Schema file not found at {self.schemaFilePath}")
            return False
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON in schema file {self.schemaFilePath}")
            return False
        except Exception as e:
            logger.error(f"Error validating schema: {str(e)}")
            return False

    def ensure_directories(self):
        # Ensure log directory exists
        log_dir = Path(self.logFilePath).parent
        log_dir.mkdir(parents=True, exist_ok=True)

settings = Settings.load_from_json()