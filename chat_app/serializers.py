from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, ChatRoom, Message, MessageStatus

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ['user', 'status', 'profile_picture', 'last_seen']

class MessageStatusSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = MessageStatus
        fields = ['user', 'status', 'timestamp']

class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField()
    statuses = MessageStatusSerializer(many=True, read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'room', 'sender', 'content', 'image', 'timestamp', 'statuses']

class ChatRoomSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    # messages field removed for performance. Fetch via message-list endpoint.

    class Meta:
        model = ChatRoom
        fields = ['id', 'name', 'participants', 'is_group_chat']