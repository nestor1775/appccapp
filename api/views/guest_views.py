# views/guest_views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers.guest_serializers import GuestSerializer, GuestRegisterSerializer
from ..models.guest import Guest
from ..models.vessel import UserVessel, Vessel
from rest_framework.permissions import IsAuthenticated
from ..permissions import IsAdmin

class GuestRegisterView(APIView):
    def post(self, request):
        serializer = GuestRegisterSerializer(data=request.data)
        if serializer.is_valid():
            guest = serializer.save()
            return Response({
                "guest_token": str(guest.guest_token),
                "vessel": guest.vessel.name
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GuestListView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        try:
            vessel = UserVessel.objects.get(user=request.user, is_primary=True, status='active').vessel
        except UserVessel.DoesNotExist:
            return Response({'error': 'No active vessel found.'}, status=status.HTTP_403_FORBIDDEN)
        guests = Guest.objects.filter(vessel=vessel)
        serializer = GuestSerializer(guests, many=True)
        return Response(serializer.data)

class GuestDetailView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request, guest_id):
        try:
            guest = Guest.objects.get(id=guest_id)
        except Guest.DoesNotExist:
            return Response({'error': 'Guest not found'}, status=status.HTTP_404_NOT_FOUND)
        
        has_access = UserVessel.objects.filter(user=request.user, vessel=guest.vessel, status='active').exists()
        if not has_access:
            return Response({'error': 'Not allowed to access this guest.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = GuestSerializer(guest)
        return Response(serializer.data)

    def delete(self, request, guest_id):
        try:
            guest = Guest.objects.get(id=guest_id)
        except Guest.DoesNotExist:
            return Response({'error': 'Guest not found'}, status=status.HTTP_404_NOT_FOUND)

        has_access = UserVessel.objects.filter(user=request.user, vessel=guest.vessel, status='active').exists()
        if not has_access:
            return Response({'error': 'Not allowed to delete this guest.'}, status=status.HTTP_403_FORBIDDEN)

        guest.delete()
        return Response({'message': 'Guest deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
