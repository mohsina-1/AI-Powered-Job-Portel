from django.db import models

# Create yfrom django.db import models
from django.contrib.auth.models import User


class JobSeekerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    education = models.CharField(max_length=200, blank=True)
    skills = models.TextField(blank=True)
    experience = models.TextField(blank=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)

    def __str__(self):
        return self.full_name
class Job(models.Model):
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    skills = models.TextField()
    description = models.TextField()
    employer = models.ForeignKey(
    'EmployerProfile',
    on_delete=models.SET_NULL,
    null=True,
    blank=True
)

    def __str__(self):
        return self.title

class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    def __str__(self):
        return f"{self.user.username} - {self.job.title}"
class EmployerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=200)
    company_email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True)
    company_address = models.TextField(blank=True)

    def __str__(self):
        return self.company_name