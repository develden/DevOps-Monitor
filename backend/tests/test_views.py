from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from ci.models import Pipeline

User = get_user_model()

class PipelineAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="secret")
        self.client.force_authenticate(user=self.user)
        self.pipeline = Pipeline.objects.create(name="Integration Test Pipeline", owner=self.user)

    def test_get_pipeline_list(self):
        url = reverse('pipeline-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # Проверяем, что созданный пайплайн присутствует в ответе
        self.assertTrue(any(item['name'] == self.pipeline.name for item in response.data)) 