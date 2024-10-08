from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from projects.models import Project
from django.contrib.auth import authenticate

class AccountsTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.home_url = reverse('home')
        self.verify_email_url = reverse('verify_email')
        self.reset_password_url = reverse('reset_password', kwargs={'email': 'testuser@example.com'})
        
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpassword')
        self.project = Project.objects.create(name='Test Project', user=self.user)

    def test_register_success(self):
        response = self.client.post(self.register_url, {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'newpassword',
            'password2': 'newpassword',
        })
        self.assertEqual(response.status_code, 302)  # Redirect to home
        self.assertTrue(User.objects.filter(username='newuser').exists())
        self.assertRedirects(response, self.home_url)

    def test_register_password_mismatch(self):
        response = self.client.post(self.register_url, {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'newpassword',
            'password2': 'differentpassword',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Passwords do not match")
        self.assertFalse(User.objects.filter(username='newuser').exists())

    def test_register_existing_username(self):
        response = self.client.post(self.register_url, {
            'username': 'testuser',  # Username already exists
            'email': 'newuser@example.com',
            'password1': 'newpassword',
            'password2': 'newpassword',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Username already exists")

    def test_register_existing_email(self):
        response = self.client.post(self.register_url, {
            'username': 'newuser',
            'email': 'testuser@example.com',  # Email already exists
            'password1': 'newpassword',
            'password2': 'newpassword',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Email already in use")

    def test_login_success(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpassword',
        })
        self.assertEqual(response.status_code, 302)  # Redirect to home
        self.assertRedirects(response, self.home_url)

    def test_login_invalid_credentials(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'wrongpassword',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid username or password")

    def test_logout(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)  # Redirect to home
        self.assertRedirects(response, self.home_url)

    def test_home_view_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Project')

    def test_home_view_unauthenticated(self):
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Test Project')

    def test_verify_email_success(self):
        response = self.client.post(self.verify_email_url, {
            'email': 'testuser@example.com',
        })
        self.assertEqual(response.status_code, 302)  # Redirect to reset password
        self.assertRedirects(response, reverse('reset_password', kwargs={'email': 'testuser@example.com'}))

    def test_verify_email_not_found(self):
        response = self.client.post(self.verify_email_url, {
            'email': 'nonexistent@example.com',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Email not found")

    def test_reset_password_success(self):
        response = self.client.post(self.reset_password_url, {
            'password': 'newpassword',
            'password2': 'newpassword',
        })
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertRedirects(response, reverse('login'))

        # Verify password change
        self.user = authenticate(username='testuser', password='newpassword')
        self.assertIsNotNone(self.user)

    def test_reset_password_mismatch(self):
        response = self.client.post(self.reset_password_url, {
            'password': 'newpassword',
            'password2': 'differentpassword',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Passwords do not match")
