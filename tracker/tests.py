from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from .models import Project,Bug
class TrackerTests(TestCase):
 def setUp(self):
  U=get_user_model(); self.user=U.objects.create_user(username='tester',password='SafePass123!'); self.project=Project.objects.create(name='Website',key='WEB',owner=self.user); self.project.members.add(self.user); Bug.objects.create(project=self.project,title='Login fails',description='Error on login',reporter=self.user)
 def test_dashboard_login_required(self): self.assertEqual(self.client.get(reverse('dashboard')).status_code,302)
 def test_dashboard_logged_in(self): self.client.login(username='tester',password='SafePass123!'); self.assertEqual(self.client.get(reverse('dashboard')).status_code,200)
 def test_api_requires_auth(self): self.assertEqual(APIClient().get('/api/bugs/').status_code,403)
 def test_api_member_access(self):
  c=APIClient(); c.force_authenticate(self.user); self.assertEqual(c.get('/api/bugs/').status_code,200)
