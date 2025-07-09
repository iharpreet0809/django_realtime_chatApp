from django.contrib import admin
from .models import Profile, ChatRoom, Message, MessageStatus

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'last_seen')
    search_fields = ('user__username',)

@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_participants')
    search_fields = ('name',)
    filter_horizontal = ('participants',)

    def get_participants(self, obj):
        return ", ".join([p.username for p in obj.participants.all()])
    get_participants.short_description = 'Participants'

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'room', 'timestamp')
    list_filter = ('room', 'sender')
    search_fields = ('content', 'sender__username', 'room__name')
    date_hierarchy = 'timestamp'

@admin.register(MessageStatus)
class MessageStatusAdmin(admin.ModelAdmin):
    list_display = ('message', 'user', 'status', 'timestamp')
    list_filter = ('status',)
    search_fields = ('user__username', 'message__id')