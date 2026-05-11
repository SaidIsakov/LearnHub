import pytest
from apps.courses.models import CourseMember
from apps.courses.models import Course, CourseMember, CourseRole
from rest_framework import status


@pytest.mark.django_db
def test_student_cannot_update_course(course, create_user, create_api_client):
  """
    Студент не может обновлять курс
  """
  misha = create_user('Misha')

  stud = CourseMember.objects.create(
    user=misha,
    course=course,
    role=CourseRole.STUDENT
  )
  client = create_api_client(misha)
  url = f'/api/courses/{course.id}/'

  response = client.patch(url, {'title': 'Hacked!'}, format='json')

  assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_instructor_can_update_course(course, create_api_client, create_user):
  """
    Инструктор может редактировать
  """
  alex = create_user('Alex')

  instructor = CourseMember.objects.create(
    user=alex,
    course=course,
    role=CourseRole.INSTRUCTOR
  )

  url = f'/api/courses/{course.id}/'

  client = create_api_client(alex)

  response = client.patch(url, {'title': 'Hacked'}, format='json')

  assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_observer_can_see_course(course, create_api_client, create_user):
  """
    Наблюдатель может видеть курс
  """
  li = create_user('Li')

  observer = CourseMember.objects.create(
    user=li,
    course=course,
    role=CourseRole.OBSERVER
  )

  url = f'/api/courses/{course.id}/'

  client = create_api_client(li)

  response = client.get(url, format='json')

  assert response.status_code == status.HTTP_200_OK
