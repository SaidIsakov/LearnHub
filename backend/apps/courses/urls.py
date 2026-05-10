from rest_framework import routers
from django.urls import path, include
from apps.courses.views import CourseViewSet

app_name = 'courses'

router = routers.DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')

urlpatterns = [
    path('', include(router.urls))
]

