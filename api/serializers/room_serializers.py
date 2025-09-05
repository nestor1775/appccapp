from rest_framework import serializers
from ..models import Room, Vessel

class RoomSerializer(serializers.ModelSerializer):
   
    vessel = serializers.SlugRelatedField(
        slug_field='unique_code',
        queryset=Vessel.objects.all()
    )

    class Meta:
        model = Room
        fields = ['id', 'vessel', 'name']

