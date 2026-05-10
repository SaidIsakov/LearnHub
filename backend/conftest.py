import pytest
from rest_framework.test import APIClient
from apps.users.models import User
from apps.courses.models import Course


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
