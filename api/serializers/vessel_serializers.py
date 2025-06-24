from rest_framework import serializers
from ..models import Vessel, UserVessel

class VesselSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vessel
        fields = ['id', 'name', 'guest_pin', 'logo_url', 'unique_code']
        read_only_fields = ['unique_code']


class UserVesselSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserVessel
        fields = ['id', 'user', 'vessel', 'role_in_vessel', 'status', 'is_primary']
        read_only_fields = ['status']

class RegisterVesselSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vessel
        fields = ['name', 'logo_url']

class JoinVesselSerializer(serializers.ModelSerializer):
    vessel = serializers.SlugRelatedField(
          queryset= Vessel.objects.all(),
          slug_field='unique_code'
     )

    class Meta:
        model= UserVessel
        fields= ['vessel']

    def validate(self,data):
        user= self.context['request'].user
        vessel= data ['vessel']

        if UserVessel.objects.filter(user=user, vessel=vessel).exists():
            raise serializers.ValidationError("You have already submitted a request for this vessel.")
        return data
    