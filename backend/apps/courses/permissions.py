from rest_framework.permissions import BasePermission
from apps.courses.models import CourseMember, CourseRole, Course, Lesson


def get_course_membership(user, obj):
  """Возвращает CourseMember или None"""
  membership = CourseMember.objects.filter(
    user=user,
    is_active=True,
    course=obj
  ).first()
  return membership

class IsCourseInstructor(BasePermission):
  """
    Только INSTRUCTOR курса
  """
  def has_object_permission(self, request, view, obj):
    membership = get_course_membership(request.user, obj)
    if not membership:
      return False

    return membership.role in [
      CourseRole.INSTRUCTOR
    ]


class IsCourseInstructorOrTA(BasePermission):
  """
    INSTRUCTOR или TEACHING_ASSISTANT
  """
  def has_object_permission(self, request, view, obj):
    membership = get_course_membership(request.user, obj)
    if not membership:
      return False

    return membership.role in [
      CourseRole.INSTRUCTOR,
      CourseRole.TEACHING_ASSISTANT
    ]


class IsCourseMember(BasePermission):
  """
    Любой участник курса
  """
  def has_object_permission(self, request, view, obj):
    membership = get_course_membership(request.user, obj)

    return membership is not None


class CanCreateLesson(BasePermission):
  """
    INSTRUCTOR или TEACHING_ASSISTANT
  """
  def has_permission(self, request, view):
    course_id = request.data.get('course')
    if not course_id:
      return False

    course = Course.objects.get(id=course_id)

    membership = get_course_membership(request.user, course)
    if not membership:
      return False

    return membership.role in [
        CourseRole.INSTRUCTOR,
        CourseRole.TEACHING_ASSISTANT
    ]


class CanEditLesson(BasePermission):
  """
    INSTRUCTOR или TEACHING_ASSISTANT
  """
  def has_object_permission(self, request, view, obj):
    membership = get_course_membership(request.user, obj.course)
    if not membership:
      return False

    return membership.role in [
      CourseRole.INSTRUCTOR,
      CourseRole.TEACHING_ASSISTANT
    ]


class CanDeleteLesson(BasePermission):
  """
    INSTRUCTOR
  """
  def has_object_permission(self, request, view, obj):
    membership = get_course_membership(request.user, obj.course)
    if not membership:
      return False

    return membership.role in [
      CourseRole.INSTRUCTOR,
    ]


class CanAddCourseMember(BasePermission):
  """
    INSTRUCTOR
    TA
  """
  def has_permission(self, request, view):
    course_id = request.data.get('course')
    if not course_id:
      return False

    course = Course.objects.get(id=course_id)

    membership = get_course_membership(request.user, course)
    if not membership:
      return False

    return membership.role in [
        CourseRole.INSTRUCTOR,
        CourseRole.TEACHING_ASSISTANT
    ]


class CanDeleteCourseMember(BasePermission):
  """
    INSTRUCTOR
  """
  def has_object_permission(self, request, view, obj):
    membership = get_course_membership(request.user, obj.course)
    if not membership:
      return False

    return membership.role in [
      CourseRole.INSTRUCTOR,
    ]
