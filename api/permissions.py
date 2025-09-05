from rest_framework import permissions
from .models import Guest

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'

class IsWorker(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'worker'

class IsAdminOrWorker(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and 
            (request.user.role == 'admin' or request.user.role == 'worker')
        )   
    
class IsGuest(permissions.BasePermission):
    def has_permission(self, request, view):
        guest_token = request.headers.get('Guest-Token')
        if not guest_token:
            return False
        try:
            guest = Guest.objects.get(guest_token=guest_token)
            request.guest = guest  
            return True
        except Guest.DoesNotExist:
            return False
        
class IsAuthenticatedOrGuestWithToken(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            return True

        print("--- DEBUGGING GUEST TOKEN ---")
        print(f"Headers: {request.headers}")
        guest_token = request.headers.get('Guest-Token')
        print(f"Token found in header: '{guest_token}'")

        if guest_token:
            try:
                guest = Guest.objects.get(guest_token=guest_token)
                request.guest = guest
                print(f"Guest '{guest.name}' found in DB.")
                print("--- PERMISSION GRANTED ---")
                return True
            except Guest.DoesNotExist:
                print("Guest with this token NOT found in DB.")
                print("--- PERMISSION DENIED ---")
                return False

        print("No guest token in headers.")
        print("--- PERMISSION DENIED ---")
        return False
