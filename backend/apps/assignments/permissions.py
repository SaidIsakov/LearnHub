from rest_framework import permissions
from apps.courses.models import CourseMember, Lesson, CourseRole
from apps.assignments.models import Assignment


def get_course_membership(user, obj):
  """Возвращает CourseMember или None"""
  membership = CourseMember.objects.filter(
    user=user,
    is_active=True,
    course=obj
  ).first()
  return membership


class CanCreateAssignment(permissions.BasePermission):
  """
     INSTRUCTOR или TA
  """
  def has_permission(self, request, view):
    lesson_id = request.data.get('lesson')
    if not lesson_id:
      return False
    lesson = Lesson.objects.get(id=lesson_id)
    course = lesson.course

    if not course:
      return False

    membership = get_course_membership(request.user, course)

    if not membership:
      return  False

    return membership.role in [
        CourseRole.INSTRUCTOR,
        CourseRole.TEACHING_ASSISTANT
    ]


class CanSubmitWork(permissions.BasePermission):
  """
    только STUDENT
  """

  def has_permission(self, request, view):
    assignment_id = request.data.get('assignment')
    if not assignment_id:
      return False
    assignment = Assignment.objects.get(id=assignment_id)
    course = assignment.lesson.course

    if not course:
      return False

    membership = get_course_membership(request.user, course)

    if not membership:
      return False

    return membership.role in [
        CourseRole.STUDENT
    ]


class CanReviewSubmission(permissions.BasePermission):
  """
    INSTRUCTOR или TA
  """

  def has_object_permission(self, request, view, obj):

    course = obj.assignment.lesson.course

    if not course:
      return False

    membership = get_course_membership(request.user, course)

    if not membership:
      return False

    return membership.role in [
        CourseRole.INSTRUCTOR,
        CourseRole.TEACHING_ASSISTANT
    ]


