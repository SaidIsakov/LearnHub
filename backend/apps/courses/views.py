from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from apps.courses.serializers import CourseSerializer, LessonSerializer, \
                                     CourseMemberSerializer
from django.db.models import Q
from apps.courses.models import Course, Lesson, CourseMember
from apps.courses.permissions import IsCourseInstructor, \
                  IsCourseInstructorOrTA, IsCourseMember, CanCreateLesson, CanDeleteLesson, CanEditLesson, CanAddCourseMember, CanDeleteCourseMember
from rest_framework.permissions import IsAuthenticated

class CourseViewSet(ModelViewSet):
  serializer_class = CourseSerializer
  pagination_class = None

  def perform_create(self, serializer):
    serializer.save(instructor=self.request.user)

  def get_permissions(self):
    if self.action in ['update', 'partial_update', 'destroy']:
      return [IsCourseInstructor()]
    if self.action == 'create':
      return [IsAuthenticated()]
    return [IsCourseMember()]


  def get_queryset(self):
    user = self.request.user
    return Course.objects.filter(
      Q(instructor=user) | Q(members__user=user)
    ).distinct()


class LessonViewSet(ModelViewSet):
  serializer_class = LessonSerializer

  def perform_create(self, serializer):
    course_id = self.request.data.get('course')
    serializer.save(
        created_by=self.request.user,
        course_id=course_id
    )

  def get_queryset(self):
    return Lesson.objects.filter(
        course__members__user=self.request.user
    ).distinct()

  def get_permissions(self):
    if self.action == 'create':
      return [CanCreateLesson()]
    if self.action in ['update', 'partial_update']:
      return [CanEditLesson()]
    if self.action == 'destroy':
      return [CanDeleteLesson()]
    if self.action in ['list', 'retrieve']:
      return [IsCourseMember()]


class CourseMemberViewSet(ModelViewSet):
  serializer_class = CourseMemberSerializer
  def perform_create(self, serializer):
    course_id = self.request.data.get('course')
    serializer.save(
        invited_by=self.request.user,
        course_id=course_id
    )

  def get_queryset(self):
    return CourseMember.objects.filter(
        course__members__user = self.request.user
    ).distinct()

  def get_permissions(self):
    if self.action == 'create':
      return [CanAddCourseMember()]
    if self.action == 'destroy':
      return [CanDeleteCourseMember()]
    else:
      return [IsCourseMember()]
