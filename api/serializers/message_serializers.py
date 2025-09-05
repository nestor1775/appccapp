from rest_framework import serializers
from ..models import PredefinedMessage, Vessel

class PredefinedMessageSerializer(serializers.ModelSerializer):
   
    vessel = serializers.SlugRelatedField(
        slug_field='unique_code',
        queryset=Vessel.objects.all()
    )

    class Meta:
        model = PredefinedMessage
        fields = ['id', 'vessel', 'type', 'content']