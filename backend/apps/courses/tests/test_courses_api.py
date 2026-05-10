from apps.courses.models import Course
from rest_framework import status
import pytest

@pytest.mark.django_db
def test_course_create(user, auth_client):
  """
    Создает курс
  """

  url = '/api/courses/'
  data = {
    'title' : 'Test_Case',
    'description': 'Test_Desc'
  }

  response = auth_client.post(url, data, format="json")
  assert response.status_code == status.HTTP_201_CREATED
  assert response.data["title"] == 'Test_Case'

  course = Course.objects.get(title='Test_Case')
  assert course.description == 'Test_Desc'
  assert course.instructor == user


@pytest.mark.django_db
def test_course_list(user, auth_client, course):
  """
    Вывод спика задач
  """
  url = '/api/courses/'
  response = auth_client.get(url)

  assert len(response.data) == 1
  assert response.data[0]["title"] == 'Test_course'
  assert response.data[0]["description"] == 'Test_description'
  assert response.data[0]["instructor"] == user.id
