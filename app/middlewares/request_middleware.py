from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import time
import uuid

class RequestMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())[:8]
        start_time = time.time()

        response = await call_next(request)

        process_time = time.time() - start_time
        response.headers["X-App-Name"] = "device_systems"
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = f"{process_time:.4f}"

        print(f"[{request_id}] {request.method} {request.url.path} -> {response.status_code} ({process_time:.4f}s)")

        return response