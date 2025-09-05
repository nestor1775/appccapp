from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers.user_serializers import RegisterSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated
from ..models import User
from ..models.vessel import UserVessel
from ..permissions import IsAdmin, IsAuthenticatedOrGuestWithToken
from ..models.user import Device
from api.utils.auth_utils import send_confirmation_email
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    #borrar usuario preview
    def delete(self, request):
        user = request.user
        user.delete()
        return Response({'message': 'User deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            # Crear usuario inactivo hasta verificar email
            user = serializer.save(is_active=False)
            
            # Enviar email de verificación
            try:
                send_confirmation_email(request, user)
                
                return Response({
                    'message': 'Usuario registrado exitosamente. Por favor verifica tu email antes de iniciar sesión.',
                    'user_id': user.id
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                # Si falla el email, mantener usuario inactivo
                return Response({
                    'message': 'Usuario registrado exitosamente. Por favor verifica tu email antes de iniciar sesión.',
                    'warning': 'No se pudo enviar el email de verificación.',
                    'user_id': user.id
                }, status=status.HTTP_201_CREATED)
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
    permission_classes = [IsAuthenticatedOrGuestWithToken]

    def get(self, request):
        vessel = None
        
        # Para usuarios autenticados
        if request.user.is_authenticated:
            try:
                vessel = UserVessel.objects.get(user=request.user, status='active').vessel
            except UserVessel.DoesNotExist:
                return Response({'error': 'No active vessel found.'}, status=status.HTTP_403_FORBIDDEN)
        # Para invitados
        elif hasattr(request, 'guest'):
            vessel = request.guest.vessel
        else:
            return Response({'error': 'Authentication or guest token required.'}, status=status.HTTP_401_UNAUTHORIZED)
            
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

class RegisterDeviceView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        token = request.data.get('token')
        platform = request.data.get('platform')
        if not token or not platform:
            return Response({'error': 'Token and platform are required.'}, status=400)
        device, created = Device.objects.update_or_create(
            #user=request.user,
            token=token,
            defaults={
                'user': request.user,
                'platform': platform
                }
        )
        return Response({'message': 'Device registered successfully.'})


class CustomLoginView(APIView):
    def post(self, request):
        email = request.data.get("email")

        password = request.data.get("password")

        if not email or not password:
            return Response({"error": "Username/email are required."}, status=400)

        user = authenticate(email=email, password=password)
        if user is None:
            return Response({"error": "email or password is incorrect."}, status=401)

        if not user.is_active:
            print("User is not active")
            return Response({"error": "Please verify your email before logging in."}, status=401)

        refresh = RefreshToken.for_user(user)
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        })


