from django.utils import timezone 
from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    user = models.ForeignKey(User, related_name='owned_projects', on_delete=models.CASCADE)
    collaborators = models.ManyToManyField(User, related_name='collaborating_projects', blank=True)
    created = models.DateTimeField(auto_now_add=True) 
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class File(models.Model):
    project = models.ForeignKey(Project, related_name='files', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default=None)
    content = models.TextField(blank=True)
    current_version = models.ForeignKey('FileVersion', null=True, blank=True, on_delete=models.SET_NULL, related_name='current_for_file')
    created = models.DateTimeField(auto_now_add=True) 
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.pk:
            self.current_version = FileVersion.objects.create(file=self, content=self.content)
        super().save(*args, **kwargs)

class FileVersion(models.Model):
    file = models.ForeignKey(File, related_name='versions', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Version {self.id} of file {self.file.name}"
    

