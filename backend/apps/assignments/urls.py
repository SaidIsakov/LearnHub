from rest_framework import routers
from apps.assignments.views import AssignmentViewSet, SubmissionViewSet
from django.urls import path, include

app_name = 'assignments'

router = routers.DefaultRouter()

router.register(r'assignments', AssignmentViewSet, basename='assignments')
router.register(r'submissions', SubmissionViewSet, basename='submissions')

urlpatterns = [
  path('', include(router.urls))
]

