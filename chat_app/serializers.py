from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, ChatRoom, Message, MessageStatus

class UserSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(max_length=20, required=False, allow_blank=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password', 'phone_number']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        phone_number = validated_data.pop('phone_number', None)
        user = User.objects.create_user(**validated_data)
        
        # Force refresh to ensure signals have completed
        user.refresh_from_db()
        
        # Create or update profile with phone number
        if phone_number:
            from .models import Profile
            profile, created = Profile.objects.get_or_create(user=user)
            profile.phone_number = phone_number
            profile.save()
        
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