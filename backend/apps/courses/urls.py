from rest_framework import routers
from django.urls import path, include
from apps.courses.views import CourseViewSet, LessonViewSet

app_name = 'courses'

router = routers.DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')
router.register(r'lessons', LessonViewSet, basename='lessons')

urlpatterns = [
    path('', include(router.urls))
]

