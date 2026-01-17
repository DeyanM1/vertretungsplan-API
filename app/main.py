# main.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from api.routes import router

from logic.logic import DomainError

app = FastAPI()

@app.exception_handler(DomainError)
async def domain_error_handler(request: Request, exc: DomainError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.message}
    )

app.include_router(router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)