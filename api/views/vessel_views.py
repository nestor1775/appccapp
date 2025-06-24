from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..serializers import RegisterVesselSerializer, VesselSerializer, UserVesselSerializer, JoinVesselSerializer
from ..serializers.user_serializers import UserSerializer
from ..models import Vessel, UserVessel
from ..permissions import IsAdmin, IsWorker

class RegisterVesselView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request):
        serializer = RegisterVesselSerializer(data=request.data)
        if serializer.is_valid():
            vessel = serializer.save()
            # Crear la relación UserVessel
            UserVessel.objects.create(
                user=request.user,
                vessel=vessel,
                role_in_vessel='admin',
                status='active',
                is_primary=True
            )
            return Response(VesselSerializer(vessel).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    
class JoinVesselRequestView(APIView):
    permission_classes= [IsAuthenticated, IsWorker]

    def post(self, request):
        serializer= JoinVesselSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            UserVessel.objects.create(
                user=request.user,
                vessel=serializer.validated_data['vessel'],
                role_in_vessel='worker',
                status='pending',
                is_primary=False 
            )
            return Response({'message': 'Request sent'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class AproveJoinRequestView(APIView):
    permission_classes= [IsAuthenticated, IsAdmin]

    def post(self, request, user_vessel_id):
        action= request.data.get("action")

        if action not in ["approve", "revoke"]:
            return Response ({"error": "Action must be 'approve' or 'revoke'"}, status=400)
        try:
            user_vessel = UserVessel.objects.get(id=user_vessel_id, status="pending")
        except UserVessel.DoesNotExist:
            return Response({"error": "Request not found or already processed"}, status=404)
        
        if not UserVessel.objects.filter(
            user=request.user,
              vessel=user_vessel.vessel,
                role_in_vessel='admin',
                  status='active'
        ).exists():
            return Response({"error": "You do not have permission to approve this request"}, status=403)

        if action == "approve":
            user_vessel.aprove()  # método del modelo
        else:
            user_vessel.revoke()  # método del modelo

        return Response({"message": f"request {'approve' if action == 'approve' else 'revoke'}"}, status=200)

class PendingJoinRequestsView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request, vessel_code):
        try:
            vessel = Vessel.objects.get(unique_code=vessel_code)
        except Vessel.DoesNotExist:
            return Response({"error": "Vessel not found"}, status=status.HTTP_404_NOT_FOUND)

        pending_requests = UserVessel.objects.filter(vessel=vessel, status="pending")
        data = [
            {
                "id": uv.id,
                "user": UserSerializer(uv.user).data,
                "requested_at": uv.created_at,  
                "is_primary": uv.is_primary,
            }
            for uv in pending_requests
        ]

        return Response(data, status=status.HTTP_200_OK)

class VesselListView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        vessels = Vessel.objects.filter(uservessel__user=request.user, uservessel__status='active').distinct()
        serializer = VesselSerializer(vessels, many=True)
        return Response(serializer.data)

class VesselDetailView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request, vessel_id):
        try:
            vessel = Vessel.objects.get(id=vessel_id)
        except Vessel.DoesNotExist:
            return Response({'error': 'Vessel not found'}, status=status.HTTP_404_NOT_FOUND)
        if not UserVessel.objects.filter(user=request.user, vessel=vessel, status='active').exists():
            return Response({'error': 'Not allowed to access this vessel.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = VesselSerializer(vessel)
        return Response(serializer.data)

    def put(self, request, vessel_id):
        try:
            vessel = Vessel.objects.get(id=vessel_id)
        except Vessel.DoesNotExist:
            return Response({'error': 'Vessel not found'}, status=status.HTTP_404_NOT_FOUND)
        if not UserVessel.objects.filter(user=request.user, vessel=vessel, status='active').exists():
            return Response({'error': 'Not allowed to update this vessel.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = VesselSerializer(vessel, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, vessel_id):
        try:
            vessel = Vessel.objects.get(id=vessel_id)
        except Vessel.DoesNotExist:
            return Response({'error': 'Vessel not found'}, status=status.HTTP_404_NOT_FOUND)
        if not UserVessel.objects.filter(user=request.user, vessel=vessel, status='active').exists():
            return Response({'error': 'Not allowed to delete this vessel.'}, status=status.HTTP_403_FORBIDDEN)
        vessel.delete()
        return Response({'message': 'Vessel deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
