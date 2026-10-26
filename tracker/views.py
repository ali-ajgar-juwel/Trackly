from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q,Count
from django.shortcuts import get_object_or_404,redirect,render
from .models import Project,Bug,Comment,Notification
from .forms import ProjectForm,BugForm,CommentForm
def visible_projects(user): return Project.objects.filter(Q(owner=user)|Q(members=user)).distinct()
@login_required
def dashboard(request):
 projects=visible_projects(request.user); bugs=Bug.objects.filter(project__in=projects).select_related('project','reporter','assignee')
 return render(request,'tracker/dashboard.html',{'project_count':projects.count(),'bug_count':bugs.count(),'open_count':bugs.filter(status='OPEN').count(),'progress_count':bugs.filter(status='IN_PROGRESS').count(),'critical_count':bugs.filter(priority='CRITICAL').exclude(status='CLOSED').count(),'recent_bugs':bugs[:7],'projects':projects[:5],'notifications':Notification.objects.filter(user=request.user,is_read=False)[:5]})
@login_required
def project_list(request): return render(request,'tracker/project_list.html',{'projects':visible_projects(request.user).annotate(bug_count=Count('bugs'))})
@login_required
def project_create(request):
 form=ProjectForm(request.POST or None)
 if request.method=='POST' and form.is_valid():
  project=form.save(commit=False); project.owner=request.user; project.save(); form.save_m2m(); project.members.add(request.user); messages.success(request,'Project created successfully.'); return redirect(project)
 return render(request,'tracker/form.html',{'form':form,'heading':'Create a project','back_url':'project_list'})
@login_required
def project_detail(request,pk):
 project=get_object_or_404(visible_projects(request.user),pk=pk); bugs=project.bugs.select_related('reporter','assignee')
 return render(request,'tracker/project_detail.html',{'project':project,'bugs':bugs})
@login_required
def bug_list(request):
 projects=visible_projects(request.user); bugs=Bug.objects.filter(project__in=projects).select_related('project','reporter','assignee'); q=request.GET.get('q','').strip(); status=request.GET.get('status',''); priority=request.GET.get('priority',''); project_id=request.GET.get('project','')
 if q: bugs=bugs.filter(Q(title__icontains=q)|Q(description__icontains=q)|Q(project__key__icontains=q))
 if status: bugs=bugs.filter(status=status)
 if priority: bugs=bugs.filter(priority=priority)
 if project_id: bugs=bugs.filter(project_id=project_id)
 return render(request,'tracker/bug_list.html',{'bugs':bugs,'projects':projects,'q':q,'selected_status':status,'selected_priority':priority,'selected_project':project_id,'statuses':Bug.Status.choices,'priorities':Bug.Priority.choices})
@login_required
def bug_create(request):
 form=BugForm(request.POST or None,user=request.user)
 if request.method=='POST' and form.is_valid():
  bug=form.save(commit=False); bug.reporter=request.user; bug.save()
  if bug.assignee and bug.assignee!=request.user: Notification.objects.create(user=bug.assignee,bug=bug,message=f'You were assigned: {bug.title}')
  messages.success(request,'Issue created successfully.'); return redirect(bug)
 return render(request,'tracker/form.html',{'form':form,'heading':'Create an issue','back_url':'bug_list'})
@login_required
def bug_detail(request,pk):
 bug=get_object_or_404(Bug.objects.filter(project__in=visible_projects(request.user)).select_related('project','reporter','assignee'),pk=pk); form=CommentForm(request.POST or None)
 if request.method=='POST' and form.is_valid():
  comment=form.save(commit=False); comment.bug=bug; comment.author=request.user; comment.save()
  if bug.reporter!=request.user: Notification.objects.create(user=bug.reporter,bug=bug,message=f'New comment on: {bug.title}')
  messages.success(request,'Comment added.'); return redirect(bug)
 return render(request,'tracker/bug_detail.html',{'bug':bug,'comment_form':form})
@login_required
def bug_edit(request,pk):
 bug=get_object_or_404(Bug.objects.filter(project__in=visible_projects(request.user)),pk=pk)
 if bug.project.owner!=request.user and not request.user.is_superuser: messages.error(request,'Only the project owner can edit this issue.'); return redirect(bug)
 old=bug.assignee; form=BugForm(request.POST or None,instance=bug,user=request.user)
 if request.method=='POST' and form.is_valid():
  updated=form.save()
  if updated.assignee and updated.assignee!=old and updated.assignee!=request.user: Notification.objects.create(user=updated.assignee,bug=updated,message=f'You were assigned: {updated.title}')
  messages.success(request,'Issue updated.'); return redirect(updated)
 return render(request,'tracker/form.html',{'form':form,'heading':'Edit issue','back_url':'bug_list'})
@login_required
def bug_delete(request,pk):
 bug=get_object_or_404(Bug.objects.filter(project__in=visible_projects(request.user)),pk=pk)
 if request.method=='POST' and (bug.project.owner==request.user or request.user.is_superuser): bug.delete(); messages.success(request,'Issue deleted.'); return redirect('bug_list')
 return render(request,'tracker/bug_confirm_delete.html',{'bug':bug})
