from django import forms
from django.db.models import Q
from .models import Project,Bug,Comment
class ProjectForm(forms.ModelForm):
 class Meta: model=Project; fields=['name','key','description','members']; widgets={'description':forms.Textarea(attrs={'rows':3})}
class BugForm(forms.ModelForm):
 class Meta: model=Bug; fields=['project','title','description','status','priority','severity','assignee','due_date']; widgets={'description':forms.Textarea(attrs={'rows':5}),'due_date':forms.DateInput(attrs={'type':'date'})}
 def __init__(self,*args,user=None,**kwargs):
  super().__init__(*args,**kwargs)
  if user and not user.is_superuser: self.fields['project'].queryset=Project.objects.filter(Q(owner=user)|Q(members=user)).distinct()
  self.fields['assignee'].queryset=user.__class__.objects.filter(is_active=True) if user else self.fields['assignee'].queryset
class CommentForm(forms.ModelForm):
 class Meta: model=Comment; fields=['body']; widgets={'body':forms.Textarea(attrs={'rows':3,'placeholder':'Share an update...'})}
