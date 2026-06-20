from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from apps.courses.serializers import CourseSerializer, LessonSerializer, \
                                     CourseMemberSerializer
from django.db.models import Q
from apps.courses.models import Course, Lesson, CourseMember, CourseRole
from apps.courses.permissions import IsCourseInstructor, \
                  IsCourseInstructorOrTA, IsCourseMember, CanCreateLesson, CanDeleteLesson, CanEditLesson, CanAddCourseMember, CanDeleteCourseMember
from rest_framework.permissions import IsAuthenticated
from apps.courses.tasks import notify_new_student
from .filters import CourseFilter, LessonFilter
from drf_spectacular.utils import extend_schema_view, extend_schema


@extend_schema_view(
    list=extend_schema(tags=['courses']),
    create=extend_schema(tags=['courses']),
    retrieve=extend_schema(tags=['courses']),
    update=extend_schema(tags=['courses']),
    partial_update=extend_schema(tags=['courses']),
    destroy=extend_schema(tags=['courses']),
)
class CourseViewSet(ModelViewSet):
  serializer_class = CourseSerializer
  pagination_class = None
  filterset_class = CourseFilter

  def perform_create(self, serializer):
    course = serializer.save(instructor=self.request.user)

    CourseMember.objects.create(
        user=self.request.user,
        course=course,
        role=CourseRole.INSTRUCTOR,
        is_active=True
    )

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


@extend_schema_view(
    list=extend_schema(tags=['lessons']),
    create=extend_schema(tags=['lessons']),
    retrieve=extend_schema(tags=['lessons']),
    update=extend_schema(tags=['lessons']),
    partial_update=extend_schema(tags=['lessons']),
    destroy=extend_schema(tags=['lessons']),
)
class LessonViewSet(ModelViewSet):
  serializer_class = LessonSerializer
  filterset_class = LessonFilter

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


@extend_schema_view(
    list=extend_schema(tags=['members']),
    create=extend_schema(tags=['members']),
    retrieve=extend_schema(tags=['members']),
    update=extend_schema(tags=['members']),
    partial_update=extend_schema(tags=['members']),
    destroy=extend_schema(tags=['members']),
)
class CourseMemberViewSet(ModelViewSet):
  serializer_class = CourseMemberSerializer

  def perform_create(self, serializer):
    course_id = self.request.data.get('course')
    serializer.save(
        invited_by=self.request.user,
        course_id=course_id
    )
    notify_new_student.delay(course_id, self.request.user.id)

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
