from rest_framework import serializers
from django.contrib.auth import get_user_model
from api.models.vessel import UserVessel, Vessel

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    vessel = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'specialty', 'date_joined', 'last_login', 'vessel', 'profile_url']
        read_only_fields = ['date_joined', 'last_login']

    def get_vessel(self, obj):
        user_vessel = UserVessel.objects.filter(user=obj, status='active').first()
        if not user_vessel:
            return None
        vessel = user_vessel.vessel
        return {
            'id': vessel.id,
            'name': vessel.name,
            'unique_code': vessel.unique_code,
            'guest_pin': vessel.guest_pin,
            'is_primary': user_vessel.is_primary,
            'logo_url': vessel.logo_url,

        }

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True)
    specialty = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role', 'specialty']

    def validate(self, data):
        if data['role'] == 'worker' and not data.get('specialty'):
            raise serializers.ValidationError({'specialty': 'Specialty is required for workers.'})
        return data

    def create(self, validated_data):
        specialty = validated_data.get('specialty', None)
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            role=validated_data['role'],
            specialty=specialty,
        )
        user.set_password(validated_data['password'])
        user.save()
        return user 

