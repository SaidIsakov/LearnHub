import pytest
from apps.courses.models import Course, Lesson, CourseMember, CourseRole
from rest_framework import status


@pytest.mark.django_db
def test_lesson_create(create_user, course, create_api_client, create_teach_assist):
  """
    Создание занятия
  """
  url = '/api/lessons/'
  misha = create_user('misha')

  teach_assist = create_teach_assist(misha, course)

  data = {
    'course': course.id,
    'title': 'Test_lesson',
    'content': 'Test_content',
  }

  client = create_api_client(misha)

  response = client.post(url, data, format='json')

  assert response.status_code == status.HTTP_201_CREATED
  assert response.data['title'] == 'Test_lesson'
  assert response.data['course'] == course.id


def test_lesson_list(create_api_client, course, create_user, create_student, lesson):
  """
    Получаем занятия
  """
  url = '/api/lessons/'
  misha = create_user('misha')

  student = create_student(misha, course)

  client = create_api_client(misha)
  response = client.get(url, format='json')

  assert len(response.data['results']) == 1
  assert response.data['results'][0]['title'] == 'Test_lesson'
