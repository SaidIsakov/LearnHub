import pytest
from apps.courses.tasks import notify_new_student, remind_about_deadline
from apps.courses.models import CourseMember, CourseRole, Lesson
from apps.assignments.models import Assignment
from datetime import timedelta
from django.utils import timezone



@pytest.mark.django_db
def test_notify_new_student(user, course, create_user, monkeypatch, create_student, create_instructor):
  """
    Проверяем что задача notify_new_student
    выполняется без ошибок
  """

  monkeypatch.setattr('apps.courses.tasks.send_message', lambda chat_id, text: None)

  misha = create_user('Misha')
  alex = create_user('Alex')

  student = create_student(misha, course)

  instructor = create_instructor(alex, course)

  result = notify_new_student.delay(course.id, misha.id)
  assert result.successful() == True


@pytest.mark.django_db
def test_remind_about_deadline(create_user, course, monkeypatch, create_student, create_instructor, lesson):
  """
    Проверяем что задача remind_about_deadline
    находит задания с дедлайном и отправляет напоминания
  """

  monkeypatch.setattr('apps.courses.tasks.send_message', lambda chat_id, text: None)

  alex = create_user('Alex')
  misha = create_user('Misha')

  instructor = create_instructor(alex, course)
  student = create_student(misha, course)

  assigment = Assignment.objects.create(
    lesson=lesson,
    deadline=timezone.now() + timedelta(hours=23),
    created_by=alex
    )

  result = remind_about_deadline.delay()

  assert result.successful() == True
