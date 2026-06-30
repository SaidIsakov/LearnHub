import pytest
from apps.courses.models import CourseMember, CourseRole
from apps.courses.models import Lesson
from rest_framework import status
from apps.assignments.models import Assignment

@pytest.mark.django_db
def test_instructor_can_create_assignment(create_user, course, create_api_client, create_instructor, lesson):
  """
    Инструктор может создать дз
  """
  alex = create_user('Alex')

  instructor = create_instructor(alex, course)

  client = create_api_client(alex)

  url = '/api/assignments/'

  response = client.post(url, data={"lesson": lesson.id, "title": "Create Base Model"})

  assert response.status_code == status.HTTP_201_CREATED

@pytest.mark.django_db
def test_student_can_submit_work(create_user, create_api_client, course, create_student, create_instructor, lesson, assignment):
  """
    Студент сдаёт работу
  """
  misha = create_user('Misha')
  alex = create_user('Alex')

  student = create_student(misha, course)
  instructor = create_instructor(alex, course)

  client = create_api_client(misha)
  url = '/api/submissions/'

  response = client.post(url, data={"assignment": assignment.id, "content": "create models"})

  assert response.status_code == status.HTTP_201_CREATED

@pytest.mark.django_db
def test_student_cannot_create_assignment(create_user, create_api_client, course, create_instructor, create_student, lesson):
  """
    Студент не может создать дз
  """
  misha = create_user('Misha')
  alex = create_user('Alex')

  instructor = create_instructor(alex, course)
  student = create_student(misha, course)

  client = create_api_client(misha)

  url = '/api/assignments/'

  response = client.post(url, data={"lesson": lesson.id, "title": "Create Base Model"})

  assert response.status_code == status.HTTP_403_FORBIDDEN
