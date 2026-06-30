import pytest
from apps.courses.models import Course, Lesson, CourseMember, CourseRole
from rest_framework import status

@pytest.mark.django_db
def test_instructor_can_add_member(create_user, create_api_client, course, create_instructor):
  """
    Инструктор может добавить участника
  """
  alex = create_user('Alex')

  instructor = create_instructor(alex, course)

  misha = create_user('Misha')
  url = '/api/members/'

  client = create_api_client(alex)
  url = '/api/members/'
  data = {
    'user': misha.id,
    'course': course.id,
    'role': 'STUDENT'
  }

  response = client.post(url, data=data, format="json")

  assert response.status_code == status.HTTP_201_CREATED

@pytest.mark.django_db
def test_instructor_can_remove_member(course, create_api_client, create_user, create_student, create_instructor):
  """
    Инструктор может удалить участника
  """
  alex = create_user('Alex')

  instructor = create_instructor(alex, course)

  misha = create_user('Misha')

  student = create_student(misha, course)

  client = create_api_client(alex)
  url = f'/api/members/{student.id}/'

  response = client.delete(url)

  assert response.status_code == status.HTTP_204_NO_CONTENT
