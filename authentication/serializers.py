from rest_framework import serializers
from authentication.enums import EventChoices
from authentication.models import WebhookResponse


class WebhookSerializer(serializers.ModelSerializer):
    # submission_id = serializers.CharField()
    # event_code = serializers.CharField()
    # event_name = serializers.CharField()
    # time_stamp = serializers.CharField()
    # data = serializers.JSONField()


    class Meta:
        model = WebhookResponse
        fields = ["submission_id","event_code","event_name","time_stamp","data"] 
    # def validate(self, attrs):
    #     return super().validate(attrs)

    # def create(self, validated_data):
    #     return super().create(validated_data)