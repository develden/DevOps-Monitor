from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Pipeline(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="pipelines")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Build(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('success', 'Success'),
        ('failed', 'Failed'),
    )
    pipeline = models.ForeignKey(Pipeline, on_delete=models.CASCADE, related_name="builds")
    build_number = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    log = models.TextField(blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.pipeline.name} Build #{self.build_number}"

class Notification(models.Model):
    NOTIF_TYPE_CHOICES = (
        ('email', 'Email'),
        ('slack', 'Slack'),
        ('telegram', 'Telegram'),
    )
    pipeline = models.ForeignKey(Pipeline, on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField()
    notif_type = models.CharField(max_length=20, choices=NOTIF_TYPE_CHOICES)
    is_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.pipeline.name} - {self.notif_type}"

class CISystemIntegration(models.Model):
    SYSTEM_TYPE_CHOICES = (
        ('jenkins', 'Jenkins'),
        ('github', 'GitHub Actions'),
        ('gitlab', 'GitLab CI'),
    )
    pipeline = models.ForeignKey(Pipeline, on_delete=models.CASCADE, related_name="integrations")
    system_type = models.CharField(max_length=50, choices=SYSTEM_TYPE_CHOICES)
    api_endpoint = models.URLField()
    auth_token = models.CharField(max_length=255)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.pipeline.name} - {self.system_type}" 