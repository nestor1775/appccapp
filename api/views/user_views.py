from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers.user_serializers import RegisterSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated
from ..models import User
from ..models.vessel import UserVessel
from ..permissions import IsAdmin

class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'user created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserListView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        try:
            vessel = UserVessel.objects.get(user=request.user, is_primary=True, status='active').vessel
        except UserVessel.DoesNotExist:
            return Response({'error': 'No active vessel found.'}, status=status.HTTP_403_FORBIDDEN)
        users = User.objects.filter(uservessel__vessel=vessel, uservessel__status='active').distinct()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

class WorkerListView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        try:
            vessel = UserVessel.objects.get(user=request.user, is_primary=True, status='active').vessel
        except UserVessel.DoesNotExist:
            return Response({'error': 'No active vessel found.'}, status=status.HTTP_403_FORBIDDEN)
        workers = User.objects.filter(role='worker', uservessel__vessel=vessel, uservessel__status='active').distinct()
        serializer = UserSerializer(workers, many=True)
        return Response(serializer.data)

class WorkerDetailView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request, worker_id):
        try:
            vessel = UserVessel.objects.get(user=request.user, is_primary=True, status='active').vessel
        except UserVessel.DoesNotExist:
            return Response({'error': 'No active vessel found.'}, status=status.HTTP_403_FORBIDDEN)
        try:
            worker = User.objects.get(id=worker_id, role='worker', uservessel__vessel=vessel, uservessel__status='active')
        except User.DoesNotExist:
            return Response({'error': 'Worker not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(worker)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        try:
            vessel = UserVessel.objects.get(user=request.user, is_primary=True, status='active').vessel
        except UserVessel.DoesNotExist:
            return Response({'error': 'No active vessel found.'}, status=status.HTTP_403_FORBIDDEN)
        try:
            user = User.objects.get(id=user_id, uservessel__vessel=vessel, uservessel__status='active')
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, user_id):
        try:
            vessel = UserVessel.objects.get(user=request.user, is_primary=True, status='active').vessel
        except UserVessel.DoesNotExist:
            return Response({'error': 'No active vessel found.'}, status=status.HTTP_403_FORBIDDEN)
        try:
            user = User.objects.get(id=user_id, uservessel__vessel=vessel, uservessel__status='active')
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id):
        try:
            vessel = UserVessel.objects.get(user=request.user, is_primary=True, status='active').vessel
        except UserVessel.DoesNotExist:
            return Response({'error': 'No active vessel found.'}, status=status.HTTP_403_FORBIDDEN)
        try:
            user = User.objects.get(id=user_id, uservessel__vessel=vessel, uservessel__status='active')
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        user.delete()
        return Response({'message': 'User deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 