from .user_views import RegisterView, UserListView, UserDetailView, UserProfileView, WorkerListView, WorkerDetailView, RegisterDeviceView
from .vessel_views import RegisterVesselView, JoinVesselRequestView,  PendingJoinRequestsView, AproveJoinRequestView, VesselListView, VesselDetailView
from .room_views import RoomView, RoomRegisterView, RoomDetailView
from .message_views import PredefinedMessageRegisterView, PredefinedMessageListView, PredefinedMessageDetailView
from .guest_views import GuestRegisterView, GuestListView, GuestDetailView
from .task_views import TaskCreateView, TaskListView, TaskDetailView

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
] 