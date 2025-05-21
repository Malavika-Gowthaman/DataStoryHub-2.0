# # exceptions/handlers.py

# from fastapi import Request
# from fastapi.responses import JSONResponse
# from pydantic import ValidationError
# from starlette.exceptions import HTTPException as StarletteHTTPException
# from exceptions.custom import IrrelevantPromptException, InvalidSQLException, RephraseException
# from sqlalchemy.exc import OperationalError, InterfaceError
# import logging

# logger = logging.getLogger(__name__)


# async def pydantic_validation_exception_handler(request: Request, exc: ValidationError):
#     errors = [err['msg'] for err in exc.errors()]
#     return JSONResponse(status_code=400, content={"status": "failed", "errors": errors})


# async def common_exception_handler(request: Request, exc: Exception):
#     logger.exception("Unhandled Exception: %s", str(exc))
#     return JSONResponse(status_code=500, content={"status": "failed", "errors": ["Something went wrong. Please try again later."]})


# async def http_exception_handler(request: Request, exc: StarletteHTTPException):
#     return JSONResponse(status_code=exc.status_code, content={"status": "failed", "errors": [exc.detail]})


# async def irrelevant_prompt_exception_handler(request: Request, exc: IrrelevantPromptException):
#     return JSONResponse(status_code=422, content={"status": "failed", "errors": [exc.msg]})


# async def invalid_sql_exception_handler(request: Request, exc: InvalidSQLException):
#     return JSONResponse(status_code=400, content={"status": "failed", "errors": [exc.msg]})


# async def rephrase_exception_handler(request: Request, exc: RephraseException):
#     return JSONResponse(status_code=422, content={"status": "failed", "errors": [exc.msg]})


# async def operational_error_handler(request: Request, exc: OperationalError):
#     logger.error("Database operational error: %s", str(exc))
#     return JSONResponse(status_code=400, content={"status": "failed", "errors": ["A database error occurred. Try again."]})


# async def interface_error_handler(request: Request, exc: InterfaceError):
#     logger.error("Database interface error: %s", str(exc))
#     return JSONResponse(status_code=400, content={"status": "failed", "errors": ["Connection error with the database."]})

from fastapi import Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from exceptions.custom import IrrelevantPromptException, InvalidSQLException, RephraseException
from sqlalchemy.exc import OperationalError, InterfaceError
import logging

logger = logging.getLogger(__name__)

# FastAPI Pydantic Validation Error Handler
async def pydantic_validation_exception_handler(request: Request, exc: ValidationError):
    errors = [err['msg'] for err in exc.errors()]
    return JSONResponse(status_code=400, content={"status": "failed", "errors": errors})

# Common exception handler for general unhandled errors
async def common_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled Exception: %s", str(exc))
    return JSONResponse(status_code=500, content={"status": "failed", "errors": ["Something went wrong. Please try again later."]})

# HTTPException handler for status-specific exceptions
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(status_code=exc.status_code, content={"status": "failed", "errors": [exc.detail]})

# Custom exception handler for irrelevant prompts
async def irrelevant_prompt_exception_handler(request: Request, exc: IrrelevantPromptException):
    return JSONResponse(status_code=422, content={"status": "failed", "errors": [exc.msg]})

# Custom exception handler for invalid SQL execution
async def invalid_sql_exception_handler(request: Request, exc: InvalidSQLException):
    return JSONResponse(status_code=400, content={"status": "failed", "errors": [exc.msg]})

# Custom exception handler for rephrase requests
async def rephrase_exception_handler(request: Request, exc: RephraseException):
    return JSONResponse(status_code=422, content={"status": "failed", "errors": [exc.msg]})

# Database operational error handler
async def operational_error_handler(request: Request, exc: OperationalError):
    logger.error("Database operational error: %s", str(exc))
    return JSONResponse(status_code=400, content={"status": "failed", "errors": ["A database error occurred. Try again."]})

# Database interface error handler
async def interface_error_handler(request: Request, exc: InterfaceError):
    logger.error("Database interface error: %s", str(exc))
    return JSONResponse(status_code=400, content={"status": "failed", "errors": ["Connection error with the database."]})
