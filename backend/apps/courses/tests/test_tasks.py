import pytest
from apps.courses.tasks import notify_new_student, remind_about_deadline
from apps.courses.models import CourseMember, CourseRole, Lesson
from apps.assignments.models import Assignment
from datetime import timedelta
from django.utils import timezone




@pytest.mark.django_db
def test_notify_new_student(user, course, create_user, monkeypatch):
  """
    Проверяем что задача notify_new_student
    выполняется без ошибок
  """

  monkeypatch.setattr('apps.courses.tasks.send_message', lambda chat_id, text: None)

  misha = create_user('Misha')
  alex = create_user('Alex')

  student = CourseMember.objects.create(
    course=course,
    user=misha,
    role=CourseRole.STUDENT
  )
  instructor = CourseMember.objects.create(
    course=course,
    user=alex,
    role=CourseRole.INSTRUCTOR
  )

  result = notify_new_student.delay(course.id, misha.id)
  assert result.successful() == True


@pytest.mark.django_db
def test_remind_about_deadline(create_user, course, monkeypatch):
  """
    Проверяем что задача remind_about_deadline
    находит задания с дедлайном и отправляет напоминания
  """

  monkeypatch.setattr('apps.courses.tasks.send_message', lambda chat_id, text: None)

  alex = create_user('Alex')
  misha = create_user('Misha')
  instructor = CourseMember.objects.create(
    course=course,
    user=alex,
    role=CourseRole.INSTRUCTOR
  )
  student = CourseMember.objects.create(
    course=course,
    user=misha,
    role=CourseRole.STUDENT
  )
  lesson = Lesson.objects.create(
    course=course,
    title = 'Test Task',
    created_by=alex,
  )
  assigment = Assignment.objects.create(
    lesson=lesson,
    deadline=timezone.now() + timedelta(hours=23),
    created_by=alex
    )

  result = remind_about_deadline.delay()

  assert result.successful() == True
