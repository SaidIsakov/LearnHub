import pytest
from apps.courses.models import Lesson, CourseMember, CourseRole
from apps.courses import ai_assistant
from rest_framework import status


@pytest.mark.django_db
def test_ai_answer_quetion(create_user, create_api_client,  monkeypatch, course, create_student, create_instructor, lesson):
  """
    Успешный вопрос к AI
  """
  monkeypatch.setattr('apps.courses.views.ask_ai_about_lesson', lambda lesson_content, question : 'answer')

  alex = create_user('Alex')
  misha = create_user('Misha')

  instructor = create_instructor(alex, course)
  student = create_student(misha, course)

  url = f'/api/lessons/{lesson.id}/ask/'
  client = create_api_client(misha)
  response = client.post(url, {"question": "Объясни тему"})

  assert response.data.get('answer') is not None


@pytest.mark.django_db
def test_quetion_without_text(create_user, create_api_client,  monkeypatch, course, create_student, create_instructor, lesson):
  """
    Вопрос без текста (валидация)
  """

  monkeypatch.setattr('apps.courses.views.ask_ai_about_lesson', lambda lesson_content, question : 'answer')

  alex = create_user('Alex')
  misha = create_user('Misha')

  instructor = create_instructor(alex, course)
  student = create_student(misha, course)

  url = f'/api/lessons/{lesson.id}/ask/'
  client = create_api_client(misha)
  response = client.post(url, {"question": ""})

  assert response.status_code == status.HTTP_400_BAD_REQUEST



@pytest.mark.django_db
def test_user_not_course_member(create_user, create_api_client,  monkeypatch, course, create_instructor, lesson):
  """
    Пользователь не участник курса
  """

  monkeypatch.setattr('apps.courses.views.ask_ai_about_lesson', lambda lesson_content, question : 'answer')

  alex = create_user('Alex')
  misha = create_user('Misha')
  
  instructor = create_instructor(alex, course)

  url = f'/api/lessons/{lesson.id}/ask/'
  client = create_api_client(misha)
  response = client.post(url, {"question": "Test question"})

  assert response.status_code == status.HTTP_404_NOT_FOUND
