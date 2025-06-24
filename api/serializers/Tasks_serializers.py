from rest_framework import serializers
from api.models import Task, Guest, User, PredefinedMessage, Room, UserVessel

class TaskCreateSerializer(serializers.ModelSerializer):
    room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all(), required=True)

    class Meta:
        model = Task
        fields = ['predefined_message', 'assigned', 'room']

    def validate(self, data):
        request = self.context['request']
        guest_token = request.headers.get('Guest-Token')
        assigned = data.get('assigned')
        room = data.get('room')
        if not room:
            raise serializers.ValidationError({'room': 'This field is required.'})

        # Solo admin o guest pueden crear tareas
        if request.user and request.user.is_authenticated:
            if request.user.role != 'admin':
                raise serializers.ValidationError('Only admins can create tasks.')
            try:
                creator_vessel = UserVessel.objects.get(user=request.user, is_primary=True, status='active').vessel
            except UserVessel.DoesNotExist:
                raise serializers.ValidationError("Authenticated user does not have an active primary vessel.")
        elif guest_token:
            try:
                guest = Guest.objects.get(guest_token=guest_token)
                creator_vessel = guest.vessel
                data['guest'] = guest
            except Guest.DoesNotExist:
                raise serializers.ValidationError("Invalid guest token.")
        else:
            raise serializers.ValidationError("Authentication or guest_token required.")

        # Solo se puede asignar tareas a workers
        if assigned.role != 'worker':
            raise serializers.ValidationError('Tasks can only be assigned to users with role worker.')

        # Validar que el assigned pertenece al mismo vessel
        try:
            assigned_vessel = UserVessel.objects.get(user=assigned, status='active', vessel=creator_vessel).vessel
        except UserVessel.DoesNotExist:
            raise serializers.ValidationError("Assigned user does not have an active vessel in this crew.")

        data['vessel'] = creator_vessel
        return data

    def create(self, validated_data):
        request = self.context['request']
        guest = validated_data.pop('guest', None)
        vessel = validated_data.pop('vessel')
        room = validated_data.get('room', None)
        creator = None
        if request.user and request.user.is_authenticated:
            creator = request.user
        task = Task.objects.create(
            guest=guest,
            creator=creator,
            vessel=vessel,
            **validated_data
        )
        return task
