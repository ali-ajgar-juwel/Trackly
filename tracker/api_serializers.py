from rest_framework import serializers
from .models import Project,Bug,Comment
class ProjectSerializer(serializers.ModelSerializer):
 owner_username=serializers.CharField(source='owner.username',read_only=True)
 class Meta: model=Project; fields=['id','name','key','description','owner','owner_username','members','created_at']; read_only_fields=['owner','created_at']
class BugSerializer(serializers.ModelSerializer):
 project_key=serializers.CharField(source='project.key',read_only=True); reporter_username=serializers.CharField(source='reporter.username',read_only=True); assignee_username=serializers.CharField(source='assignee.username',read_only=True)
 class Meta: model=Bug; fields=['id','project','project_key','title','description','status','priority','severity','reporter','reporter_username','assignee','assignee_username','due_date','created_at','updated_at']; read_only_fields=['reporter','created_at','updated_at']
class CommentSerializer(serializers.ModelSerializer):
 author_username=serializers.CharField(source='author.username',read_only=True)
 class Meta: model=Comment; fields=['id','bug','author','author_username','body','created_at']; read_only_fields=['author','created_at']
