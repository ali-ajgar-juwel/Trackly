from django.db.models import Q
from rest_framework import permissions,viewsets
from rest_framework.exceptions import PermissionDenied
from .models import Project,Bug,Comment
from .api_serializers import ProjectSerializer,BugSerializer,CommentSerializer
class ProjectViewSet(viewsets.ModelViewSet):
 serializer_class=ProjectSerializer; permission_classes=[permissions.IsAuthenticated]; search_fields=['name','key','description']; ordering_fields=['created_at','name']
 def get_queryset(self): return Project.objects.filter(Q(owner=self.request.user)|Q(members=self.request.user)).distinct()
 def perform_create(self,serializer): serializer.save(owner=self.request.user)
 def perform_update(self,serializer):
  if self.get_object().owner!=self.request.user and not self.request.user.is_superuser: raise PermissionDenied('Only project owners can update projects.')
  serializer.save()
class BugViewSet(viewsets.ModelViewSet):
 serializer_class=BugSerializer; permission_classes=[permissions.IsAuthenticated]; search_fields=['title','description','project__key']; ordering_fields=['created_at','updated_at','priority','due_date']
 def get_queryset(self): return Bug.objects.filter(Q(project__owner=self.request.user)|Q(project__members=self.request.user)).distinct()
 def perform_create(self,serializer):
  project=serializer.validated_data['project']
  if not(project.owner_id==self.request.user.id or project.members.filter(pk=self.request.user.pk).exists()): raise PermissionDenied('You must be a project member to create issues.')
  serializer.save(reporter=self.request.user)
class CommentViewSet(viewsets.ModelViewSet):
 serializer_class=CommentSerializer; permission_classes=[permissions.IsAuthenticated]; http_method_names=['get','post','head','options']
 def get_queryset(self): return Comment.objects.filter(Q(bug__project__owner=self.request.user)|Q(bug__project__members=self.request.user)).distinct()
 def perform_create(self,serializer): serializer.save(author=self.request.user)
