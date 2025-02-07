from rest_framework import serializers
from .models import Pipeline, Build, Notification, CISystemIntegration

class PipelineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pipeline
        fields = '__all__'

class BuildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Build
        fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

class CISystemIntegrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CISystemIntegration
        fields = '__all__' 