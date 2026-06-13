from celery import shared_task
from apps.courses.models import Course, CourseRole, CourseMember
from apps.users.models import User


@shared_task
def notify_new_student(course_id, student_id):
  course = Course.objects.get(id = course_id)
  student = User.objects.get(id=student_id)
  instructor = CourseMember.objects.get(role=CourseRole.INSTRUCTOR, course=course)

  return f'На курс {course.title} записался {student.username} - инструктор {instructor.user.username}'
