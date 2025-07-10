from django.contrib.auth.models import User
from django.db import models
import json
from django.utils import timezone

from middlewares.current_user import CurrentUserMiddleware


class BaseModel(models.Model):
    created_by = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='%(class)s_created', null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='%(class)s_updated', null=True, blank=True
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        current_user = CurrentUserMiddleware.get_current_user()
        if current_user and current_user.is_authenticated:
            if not self.created_by:
                self.created_by = current_user
            self.updated_by = current_user
        super(BaseModel, self).save(*args, **kwargs)

    def to_dict(self):
        return {k: v for k, v in vars(self).items() if not k.startswith('_')}

    DEFAULT_SERIALIZER_EXCLUDE = ('created_by', 'created_at', 'updated_by', 'updated_at')


class APILog(BaseModel):
    """
    Model to store API request and response logs
    """
    # Request information
    method = models.CharField(max_length=10)
    path = models.CharField(max_length=500)
    query_params = models.TextField(blank=True, null=True)
    request_headers = models.TextField(blank=True, null=True)
    request_body = models.TextField(blank=True, null=True)
    request_user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='api_logs'
    )
    request_ip = models.GenericIPAddressField(null=True, blank=True)
    
    # Response information
    response_status_code = models.IntegerField()
    response_headers = models.TextField(blank=True, null=True)
    response_body = models.TextField(blank=True, null=True)
    
    # Timing information
    request_timestamp = models.DateTimeField()
    response_timestamp = models.DateTimeField()
    duration_ms = models.FloatField(help_text="Request duration in milliseconds")
    
    # Additional metadata
    user_agent = models.CharField(max_length=500, blank=True, null=True)
    content_type = models.CharField(max_length=100, blank=True, null=True)
    
    class Meta:
        db_table = 'api_logs'
        ordering = ['-request_timestamp']
        indexes = [
            models.Index(fields=['method', 'path']),
            models.Index(fields=['request_timestamp']),
            models.Index(fields=['response_status_code']),
            models.Index(fields=['request_user']),
        ]
    
    def __str__(self):
        return f"{self.method} {self.path} - {self.response_status_code} ({self.duration_ms:.2f}ms)"
    
    @classmethod
    def log_request(cls, request, response, duration_ms):
        """
        Create a log entry for an API request/response
        """
        try:
            # Get request data
            request_headers = dict(request.headers)
            # Remove sensitive headers
            sensitive_headers = ['authorization', 'cookie', 'x-csrftoken']
            for header in sensitive_headers:
                request_headers.pop(header.lower(), None)
            
            # Get request body (limit size to avoid database issues)
            request_body = None
            if hasattr(request, 'body') and request.body:
                try:
                    body_str = request.body.decode('utf-8')
                    if len(body_str) <= 10000:  # Limit to 10KB
                        request_body = body_str
                except (UnicodeDecodeError, AttributeError):
                    pass
            
            # Get response data
            response_headers = dict(response.headers)
            response_body = None
            if hasattr(response, 'content') and response.content:
                try:
                    content_str = response.content.decode('utf-8')
                    if len(content_str) <= 10000:  # Limit to 10KB
                        response_body = content_str
                except (UnicodeDecodeError, AttributeError):
                    pass
            
            # Create log entry
            log_entry = cls.objects.create(
                method=request.method,
                path=request.path,
                query_params=json.dumps(dict(request.GET)) if request.GET else None,
                request_headers=json.dumps(request_headers),
                request_body=request_body,
                request_user=request.user if request.user.is_authenticated else None,
                request_ip=cls._get_client_ip(request),
                response_status_code=response.status_code,
                response_headers=json.dumps(response_headers),
                response_body=response_body,
                request_timestamp=timezone.now(),
                response_timestamp=timezone.now(),
                duration_ms=duration_ms,
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                content_type=request.content_type or '',
            )
            return log_entry
        except Exception as e:
            # Log the error but don't break the request
            print(f"Error logging API request: {e}")
            return None
    
    @staticmethod
    def _get_client_ip(request):
        """Extract client IP from request"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
