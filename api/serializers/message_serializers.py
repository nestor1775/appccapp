from rest_framework import serializers
from ..models import PredefinedMessage, Vessel

class PredefinedMessageSerializer(serializers.ModelSerializer):
    # Cambia el campo 'vessel' para que use unique_code en vez de id
    vessel = serializers.SlugRelatedField(
        slug_field='unique_code',
        queryset=Vessel.objects.all()
    )

    class Meta:
        model = PredefinedMessage
        fields = ['vessel', 'type', 'content']