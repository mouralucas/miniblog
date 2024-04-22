from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.test import TestCase
from django.urls import reverse

from blog.forms import PostForm, CommentForm
from blog.models import Post


# Create your tests here.
class TestUser(TestCase):
    def test_login(self):
        user = User.objects.create_user(username='testuser', password='123')

        response = self.client.post('/user/login', payload={'username': 'testuser', 'password': '123'})
        self.assertEqual(response.status_code, 200)
