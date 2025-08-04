from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
async def ExceptionHandlerMiddleware(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        if hasattr(e, "status_code"):
            if e.status_code == 500:
                return JSONResponse(status_code=500, content={"message": "Internal Server Error"})
            else:
                return JSONResponse(status_code=e.status_code, content={"message": e.detail})
        else:
            return JSONResponse(status_code=500, content={"message": "Internal Server Error"})
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=422, content={"message": "Invalid or missing payload"})