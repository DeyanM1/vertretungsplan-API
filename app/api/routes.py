from fastapi import APIRouter
from logic.logic import DomainError, getAvailableClasses, makeRequest
from pydantic import BaseModel

router = APIRouter()

class InputData(BaseModel):
    className: str
    weekNum: str



@router.get("/classes")
def returnClasses():
    return {"result": getAvailableClasses()}

@router.get("/plan")
def returnPlan(data: InputData):
    if not data.weekNum.lstrip("-").isdigit():
        raise DomainError("weekNum must be vaild number", 404)

    if int(data.weekNum) < -3 or int(data.weekNum) > 52:
        raise DomainError("weekNum must be a number ranging from -3 to 52", 404)
    
    result = makeRequest(data.className, data.weekNum)
    
    return {"result": result}
