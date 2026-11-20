from fastapi import APIRouter
router = APIRouter(prefix="/api")
from Service import service

@router.post("/student")
async def predict(data:dict):
    return service.predict(data)