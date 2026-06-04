import time
import uuid
from fastapi import Request

from starlette.middleware.base import BaseHTTPMiddleware


class LoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        trace_id = str(uuid.uuid4())
        start_time = time.time()

        response = await call_next(request)

        latency_ms = round((time.time() - start_time) * 1000, 2)

        store_id = request.path_params.get("id", "N/A")

        log_data = {
            "trace_id": trace_id,
            "store_id": store_id,
            "endpoint": request.url.path,
            "status_code": response.status_code,
            "latency_ms": latency_ms,
            "event_count": 0
        }

        print(log_data)

        response.headers["X-Trace-ID"] = trace_id

        return response