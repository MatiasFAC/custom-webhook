from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class User(BaseModel):
    name: str
    phone: str = Field(..., pattern=r'^\+569\d{8}$')

class AlertedUsers(BaseModel):
    list: List[User]
    gerencia: Optional[List[User]] = []
    lideresdev: Optional[List[User]] = []
    syt: Optional[List[User]] = []

class HealthResponse(BaseModel):
    status: str
    uptime: int
    timestamp: str

class ErrorResponse(BaseModel):
    detail: str 