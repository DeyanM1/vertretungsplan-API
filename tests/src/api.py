from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

import functions  # type: ignore  # noqa: F401
from functions import DomainError
 
app = FastAPI(title="Vertretungsplan API")


class InputData(BaseModel):
    className: str
    weekNum: str


@app.exception_handler(DomainError)
async def domain_error_handler(request: Request, exc: DomainError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.message}
    )

@app.get("/classes")
def returnClasses():
    return {"result": functions.getAvailableClasses().keys()}

@app.get("/plan")
def returnPlan(data: InputData):
    if not data.weekNum.lstrip("-").isdigit():
        raise HTTPException(status_code=404, detail="weekNum must be a valid number")

    if int(data.weekNum) < -3 or int(data.weekNum) > 52:
        raise HTTPException(status_code=404, detail="weekNum must be a number from -3 to 52")
    
    result = functions.makeRequest(data.className, data.weekNum)
    if result == "E500":
        raise HTTPException(status_code=500, detail="An Error Occured on the server side")
    
    return {"result": result}
