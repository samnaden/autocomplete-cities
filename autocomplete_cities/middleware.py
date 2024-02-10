import logging

from pydantic import ValidationError
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.types import Message


async def set_body(request: Request, body: bytes):
    async def receive() -> Message:
        return {"type": "http.request", "body": body}

    request._receive = receive


async def catch_exceptions_middleware(request: Request, call_next):
    caught_exception = None
    req_body = await request.body()
    await set_body(request, req_body)
    try:
        response = await call_next(request)

        if response.status_code == 422:
            # pydantic would ideally raise a ValidationError, but instead they appear to handle it on their end and return a 422
            res_body = b""
            async for chunk in response.body_iterator:
                res_body += chunk
            res_body = res_body.decode()

            raise ValueError(res_body)

        return response
    except (ValidationError,) as e:
        caught_exception = e
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message": {
                    "errors": e.errors(),
                },
            },
        )
    except (ValueError,) as e:
        caught_exception = e
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message": str(e),
            },
        )
    except Exception as e:
        caught_exception = e
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "Internal Server Error",
            },
        )
    finally:
        if caught_exception is not None:
            logging.exception(
                f"problem handling {request.url} with body {req_body}",
                exc_info=caught_exception,
            )
        else:
            logging.info(f"successfully handled {request.url} with body {req_body}")
