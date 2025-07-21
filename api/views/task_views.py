from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers.Tasks_serializers import TaskCreateSerializer, TaskUpdateSerializer
from ..permissions import IsAuthenticatedOrGuestWithToken, IsWorker
from ..models import Task, UserVessel

class TaskCreateView(APIView):
    permission_classes = [IsAuthenticatedOrGuestWithToken]

    def post(self, request):
        serializer = TaskCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            task = serializer.save()
            if task.assigned.role != 'worker':
                return Response({'error': 'Tasks can only be assigned to users with role worker.'}, status=status.HTTP_400_BAD_REQUEST)
            creator_name = task.creator.username if task.creator else (task.guest.name if task.guest else None)
            creator_token = None
            if not task.creator and task.guest:
                creator_token = str(task.guest.guest_token)
            return Response({
                "id": task.id,
                "message": task.predefined_message.content,
                "assigned_to": task.assigned.username,
                "status": task.status,
                "creator": creator_name,
                "creator_guest_token": creator_token,
                "room": task.room.name if task.room else None
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskListView(APIView):
    permission_classes = [IsAuthenticatedOrGuestWithToken]

    def get(self, request):
        if request.user.is_authenticated:
            vessel = UserVessel.objects.filter(user=request.user, status='active').first()
            if not vessel:
                return Response({'error': 'No active vessel found.'}, status=status.HTTP_403_FORBIDDEN)
            vessel = vessel.vessel
            if request.user.role == 'worker':
                tasks = Task.objects.filter(assigned=request.user, vessel=vessel)
            else:
                tasks = Task.objects.filter(vessel=vessel)
        else:
            return Response({'error': 'Authentication required.'}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = TaskCreateSerializer(tasks, many=True)
        return Response(serializer.data)

class TaskDetailView(APIView):
    permission_classes = [IsAuthenticatedOrGuestWithToken]

    def get(self, request, task_id):
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

        if request.user.is_authenticated:
            # Verificamos que el usuario esté activo en el mismo barco que la tarea
            has_access = UserVessel.objects.filter(
                user=request.user,
                vessel=task.vessel,
                status='active'
            ).exists()

            if not has_access:
                return Response({'error': 'Not allowed to access this task.'}, status=status.HTTP_403_FORBIDDEN)

            # Si es worker, solo puede ver tareas asignadas a él
            if request.user.role == 'worker' and task.assigned != request.user:
                return Response({'error': 'Workers can only view their own tasks.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = TaskCreateSerializer(task)
        return Response(serializer.data)

    def put(self, request, task_id):
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
            
        if request.user.is_authenticated:
            has_access = UserVessel.objects.filter(
                user=request.user,
                vessel=task.vessel,
                status='active'
            ).exists()

            if not has_access:
                return Response({'error': 'Not allowed to update this task.'}, status=status.HTTP_403_FORBIDDEN)

            # Allow workers to update only their own tasks
            if request.user.role == 'worker' and task.assigned != request.user:
                return Response({'error': 'You can only update your own tasks.'}, status=status.HTTP_403_FORBIDDEN)
                
        serializer = TaskUpdateSerializer(
            task, 
            data=request.data, 
            partial=True,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, task_id):
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
        if request.user.is_authenticated:
            has_access = UserVessel.objects.filter(
                user=request.user,
                vessel=task.vessel,
                status='active'
            ).exists()

            if not has_access:
                return Response({'error': 'Not allowed to delete this task.'}, status=status.HTTP_403_FORBIDDEN)

            if request.user.role == 'worker':
                return Response({'error': 'Workers cannot delete tasks.'}, status=status.HTTP_403_FORBIDDEN)
        task.delete()
        return Response({'message': 'Task deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
