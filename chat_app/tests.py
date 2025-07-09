from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import ChatRoom, Message, Profile

class AuthTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {'username': 'testuser', 'password': 'testpassword123', 'email': 'test@example.com'}
        self.user = User.objects.create_user(**self.user_data)

    def test_signup(self):
        response = self.client.post('/api/signup/', {'username': 'newuser', 'password': 'newpassword123', 'email': 'new@example.com'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_login(self):
        response = self.client.post('/api/login/', {'username': self.user_data['username'], 'password': self.user_data['password']}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_login_invalid_credentials(self):
        response = self.client.post('/api/login/', {'username': 'wronguser', 'password': 'wrongpassword'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class ChatTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(username='user1', password='password1')
        self.user2 = User.objects.create_user(username='user2', password='password2')
        self.client.force_authenticate(user=self.user1)
        self.room = ChatRoom.objects.create(name='testroom')
        self.room.participants.add(self.user1, self.user2)

    def test_create_chat_room(self):
        response = self.client.post('/api/chats/', {'name': 'newroom', 'participants': [self.user2.id]}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(ChatRoom.objects.filter(name='newroom').exists())

    def test_get_chat_rooms(self):
        response = self.client.get('/api/chats/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'testroom')

    def test_send_message(self):
        response = self.client.post(f'/api/chats/{self.room.id}/messages/', {'content': 'Hello, world!'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Message.objects.count(), 1)
        self.assertEqual(Message.objects.first().content, 'Hello, world!')

    def test_get_messages(self):
        Message.objects.create(room=self.room, sender=self.user1, content='First message')
        response = self.client.get(f'/api/chats/{self.room.id}/messages/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

class ProfileTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='profileuser', password='password')
        self.client.force_authenticate(user=self.user)

    def test_get_profile(self):
        response = self.client.get('/api/profile/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user']['username'], 'profileuser')

    def test_update_profile_status(self):
        response = self.client.patch('/api/profile/', {'status': 'Busy'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.profile.status, 'Busy')