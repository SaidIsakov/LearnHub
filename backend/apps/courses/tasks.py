from celery import shared_task
from apps.courses.models import Course, CourseRole, CourseMember
from apps.users.models import User
from apps.courses.telegram import send_message
from decouple import config
from apps.assignments.models import Assignment
from django.utils import timezone
from datetime import timedelta
import logging


logger = logging.getLogger(__name__)

CHAT_ID = config('TELEGRAM_CHAT_ID')


@shared_task
def notify_new_student(course_id, student_id):
  logger.info(f"Sending notification for course_id = {course_id}, student_id = {student_id}")

  course = Course.objects.get(id = course_id)
  student = User.objects.get(id=student_id)
  instructor = CourseMember.objects.get(role=CourseRole.INSTRUCTOR, course=course)

  message = (
      f'📚 Новый студент!\n'
      f'Курс: {course.title}\n'
      f'Студент: {student.username}'
  )

  send_message(
    chat_id=CHAT_ID,
    text=message
  )
  logger.info(f"The message was sent to the instructor about {student.username} in course {course.title}")

@shared_task
def remind_about_deadline():
  logger.info(f'Sending a message about deadlines to students')

  now = timezone.now()
  time_after_24_hours = now + timedelta(hours=24)
  assignments = Assignment.objects.filter(
      deadline__gte=now,
      deadline__lte=time_after_24_hours
  ).values_list('title', flat=True)

  students = CourseMember.objects.select_related(
    "course", 'user'
  ).filter(
        role=CourseRole.STUDENT,
        course__lessons__assignments__deadline__gte=now,
        course__lessons__assignments__deadline__lte=time_after_24_hours
    )

  logger.info(f'Found {students.count()} students to notify about deadlines')

  message = '📚 Дедлайн через 24 часа:\n' + '\n'.join(list(assignments))

  for student in students:
    send_message(
        chat_id=CHAT_ID,
        text=message
    )
  logger.info(f'Deadline reminders have been sent')
