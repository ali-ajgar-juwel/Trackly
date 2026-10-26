from rest_framework.routers import DefaultRouter
from .api_views import ProjectViewSet,BugViewSet,CommentViewSet
router=DefaultRouter(); router.register('projects',ProjectViewSet,basename='api-project'); router.register('bugs',BugViewSet,basename='api-bug'); router.register('comments',CommentViewSet,basename='api-comment')
urlpatterns=router.urls
