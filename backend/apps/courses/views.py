from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from apps.courses.serializers import CourseSerializer, LessonSerializer, \
                                     CourseMemberSerializer
from django.db.models import Q
from apps.courses.models import Course, Lesson, CourseMember, CourseRole, ChatMessage
from apps.courses.permissions import IsCourseInstructor, \
                  IsCourseInstructorOrTA, IsCourseMember, CanCreateLesson, CanDeleteLesson, CanEditLesson, CanAddCourseMember, CanDeleteCourseMember
from rest_framework.permissions import IsAuthenticated
from apps.courses.tasks import notify_new_student
from .filters import CourseFilter, LessonFilter
from drf_spectacular.utils import extend_schema_view, extend_schema
from django.core.cache import cache
from rest_framework.response import Response
from apps.courses.cache import invalidate_courses_cache, invalidate_lessons_cache
from rest_framework.decorators import action
from apps.courses.ai.ai_assistant import ask_ai_about_lesson


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

  def list(self, request, *args, **kwargs):
    cache_key = f'courses_list_user_{request.user.id}_{request.GET.urlencode()}'
    cache_data = cache.get(cache_key)

    if cache_data is not None:
      return Response(cache_data)

    response = super().list(request, *args, **kwargs)
    cache.set(cache_key, response.data, timeout=60*5)
    return response

  def perform_create(self, serializer):
    course = serializer.save(instructor=self.request.user)

    CourseMember.objects.create(
        user=self.request.user,
        course=course,
        role=CourseRole.INSTRUCTOR,
        is_active=True
    )

    invalidate_courses_cache()

  def perform_update(self, serializer):
    super().perform_update(serializer)
    invalidate_courses_cache()

  def perform_destroy(self, instance):
    super().perform_destroy(instance)
    invalidate_courses_cache()

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
    ask=extend_schema(tags=['lessons']),
)
class LessonViewSet(ModelViewSet):
  serializer_class = LessonSerializer
  filterset_class = LessonFilter

  def list(self, request, *args, **kwargs):
    cache_key = f'lessons_list_user_{request.user.id}_{request.GET.urlencode()}'
    cache_data = cache.get(cache_key)

    if cache_data is not None:
      return Response(cache_data)

    response = super().list(request, *args, **kwargs)
    cache.set(cache_key, response.data, timeout=60*5)
    return response

  def perform_create(self, serializer):
    course_id = self.request.data.get('course')
    serializer.save(
        created_by=self.request.user,
        course_id=course_id
    )

    invalidate_lessons_cache()

  def perform_update(self, serializer):
    super().perform_update(serializer)
    invalidate_lessons_cache()

  def perform_destroy(self, instance):
    super().perform_destroy(instance)
    invalidate_lessons_cache()

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
    if self.action in ['list', 'retrieve', 'ask']:
      return [IsCourseMember()]

  @action(detail=True, methods=['POST'])
  def ask(self, request, pk=None):
    lesson = self.get_object()
    question = request.data.get('question')

    if not question:
      return Response({'error': 'Question is required'}, status=400)

    answer = ask_ai_about_lesson(lesson.content, question)

    ChatMessage.objects.create(
        lesson=lesson,
        user=request.user,
        question=question,
        answer=answer
    )

    return Response({'answer': answer})


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
    user_id = self.request.data.get('user')
    serializer.save(
        invited_by=self.request.user,
        course_id=course_id
    )
    notify_new_student.delay(course_id, user_id)

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
