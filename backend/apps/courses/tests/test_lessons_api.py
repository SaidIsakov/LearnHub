import pytest
from apps.courses.models import Course, Lesson, CourseMember, CourseRole
from rest_framework import status


@pytest.mark.django_db
def test_lesson_create(create_user, course, create_api_client):
  """
    Создание занятия
  """
  url = '/api/lessons/'
  misha = create_user('misha')

  member = CourseMember.objects.create(
      user=misha,
      course=course,
      role=CourseRole.TEACHING_ASSISTANT
  )

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


def test_lesson_list(create_api_client, course, create_user):
  """
    Получаем занятия
  """
  url = '/api/lessons/'
  misha = create_user('misha')

  member = CourseMember.objects.create(
      user=misha,
      course=course,
      role=CourseRole.STUDENT
  )

  lesson = Lesson.objects.create(
      course = course,
      title = 'Test_lesson',
      content='Test_content',
      created_by=misha
  )

  client = create_api_client(misha)
  response = client.get(url, format='json')

  assert len(response.data['results']) == 1
  assert response.data['results'][0]['title'] == 'Test_lesson'
