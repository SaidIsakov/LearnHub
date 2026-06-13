from celery import shared_task
from apps.courses.models import Course, CourseRole, CourseMember
from apps.users.models import User
from apps.courses.telegram import send_message
from decouple import config


BOT_TOKEN = config('TELEGRAM_BOT_TOKEN')
CHAT_ID = config('TELEGRAM_CHAT_ID')


@shared_task
def notify_new_student(course_id, student_id):
  course = Course.objects.get(id = course_id)
  student = User.objects.get(id=student_id)
  instructor = CourseMember.objects.get(role=CourseRole.INSTRUCTOR, course=course)

  message = f'На курс {course.title} записался {student.username} - инструктор {instructor.user.username}'

  send_message(
    chat_id=CHAT_ID,
    text=message
  )

