import pytest
from apps.courses.models import CourseMember, CourseRole
from apps.courses.models import Lesson
from rest_framework import status
from apps.assignments.models import Assignment

@pytest.mark.django_db
def test_instructor_can_create_assignment(create_user, course, create_api_client):
  """
    Инструктор может создать дз
  """
  alex = create_user('Alex')
  instructor = CourseMember.objects.create(
    user=alex,
    course=course,
    role=CourseRole.INSTRUCTOR
  )
  lesson = Lesson.objects.create(course=course, created_by=alex, title='Test Lesson')

  client = create_api_client(alex)

  url = '/api/assignments/'

  response = client.post(url, data={"lesson": lesson.id, "title": "Create Base Model"})

  assert response.status_code == status.HTTP_201_CREATED

@pytest.mark.django_db
def test_student_can_submit_work(create_user, create_api_client, course):
  """
    Студент сдаёт работу
  """
  misha = create_user('Misha')
  alex = create_user('Alex')

  student = CourseMember.objects.create(
    user=misha,
    course=course,
    role=CourseRole.STUDENT
  )


  instructor = CourseMember.objects.create(
    user=alex,
    course=course,
    role=CourseRole.INSTRUCTOR
  )

  lesson = Lesson.objects.create(course=course, created_by=alex, title='Test Lesson')

  assignment = Assignment.objects.create(lesson=lesson, title='Create Models', created_by=alex)

  client = create_api_client(misha)
  url = '/api/submissions/'

  response = client.post(url, data={"assignment": assignment.id, "content": "create models"})

  assert response.status_code == status.HTTP_201_CREATED

@pytest.mark.django_db
def test_student_cannot_create_assignment(create_user, create_api_client, course):
  """
    Студент не может создать дз
  """
  misha = create_user('Misha')
  alex = create_user('Alex')

  instructor = CourseMember.objects.create(
    user=alex,
    course=course,
    role=CourseRole.INSTRUCTOR
  )

  student = CourseMember.objects.create(
    user=misha,
    course=course,
    role=CourseRole.STUDENT
  )
  lesson = Lesson.objects.create(course=course, created_by=alex, title='Test Lesson')

  client = create_api_client(misha)

  url = '/api/assignments/'

  response = client.post(url, data={"lesson": lesson.id, "title": "Create Base Model"})

  assert response.status_code == status.HTTP_403_FORBIDDEN
