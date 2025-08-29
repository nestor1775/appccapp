from rest_framework import serializers
from api.models import Task, Guest, User, PredefinedMessage, Room, UserVessel

class TaskCreateSerializer(serializers.ModelSerializer):
    room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all(), required=True)
    
    # Campos de solo lectura para la respuesta
    id = serializers.IntegerField(read_only=True)
    message = serializers.CharField(source='predefined_message.content', read_only=True)
    assigned_username = serializers.CharField(source='assigned.username', read_only=True)
    room_name = serializers.CharField(source='room.name', read_only=True)
    creator_name = serializers.SerializerMethodField(read_only=True)
    creation_date = serializers.DateTimeField(read_only=True)
    completion_date = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Task
        fields = [
            'id',
            'predefined_message', 'message',
            'assigned', 'assigned_username',
            'room', 'room_name',
            'status',
            'creator_name',
            'creation_date',
            'completion_date'
        ]
        
    def get_creator_name(self, obj):
        if obj.creator:
            return obj.creator.username
        elif hasattr(obj, 'guest') and obj.guest:
            return obj.guest.name
        return None

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
                creator_vessel = UserVessel.objects.get(user=request.user, status='active').vessel
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


class TaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['status']
        read_only_fields = ['id', 'predefined_message', 'assigned', 'room', 'creator', 'guest', 'vessel', 'creation_date', 'completion_date']
    
    def update(self, instance, validated_data):
        # Actualiza el estado
        instance.status = validated_data.get('status', instance.status)
        
        # Si se marca como completado y no tiene fecha de finalización, la establecemos
        if instance.status == 'completed' and not instance.completion_date:
            from django.utils import timezone
            instance.completion_date = timezone.now()
            
        instance.save()
        return instance
