from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers.message_serializers import PredefinedMessageSerializer
from rest_framework.permissions import IsAuthenticated
from ..models import PredefinedMessage, Vessel, UserVessel
from ..permissions import IsAdmin, IsAuthenticatedOrGuestWithToken, IsAdminOrWorker
from ..models.guest import Guest

class PredefinedMessageRegisterView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request):
        serializer = PredefinedMessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PredefinedMessageListView(APIView):
    permission_classes = [IsAuthenticatedOrGuestWithToken]

    def get(self, request):
        vessel = None
        if request.user.is_authenticated:
            user_vessel = UserVessel.objects.filter(user=request.user, status='active').first()
            if user_vessel:
                vessel = user_vessel.vessel
        elif hasattr(request, 'guest'):
            vessel = request.guest.vessel

        if not vessel:
            return Response({'error': 'No vessel found.'}, status=status.HTTP_403_FORBIDDEN)

        messages = PredefinedMessage.objects.filter(vessel=vessel)
        serializer = PredefinedMessageSerializer(messages, many=True)
        return Response(serializer.data)

class PredefinedMessageDetailView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrWorker]

    def get(self, request, message_id):
        try:
            message = PredefinedMessage.objects.get(id=message_id)
        except PredefinedMessage.DoesNotExist:
            return Response({'error': 'Message not found'}, status=status.HTTP_404_NOT_FOUND)
        try:
            user_vessel = UserVessel.objects.filter(user=request.user, status='active').first()
            vessel = user_vessel.vessel if user_vessel else None
        except UserVessel.DoesNotExist:
            return Response({'error': 'No active vessel found.'}, status=status.HTTP_403_FORBIDDEN)
        if not vessel or message.vessel != vessel:
            return Response({'error': 'Not allowed to access this message.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = PredefinedMessageSerializer(message)
        return Response(serializer.data)

    def put(self, request, message_id):
        try:
            message = PredefinedMessage.objects.get(id=message_id)
        except PredefinedMessage.DoesNotExist:
            return Response({'error': 'Message not found'}, status=status.HTTP_404_NOT_FOUND)
        try:
            user_vessel = UserVessel.objects.filter(user=request.user, status='active').first()
            vessel = user_vessel.vessel if user_vessel else None
        except UserVessel.DoesNotExist:
            return Response({'error': 'No active vessel found.'}, status=status.HTTP_403_FORBIDDEN)
        if not vessel or message.vessel != vessel:
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
            user_vessel = UserVessel.objects.filter(user=request.user, status='active').first()
            vessel = user_vessel.vessel if user_vessel else None
        except UserVessel.DoesNotExist:
            return Response({'error': 'No active vessel found.'}, status=status.HTTP_403_FORBIDDEN)
        if not vessel or message.vessel != vessel:
            return Response({'error': 'Not allowed to delete this message.'}, status=status.HTTP_403_FORBIDDEN)
        message.delete()
        return Response({'message': 'Message deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)