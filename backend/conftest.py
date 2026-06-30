import pytest
from rest_framework.test import APIClient
from apps.users.models import User
from apps.courses.models import Course, CourseMember, CourseRole, Lesson
from apps.assignments.models import Assignment


@pytest.fixture
def user():
  """
    Создает пользователя
  """
  return User.objects.create()


@pytest.fixture
def auth_client(user):
  """
    Логируем пользователя
  """
  client = APIClient()
  client.force_login(user)

  return client


@pytest.fixture
def course(user):
  """
    Создаем курс
  """
  return Course.objects.create(
    instructor=user,
    title='Test_course',
    description='Test_description'
  )


@pytest.fixture
def lesson(user, course, create_instructor):
  """
    Создаем урок
  """
  return Lesson.objects.create(
      title='Test_lesson',
      content='Test_content',
      course=course,
      created_by=user
  )


@pytest.fixture
def assignment(lesson, user):
  """
    Создаем урок
  """
  return Assignment.objects.create(
      lesson=lesson,
      title='Create Models',
      created_by=user
  )


@pytest.fixture
def create_user(db):
  """
    фабрика пользователей
  """
  def _create_user(name):
    return User.objects.create(username=name)
  return _create_user


@pytest.fixture
def create_api_client(db):
  """
    Создает клиента и логинет его
  """
  def _client_for(user):
    client = APIClient()
    client.force_login(user)
    return client
  return _client_for


@pytest.fixture
def create_student(db):
  """
    фабрика пользователей для студентов
  """
  def _create_student(user, course):
    return CourseMember.objects.create(user=user, course=course, role=CourseRole.STUDENT)
  return _create_student



@pytest.fixture
def create_instructor(db):
  """
    фабрика пользователей для инструкторов
  """
  def _create_instructor(user, course):
    return CourseMember.objects.create(user=user, course=course, role=CourseRole.INSTRUCTOR)
  return _create_instructor


@pytest.fixture
def create_observer(db):
  """
    фабрика пользователей для наблюдателей
  """
  def _create_observer(user, course):
    return CourseMember.objects.create(user=user, course=course, role=CourseRole.OBSERVER)
  return _create_observer


@pytest.fixture
def create_teach_assist(db):
  """
    фабрика пользователей для обучающих помощников
  """
  def _create_teach_assist(user, course):
    return CourseMember.objects.create(user=user, course=course, role=CourseRole.TEACHING_ASSISTANT)
  return _create_teach_assist


@pytest.fixture(autouse=True)
def celery_eager_mode(settings):
  settings.CELERY_TASK_ALWAYS_EAGER = True
