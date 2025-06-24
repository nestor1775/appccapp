from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers.room_serializers import RoomSerializer
from rest_framework.permissions import IsAuthenticated
from ..models import Room, Vessel, UserVessel
from ..permissions import IsAdmin

class RoomView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, unique_code=None):
        # Si unique_code no se usa, obtener vessel del usuario
        if request.user.is_authenticated:
            try:
                vessel = UserVessel.objects.get(user=request.user, is_primary=True, status='active').vessel
            except UserVessel.DoesNotExist:
                return Response({'error': 'No active vessel found.'}, status=status.HTTP_403_FORBIDDEN)
            rooms = Room.objects.filter(vessel=vessel)
        else:
            return Response({'error': 'Authentication required.'}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)
    
class RoomRegisterView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request):
        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RoomDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, room_id):
        try:
            room = Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            return Response({'error': 'Room not found'}, status=status.HTTP_404_NOT_FOUND)
        if request.user.is_authenticated:
            try:
                vessel = UserVessel.objects.get(user=request.user, is_primary=True, status='active').vessel
            except UserVessel.DoesNotExist:
                return Response({'error': 'No active vessel found.'}, status=status.HTTP_403_FORBIDDEN)
            if room.vessel != vessel:
                return Response({'error': 'Not allowed to access this room.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = RoomSerializer(room)
        return Response(serializer.data)

    def put(self, request, room_id):
        try:
            room = Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            return Response({'error': 'Room not found'}, status=status.HTTP_404_NOT_FOUND)
        if request.user.is_authenticated:
            try:
                vessel = UserVessel.objects.get(user=request.user, is_primary=True, status='active').vessel
            except UserVessel.DoesNotExist:
                return Response({'error': 'No active vessel found.'}, status=status.HTTP_403_FORBIDDEN)
            if room.vessel != vessel:
                return Response({'error': 'Not allowed to update this room.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = RoomSerializer(room, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, room_id):
        try:
            room = Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            return Response({'error': 'Room not found'}, status=status.HTTP_404_NOT_FOUND)
        if request.user.is_authenticated:
            try:
                vessel = UserVessel.objects.get(user=request.user, is_primary=True, status='active').vessel
            except UserVessel.DoesNotExist:
                return Response({'error': 'No active vessel found.'}, status=status.HTTP_403_FORBIDDEN)
            if room.vessel != vessel:
                return Response({'error': 'Not allowed to delete this room.'}, status=status.HTTP_403_FORBIDDEN)
        room.delete()
        return Response({'message': 'Room deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
