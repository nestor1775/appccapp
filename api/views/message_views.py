from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers.message_serializers import PredefinedMessageSerializer
from rest_framework.permissions import IsAuthenticated
from ..models import PredefinedMessage, Vessel, UserVessel
from ..permissions import IsAdmin

class PredefinedMessageRegisterView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request):
        serializer = PredefinedMessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PredefinedMessageListView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        try:
            vessel = UserVessel.objects.get(user=request.user, is_primary=True, status='active').vessel
        except UserVessel.DoesNotExist:
            return Response({'error': 'No active vessel found.'}, status=status.HTTP_403_FORBIDDEN)
        messages = PredefinedMessage.objects.filter(vessel=vessel)
        serializer = PredefinedMessageSerializer(messages, many=True)
        return Response(serializer.data)

class PredefinedMessageDetailView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request, message_id):
        try:
            message = PredefinedMessage.objects.get(id=message_id)
        except PredefinedMessage.DoesNotExist:
            return Response({'error': 'Message not found'}, status=status.HTTP_404_NOT_FOUND)
        try:
            vessel = UserVessel.objects.get(user=request.user, is_primary=True, status='active').vessel
        except UserVessel.DoesNotExist:
            return Response({'error': 'No active vessel found.'}, status=status.HTTP_403_FORBIDDEN)
        if message.vessel != vessel:
            return Response({'error': 'Not allowed to access this message.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = PredefinedMessageSerializer(message)
        return Response(serializer.data)

    def put(self, request, message_id):
        try:
            message = PredefinedMessage.objects.get(id=message_id)
        except PredefinedMessage.DoesNotExist:
            return Response({'error': 'Message not found'}, status=status.HTTP_404_NOT_FOUND)
        try:
            vessel = UserVessel.objects.get(user=request.user, is_primary=True, status='active').vessel
        except UserVessel.DoesNotExist:
            return Response({'error': 'No active vessel found.'}, status=status.HTTP_403_FORBIDDEN)
        if message.vessel != vessel:
            return Response({'error': 'Not allowed to update this message.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = PredefinedMessageSerializer(message, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, message_id):
        try:
            message = PredefinedMessage.objects.get(id=message_id)
        except PredefinedMessage.DoesNotExist:
            return Response({'error': 'Message not found'}, status=status.HTTP_404_NOT_FOUND)
        try:
            vessel = UserVessel.objects.get(user=request.user, is_primary=True, status='active').vessel
        except UserVessel.DoesNotExist:
            return Response({'error': 'No active vessel found.'}, status=status.HTTP_403_FORBIDDEN)
        if message.vessel != vessel:
            return Response({'error': 'Not allowed to delete this message.'}, status=status.HTTP_403_FORBIDDEN)
        message.delete()
        return Response({'message': 'Message deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)