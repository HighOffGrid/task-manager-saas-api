import time
from starlette.middleware.base  import BaseHTTPMiddleware
from app.core.logger import logger

class LogMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):
        start_time = time.time()
        response = await call_next(request)

        process_time = time.time() - start_time

        logger.info(
            {
                "method": request.method,
                "path": request.url.path,
                "status": response.status_code,
                "process_time": process_time
            }
        )

        return response