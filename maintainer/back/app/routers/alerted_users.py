from fastapi import APIRouter, Depends, HTTPException, Header
from typing import Optional
from ..models import AlertedUsers, ErrorResponse
from ..services import AlertedUsersService
from ..config import settings

router = APIRouter()
service = AlertedUsersService()

async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != settings.apiKey:
        raise HTTPException(
            status_code=401,
            detail="Invalid API key"
        )
    return x_api_key

@router.get(
    "/alerted-users",
    response_model=AlertedUsers,
    responses={401: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
    dependencies=[Depends(verify_api_key)]
)
async def get_alerted_users():
    try:
        return service.get_alerted_users()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post(
    "/alerted-users",
    response_model=AlertedUsers,
    responses={401: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
    dependencies=[Depends(verify_api_key)]
)
async def update_alerted_users(users: AlertedUsers):
    try:
        return service.update_alerted_users(users)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get(
    "/health",
    response_model=dict,
    responses={500: {"model": ErrorResponse}}
)
async def health_check():
    try:
        return service.get_health_status()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))