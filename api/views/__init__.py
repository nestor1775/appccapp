from .user_views import RegisterView, UserListView, UserDetailView, UserProfileView, WorkerListView, WorkerDetailView, RegisterDeviceView, CustomLoginView
from .vessel_views import RegisterVesselView, JoinVesselRequestView,  PendingJoinRequestsView, AproveJoinRequestView, VesselListView, VesselDetailView
from .room_views import RoomView, RoomRegisterView, RoomDetailView
from .message_views import PredefinedMessageRegisterView, PredefinedMessageListView, PredefinedMessageDetailView
from .guest_views import GuestRegisterView, GuestListView, GuestDetailView
from .task_views import TaskCreateView, TaskListView, TaskDetailView
from .allauth_views import ResendConfirmationEmailView, ResetPasswordEmailView

__all__ = [
    'RegisterView',
    'UserListView',
    'UserDetailView',
    'UserProfileView',
    'RegisterVesselView',
    'WorkerListView',
    'WorkerDetailView',
    'JoinVesselRequestView',
    'PendingJoinRequestsView',
    'AproveJoinRequestView',
    'RoomView',
    'RoomRegisterView',
    'RoomDetailView',
    'PredefinedMessageRegisterView',
    'PredefinedMessageListView',
    'PredefinedMessageDetailView',
    'GuestRegisterView',
    'GuestListView',
    'GuestDetailView',
    'VesselListView',
    'VesselDetailView',
    'TaskCreateView',
    'TaskListView',
    'TaskDetailView',
    'RegisterDeviceView',
    'CustomLoginView',
    'ResendConfirmationEmailView',
    'ResetPasswordEmailView',
] 