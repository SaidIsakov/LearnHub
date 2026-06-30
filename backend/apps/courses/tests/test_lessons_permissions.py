import pytest
from rest_framework import status
from apps.courses.models import Lesson, Course, CourseMember, CourseRole


def test_student_cannot_create_lesson(create_user, create_api_client, course, create_student):
  """
    Студент не может создать занятие
  """
  url = '/api/lessons/'

  alex = create_user('Alex')


  student = create_student(alex, course)

  client = create_api_client(alex)

  data = {
    'title': 'Test_lesson',
    'content': 'Test_content',
    'course': course.id,
  }

  response = client.post(url, data=data, format='json')

  assert response.status_code == status.HTTP_403_FORBIDDEN


def test_ta_can_edit_lesson(create_user, create_api_client, course, create_instructor, lesson, create_teach_assist):
  """
    TEACHING_ASSISTANT может редактировать задачи
  """

  alex = create_user('Alex')
  vova = create_user('Vova')

  teach_assist = create_teach_assist(alex, course)

  instructor = create_instructor(vova, course)

  url = f'/api/lessons/{lesson.id}/'


  client = create_api_client(alex)

  response = client.patch(url, {'title': 'Changed!'}, format='json')
  assert response.status_code == status.HTTP_200_OK


def test_ta_cannot_delete_lesson(create_user, create_api_client, course, lesson, create_teach_assist):
  """
    TEACHING_ASSISTANT не может удалить занятие
  """
  alex = create_user('Alex')
  vova = create_user('Vova')

  teach_assist = create_teach_assist(alex, course)

  url = f'/api/lessons/{lesson.id}/'

  client = create_api_client(alex)

  response = client.delete(url, format='json')

  assert response.status_code == status.HTTP_403_FORBIDDEN
