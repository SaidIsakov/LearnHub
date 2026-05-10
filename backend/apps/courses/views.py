from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from apps.courses.serializers import CourseSerializer
from django.db.models import Q
from apps.courses.models import Course


class CourseViewSet(ModelViewSet):
  serializer_class = CourseSerializer
  pagination_class = None

  def perform_create(self, serializer):
    serializer.save(instructor=self.request.user)

  def get_queryset(self):
    user = self.request.user
    return Course.objects.filter(
      Q(instructor=user) | Q(members__user=user)
    ).distinct()
