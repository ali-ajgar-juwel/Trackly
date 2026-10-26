from django.contrib import admin
from .models import Project,Bug,Comment,Notification
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin): list_display=('name','key','owner','created_at'); search_fields=('name','key')
@admin.register(Bug)
class BugAdmin(admin.ModelAdmin): list_display=('title','project','status','priority','assignee','updated_at'); list_filter=('status','priority','severity'); search_fields=('title','description')
admin.site.register(Comment); admin.site.register(Notification)
