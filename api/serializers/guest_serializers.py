from rest_framework import serializers
from api.models import Guest, Vessel

class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = ['id', 'name', 'vessel', 'guest_token']
        read_only_fields = ['guest_token']

class GuestRegisterSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    guest_pin = serializers.CharField(write_only=True)

    def validate_guest_pin(self, value):
        try:
            vessel = Vessel.objects.get(guest_pin=value)
            return vessel
        except Vessel.DoesNotExist:
            raise serializers.ValidationError("Invalid guest pin.")

    def create(self, validated_data):
        vessel = validated_data.get('guest_pin')  # Ya convertido en Vessel
        name = validated_data.get('name')
        return Guest.objects.create(name=name, vessel=vessel)