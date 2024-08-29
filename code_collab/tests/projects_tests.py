from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from projects.models import Project, File, FileVersion

class ProjectFileTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        self.project = Project.objects.create(name='Test Project', description='Test Description', user=self.user)
        self.file = File.objects.create(name='Test File', project=self.project, content='Initial Content')

    def test_create_file(self):
        response = self.client.post(reverse('create_file', args=[self.project.pk]), {'name': 'New File'})
        self.assertEqual(File.objects.count(), 2)
        self.assertRedirects(response, reverse('project_detail', args=[self.project.pk]))

    def test_update_file(self):
        response = self.client.post(reverse('update_file', args=[self.file.pk]), {'name': 'Updated File'})
        self.file.refresh_from_db()
        self.assertEqual(self.file.name, 'Updated File')
        self.assertRedirects(response, reverse('project_detail', args=[self.project.pk]))

    def test_revert_file_to_version(self):
        self.file.content = 'Updated Content'
        self.file.save()

        # Save the version
        version = FileVersion.objects.create(file=self.file, content=self.file.content)

        response = self.client.post(reverse('revert_file', args=[self.file.pk, version.pk]))
        self.file.refresh_from_db()

        self.assertEqual(self.file.content, 'Updated Content')
        self.assertRedirects(response, reverse('file_detail', args=[self.file.pk]))

    def test_file_detail_view(self):
        response = self.client.get(reverse('file_detail', args=[self.file.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.file.name)

    def test_create_project(self):
        response = self.client.post(reverse('create_project'), {'name': 'New Project', 'description': 'Project Description'})
        self.assertEqual(Project.objects.count(), 2)
        self.assertRedirects(response, reverse('project_detail', args=[Project.objects.last().pk]))

    def test_update_project(self):
        response = self.client.post(reverse('update_project', args=[self.project.pk]), {'name': 'Updated Project', 'description': 'Updated Description'})
        self.project.refresh_from_db()
        self.assertEqual(self.project.name, 'Updated Project')
        self.assertRedirects(response, reverse('project_list'))

    def test_delete_project(self):
        response = self.client.post(reverse('delete_project', args=[self.project.pk]))
        self.assertEqual(Project.objects.count(), 0)
        self.assertRedirects(response, reverse('project_list'))

    def test_current_user_project_list(self):
        response = self.client.get(reverse('current_user_project_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.project.name)
