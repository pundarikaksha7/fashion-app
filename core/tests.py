from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Post, Profile
import uuid

class APITestSuite(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass123")
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_signup(self):
        response = self.client.post('/api/signup/', {
            'username': 'testuser', 'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 201)

    def test_signin(self):
        response = self.client.post('/api/signin/', {
            'username': 'testuser', 'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        response = self.client.post('/api/logout/')
        self.assertEqual(response.status_code, 200)

    def test_token_auth(self):
        response = self.client.post('/api/token-auth/', {
            'username': 'testuser', 'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 200)

    def test_upload_post(self):
        with open('media/post_media/b8115723-2d5a-4a71-ab4f-f26cdf4ad42c.png', 'wb') as f:  # Dummy file
            f.write(b'\x00\x00')
        with open('media/post_media/b8115723-2d5a-4a71-ab4f-f26cdf4ad42c.png', 'rb') as img:
            response = self.client.post('/api/upload/', {
                'caption': 'Test Caption', 'file': img
            })
        self.assertIn(response.status_code, [200, 201])

    def test_api_posts(self):
        response = self.client.get('/api/posts/')
        self.assertEqual(response.status_code, 200)

    def test_profile(self):
        Profile.objects.create(user=self.user)
        response = self.client.get(f'/api/profile/{self.user.username}/')
        self.assertEqual(response.status_code, 200)

    def test_profile_posts(self):
        response = self.client.get(f'/api/profile/{self.user.username}/posts/')
        self.assertEqual(response.status_code, 200)

    def test_saved_posts(self):
        response = self.client.get('/api/saved/')
        self.assertEqual(response.status_code, 200)

    def test_for_you(self):
        Profile.objects.create(user=self.user)
        response = self.client.get('/api/foryou/')
        self.assertEqual(response.status_code, 200)

    def test_search(self):
        response = self.client.get('/api/search/?q=test')
        self.assertEqual(response.status_code, 200)

    def test_add_comment(self):
        post = Post.objects.create(user=self.user.username, caption='Hello world')
        response = self.client.post(f'/api/comment/{post.id}/', {'text': 'Nice post!'})
        self.assertEqual(response.status_code, 201)

    def test_like_post(self):
        post = Post.objects.create(user=self.user.username, caption='Like this')
        response = self.client.post('/api/like/', {'post_id': str(post.id)})
        self.assertEqual(response.status_code, 200)

    def test_save_post(self):
        post = Post.objects.create(user=self.user.username, caption='Save this')
        response = self.client.post(f'/api/save/{post.id}/')
        self.assertEqual(response.status_code, 200)

    def test_follow(self):
        second_user = User.objects.create_user(username="someone", password="pass")
        Profile.objects.create(user=second_user)
        response = self.client.post('/api/follow/', {
            'follower': self.user.username, 'user': 'someone'
        })
        self.assertEqual(response.status_code, 200)

    def test_settings(self):
        response = self.client.post('/api/settings/', {
            'bio': 'New bio',
            'location': 'Earth',
        })
        self.assertIn(response.status_code, [200, 201])

    def test_recommend(self):
        post = Post.objects.create(user=self.user.username, caption='Rec test')
        response = self.client.get(f'/api/recommend/{post.id}/')
        self.assertEqual(response.status_code, 200)

    def test_send_message(self):
        receiver = User.objects.create_user(username="receiver", password="pass")
        response = self.client.post('/api/messages/send/', {
            'receiver': 'receiver',
            'message': 'Hello!'
        })
        self.assertEqual(response.status_code, 200)

    def test_get_conversation(self):
        receiver = User.objects.create_user(username="receiver", password="pass")
        response = self.client.get('/api/messages/receiver/')
        self.assertEqual(response.status_code, 200)

    def test_delete_post(self):
        post = Post.objects.create(user=self.user.username, caption='Del me')
        response = self.client.delete(f'/api/post/delete/{post.id}/')
        self.assertEqual(response.status_code, 204)

    def test_delete_comment(self):
        post = Post.objects.create(user=self.user.username, caption='Post for comment')
        response = self.client.post(f'/api/comment/{post.id}/', {'text': 'Comment to delete'})
        comment_id = response.data.get('id')
        if comment_id:
            delete_resp = self.client.delete(f'/api/comment/delete/{comment_id}/')
            self.assertEqual(delete_resp.status_code, 204)