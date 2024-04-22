from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.test import TestCase
from django.urls import reverse

from blog.forms import PostForm, CommentForm
from blog.models import Post


class TestPost(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user_2 = User.objects.create_user(username='testuser_2', password='testpassword_2')

    def test_get_create_post_form(self):
        response = self.client.get('/post/new')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/new_post.html')
        self.assertIn('form', response.context)

        form = response.context['form']
        self.assertIsInstance(form, PostForm)

    def test_create_post_success(self):
        self.client.login(username='testuser', password='testpassword')

        # Check view called
        payload = {'title': 'test', 'content': 'test', 'status': 'published'}
        response = self.client.post('/post/new', data=payload)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url=reverse('blog:feed'))

        # Check redirected view
        redirected_url = response.url
        redirected_response = self.client.get(redirected_url)
        self.assertEqual(redirected_response.status_code, 200)
        self.assertTemplateUsed(redirected_response, 'blog/landing_page.html')
        self.assertIn('posts', redirected_response.context)
        self.assertIn('comment_form', redirected_response.context)
        self.assertIsInstance(redirected_response.context['comment_form'], CommentForm)
        self.assertIsInstance(redirected_response.context['posts'], QuerySet)
        self.assertEqual(1, len(redirected_response.context['posts']))

        # Create a and test if posts length go to two
        payload = {'title': 'test draft', 'content': 'test draft', 'status': 'draft'}
        response = self.client.post('/post/new', data=payload)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url=reverse('blog:feed'))

        redirected_url = response.url
        redirected_response = self.client.get(redirected_url)
        self.assertEqual(2, len(redirected_response.context['posts']))

        # Log out user 1 and log in user two, the length must be one due the draft
        self.client.logout()
        self.client.login(username='testuser_2', password='testpassword_2')

        response = self.client.get('/')
        self.assertEqual(1, len(response.context['posts']))

    def test_create_post_error(self):
        self.client.login(username='testuser', password='testpassword')

        # Call create post without data
        response = self.client.post('/post/new')
        self.assertEqual(response.status_code, 200)

        # In this case, return to form page
        self.assertTemplateUsed(response, 'blog/new_post.html')
        self.assertIn('form', response.context)

        form = response.context['form']
        self.assertGreater(len(form.errors), 0)  # If len(form.errors) there is validation error


class TestComment(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        post = Post.objects.create(title='test', content='test', user=self.user)
        self.post_id = post.id

    def test_comment_success(self):
        self.client.login(username='testuser', password='testpassword')

        # Sent a comment to a post
        payload = {
            'post_id': self.post_id,
            'content': 'This is a test comment'
        }
        response = self.client.post('/post/comment/new', data=payload)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url=reverse('blog:feed'))

        # Check the redirected view
        redirected_url = response.url
        redirected_response = self.client.get(redirected_url)
        self.assertEqual(redirected_response.status_code, 200)