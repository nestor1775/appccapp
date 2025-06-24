from rest_framework import serializers
from ..models import Room, Vessel

class RoomSerializer(serializers.ModelSerializer):
    # Cambia el campo 'vessel' para que use unique_code en vez de id
    vessel = serializers.SlugRelatedField(
        slug_field='unique_code',
        queryset=Vessel.objects.all()
    )

    class Meta:
        model = Room
        fields = ['id', 'vessel', 'name']

