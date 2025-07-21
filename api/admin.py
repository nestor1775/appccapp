from django.contrib import admin
from .models import User, Vessel, UserVessel, Room, PredefinedMessage, Guest, Task
from .models.user import Device

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'specialty', 'is_staff', 'device_tokens', 'profile_url')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)

    def device_tokens(self, obj):
        return ', '.join([d.token for d in obj.devices.all()])
    device_tokens.short_description = 'Device Tokens'

@admin.register(Vessel)
class VesselAdmin(admin.ModelAdmin):
    list_display = ('name', 'unique_code', 'guest_pin')
    search_fields = ('name', 'unique_code')
    list_filter = ('name',)

@admin.register(UserVessel)
class UserVesselAdmin(admin.ModelAdmin):
    list_display = ('user', 'vessel', 'role_in_vessel', 'status', 'is_primary')
    list_filter = ('role_in_vessel', 'status', 'is_primary')
    search_fields = ('user__username', 'vessel__name')

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'vessel')
    search_fields = ('name', 'vessel__name')
    list_filter = ('vessel',)

@admin.register(PredefinedMessage)
class PredefinedMessageAdmin(admin.ModelAdmin):
    list_display = ('type', 'vessel')
    search_fields = ('type', 'vessel__name')
    list_filter = ('type', 'vessel')

@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ('name', 'vessel','guest_token')
    search_fields = ('name', 'vessel__name' )
    list_filter = ('vessel',)

# @admin.register(Order)
# class OrderAdmin(admin.ModelAdmin):
#     list_display = ('predefined_message', 'guest', 'date_time', 'room')
#     search_fields = ('predefined_message__type', 'guest__name', 'room__name')
#     list_filter = ('date_time', 'room')

@admin.register(Task)
class Task(admin.ModelAdmin):
    list_display = ('predefined_message', 'status', 'creation_date', 'completion_date', 'assigned', 'creator', 'vessel')
    search_fields = ('predefined_message', 'assigned__username', 'creator__username', 'vessel__name')
    list_filter = ('status', 'vessel')

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('user', 'token', 'platform', 'last_seen')
    search_fields = ('user__username', 'token', 'platform')
    list_filter = ('platform',)

