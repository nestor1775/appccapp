from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    RegisterView, RegisterVesselView, UserListView, UserDetailView, UserProfileView, WorkerListView, WorkerDetailView,
    JoinVesselRequestView, AproveJoinRequestView, PendingJoinRequestsView,
    RoomView, RoomRegisterView, RoomDetailView,
    PredefinedMessageRegisterView, PredefinedMessageListView, PredefinedMessageDetailView,
    GuestRegisterView, GuestListView, GuestDetailView,
    VesselListView, VesselDetailView,
    TaskCreateView, TaskListView, TaskDetailView
)

urlpatterns = [
    # Auth
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register'),

    # Users
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:user_id>/', UserDetailView.as_view(), name='user-detail'),
    path('users/profile/', UserProfileView.as_view(), name='user-profile'),
    path('workers/', WorkerListView.as_view(), name='worker-list'),
    path('workers/<int:worker_id>/', WorkerDetailView.as_view(), name='worker-detail'),

    # Vessels
    path('vessel/register/', RegisterVesselView.as_view(), name='register_vessel'),
    path('vessels/', VesselListView.as_view(), name='vessel-list'),
    path('vessels/<int:vessel_id>/', VesselDetailView.as_view(), name='vessel-detail'),
    path('vessels/join/', JoinVesselRequestView.as_view(), name='join-vessel'),
    path('vessels/join-request/<int:user_vessel_id>/action/', AproveJoinRequestView.as_view(), name='approve-join-request'),
    path('vessels/<str:vessel_code>/pending-requests/', PendingJoinRequestsView.as_view(), name='pending-join-requests'),

    # Rooms
    path('rooms/', RoomView.as_view(), name='room-list-by-vessel'),  # Considera cambiar a RoomListView si lo implementas
    path('rooms/register/', RoomRegisterView.as_view(), name='register-room'),
    path('rooms/<int:room_id>/', RoomDetailView.as_view(), name='room-detail'),

    # Tasks
    path('tasks/', TaskListView.as_view(), name='task-list'),
    path('tasks/create/', TaskCreateView.as_view(), name='task-create'),
    path('tasks/<int:task_id>/', TaskDetailView.as_view(), name='task-detail'),

    # Predefined Messages
    path('messages/', PredefinedMessageListView.as_view(), name='predefined-message-list'),
    path('message/register/', PredefinedMessageRegisterView.as_view(), name='register-message'),
    path('messages/<int:message_id>/', PredefinedMessageDetailView.as_view(), name='predefined-message-detail'),

    # Guests
    path('guests/', GuestListView.as_view(), name='guest-list'),
    path('guests/register/', GuestRegisterView.as_view(), name='guest-register'),
    path('guests/<int:guest_id>/', GuestDetailView.as_view(), name='guest-detail'),
]