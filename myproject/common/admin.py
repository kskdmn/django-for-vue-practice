from django.contrib import admin
from .models import APILog


@admin.register(APILog)
class APILogAdmin(admin.ModelAdmin):
    """Admin interface for API logs"""
    
    list_display = [
        'method', 'path', 'response_status_code', 'request_user',
        'request_timestamp', 'duration_ms', 'request_ip'
    ]
    
    list_filter = [
        'method', 'response_status_code', 'request_user',
        'request_timestamp', 'content_type'
    ]
    
    search_fields = [
        'path', 'request_user__username', 'request_ip', 'user_agent'
    ]
    
    readonly_fields = [
        'method', 'path', 'query_params', 'request_headers', 'request_body',
        'request_user', 'request_ip', 'response_status_code', 'response_headers',
        'response_body', 'request_timestamp', 'response_timestamp',
        'duration_ms', 'user_agent', 'content_type', 'created_at', 'updated_at'
    ]
    
    fieldsets = (
        ('Request Information', {
            'fields': ('method', 'path', 'query_params', 'request_headers', 'request_body')
        }),
        ('User Information', {
            'fields': ('request_user', 'request_ip', 'user_agent')
        }),
        ('Response Information', {
            'fields': ('response_status_code', 'response_headers', 'response_body')
        }),
        ('Timing', {
            'fields': ('request_timestamp', 'response_timestamp', 'duration_ms')
        }),
        ('Metadata', {
            'fields': ('content_type', 'created_at', 'updated_at')
        }),
    )
    
    def has_add_permission(self, request):
        """Disable adding new logs manually"""
        return False
    
    def has_change_permission(self, request, obj=None):
        """Disable editing logs"""
        return False
    
    def has_delete_permission(self, request, obj=None):
        """Allow deleting logs"""
        return True 