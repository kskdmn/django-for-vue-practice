from rest_framework.serializers import ModelSerializer
from .models import Sample


class SampleSerializer(ModelSerializer):
    class Meta:
        model = Sample
        fields = '__all__'
        read_only_fields = ('id', 'created_by', 'created_at', 'updated_by', 'updated_at')