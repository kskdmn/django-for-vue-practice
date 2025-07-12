import time
from django.utils.deprecation import MiddlewareMixin
from common.models import APILog


class APILoggingMiddleware(MiddlewareMixin):
    """
    Middleware to log all API requests and responses
    """

    def process_request(self, request):
        """Store the start time of the request and capture request body"""
        request.start_time = time.time()

        # Only capture body for API requests
        if request.path.startswith('/api/'):
            # Capture request body before it gets consumed
            request.captured_body = None
            if hasattr(request, 'body') and request.body:
                try:
                    body_str = request.body.decode('utf-8')
                    request.captured_body = body_str[:10000]  # Limit to 10,000 characters
                except (UnicodeDecodeError, AttributeError):
                    pass

    def process_response(self, request, response):
        """Log the API request and response"""
        # Only log API requests (requests to /api/ endpoints)
        if hasattr(request, 'start_time') and request.path.startswith('/api/'):
            duration_ms = (time.time() - request.start_time) * 1000

            # Log asynchronously to avoid blocking the response
            try:
                APILog.log_request(request, response, duration_ms)
            except Exception as e:
                # Don't let logging errors break the response
                print(f"Error in API logging middleware: {e}")

        return response

    def process_exception(self, request, exception):
        """Log exceptions that occur during request processing"""
        if hasattr(request, 'start_time') and request.path.startswith('/api/'):
            duration_ms = (time.time() - request.start_time) * 1000

            # Create a mock response for the exception
            from django.http import HttpResponse
            error_response = HttpResponse(
                content=str(exception),
                status=500,
                content_type='text/plain'
            )

            try:
                APILog.log_request(request, error_response, duration_ms)
            except Exception as e:
                print(f"Error logging API exception: {e}")

        return None
