from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from tracker import views
urlpatterns=[path('admin/',admin.site.urls),path('accounts/login/',auth_views.LoginView.as_view(template_name='registration/login.html'),name='login'),path('accounts/logout/',auth_views.LogoutView.as_view(),name='logout'),path('',views.dashboard,name='dashboard'),path('projects/',views.project_list,name='project_list'),path('projects/new/',views.project_create,name='project_create'),path('projects/<int:pk>/',views.project_detail,name='project_detail'),path('bugs/',views.bug_list,name='bug_list'),path('bugs/new/',views.bug_create,name='bug_create'),path('bugs/<int:pk>/',views.bug_detail,name='bug_detail'),path('bugs/<int:pk>/edit/',views.bug_edit,name='bug_edit'),path('bugs/<int:pk>/delete/',views.bug_delete,name='bug_delete'),path('api/',include('tracker.api_urls')),path('api-auth/',include('rest_framework.urls'))]
