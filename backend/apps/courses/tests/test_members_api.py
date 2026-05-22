import pytest
from apps.courses.models import Course, Lesson, CourseMember, CourseRole
from rest_framework import status

@pytest.mark.django_db
def test_instructor_can_add_member(create_user, create_api_client, course):
  """
    Инструктор может добавить участника
  """
  alex = create_user('Alex')

  instructor = CourseMember.objects.create(
    user=alex,
    course=course,
    role=CourseRole.INSTRUCTOR
  )

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
def test_instructor_can_remove_member(course, create_api_client, create_user):
  """
    Инструктор может удалить участника
  """
  alex = create_user('Alex')

  instructor = CourseMember.objects.create(
    user=alex,
    course=course,
    role=CourseRole.INSTRUCTOR
  )

  misha = create_user('Misha')

  member = CourseMember.objects.create(
    user=misha,
    course=course,
    role=CourseRole.STUDENT
  )

  client = create_api_client(alex)
  url = f'/api/members/{member.id}/'

  response = client.delete(url)

  assert response.status_code == status.HTTP_204_NO_CONTENT
