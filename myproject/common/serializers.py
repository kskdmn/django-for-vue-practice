from rest_framework import serializers
from .models import APILog


class APILogSerializer(serializers.ModelSerializer):
    """Serializer for APILog model"""
    
    class Meta:
        model = APILog
        fields = [
            'id', 'method', 'path', 'query_params', 'request_headers',
            'request_body', 'request_user', 'request_ip', 'response_status_code',
            'response_headers', 'response_body', 'request_timestamp',
            'response_timestamp', 'duration_ms', 'user_agent', 'content_type',
            'created_at'
        ]
        read_only_fields = fields
    
    def to_representation(self, instance):
        """Custom representation to handle JSON fields"""
        data = super().to_representation(instance)
        
        # Parse JSON fields for better readability
        if instance.query_params:
            try:
                data['query_params'] = instance.query_params
            except:
                pass
        
        if instance.request_headers:
            try:
                data['request_headers'] = instance.request_headers
            except:
                pass
        
        if instance.response_headers:
            try:
                data['response_headers'] = instance.response_headers
            except:
                pass
        
        return data


class APILogSummarySerializer(serializers.ModelSerializer):
    """Simplified serializer for log summaries"""
    
    class Meta:
        model = APILog
        fields = [
            'id', 'method', 'path', 'response_status_code',
            'request_timestamp', 'duration_ms', 'request_user'
        ]
        read_only_fields = fields 