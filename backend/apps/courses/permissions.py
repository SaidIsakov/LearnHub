from rest_framework.permissions import BasePermission
from apps.courses.models import CourseMember, CourseRole


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
