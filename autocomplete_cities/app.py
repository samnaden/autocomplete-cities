import os
import logging
import uvicorn
from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware

from autocomplete_cities.api.v1_0.api import router as router_v1
from autocomplete_cities.middleware import catch_exceptions_middleware

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", logging.INFO),
    format="%(asctime)s %(levelname)-8.8s %(thread)d %(module)-25.25s:%(lineno)-5.5s %(message)s",
)

app = FastAPI(title="Autocomplete Cities", version="1.0")
app.include_router(router_v1)

app.add_middleware(BaseHTTPMiddleware, dispatch=catch_exceptions_middleware)

if __name__ == "__main__":
    uvicorn.run(app=app, host="0.0.0.0", port=5000, debug=True)  # nosec
