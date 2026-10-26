from django.conf import settings
from django.db import models
from django.urls import reverse
class Project(models.Model):
 name=models.CharField(max_length=120); key=models.SlugField(max_length=12,unique=True); description=models.TextField(blank=True)
 owner=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='owned_projects'); members=models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True,related_name='tracker_projects'); created_at=models.DateTimeField(auto_now_add=True)
 class Meta: ordering=['-created_at']
 def __str__(self): return f'{self.key} — {self.name}'
 def get_absolute_url(self): return reverse('project_detail',args=[self.pk])
class Bug(models.Model):
 class Status(models.TextChoices): OPEN='OPEN','Open'; IN_PROGRESS='IN_PROGRESS','In progress'; FIXED='FIXED','Fixed'; VERIFIED='VERIFIED','Verified'; CLOSED='CLOSED','Closed'
 class Priority(models.TextChoices): LOW='LOW','Low'; MEDIUM='MEDIUM','Medium'; HIGH='HIGH','High'; CRITICAL='CRITICAL','Critical'
 class Severity(models.TextChoices): MINOR='MINOR','Minor'; NORMAL='NORMAL','Normal'; MAJOR='MAJOR','Major'; BLOCKER='BLOCKER','Blocker'
 project=models.ForeignKey(Project,on_delete=models.CASCADE,related_name='bugs'); title=models.CharField(max_length=180); description=models.TextField(); status=models.CharField(max_length=20,choices=Status.choices,default=Status.OPEN); priority=models.CharField(max_length=12,choices=Priority.choices,default=Priority.MEDIUM); severity=models.CharField(max_length=12,choices=Severity.choices,default=Severity.NORMAL)
 reporter=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='reported_bugs'); assignee=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name='assigned_bugs'); due_date=models.DateField(null=True,blank=True); created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)
 class Meta: ordering=['-updated_at']
 def __str__(self): return f'{self.project.key}-{self.pk}: {self.title}'
 def get_absolute_url(self): return reverse('bug_detail',args=[self.pk])
class Comment(models.Model):
 bug=models.ForeignKey(Bug,on_delete=models.CASCADE,related_name='comments'); author=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE); body=models.TextField(); created_at=models.DateTimeField(auto_now_add=True)
 class Meta: ordering=['created_at']
class Notification(models.Model):
 user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='tracker_notifications'); message=models.CharField(max_length=240); bug=models.ForeignKey(Bug,on_delete=models.CASCADE,null=True,blank=True); is_read=models.BooleanField(default=False); created_at=models.DateTimeField(auto_now_add=True)
 class Meta: ordering=['-created_at']
