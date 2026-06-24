import redis


def invalidate_courses_cache():
  """
    Удаляет весь кэш списка курсов
  """

  r = redis.Redis(host='redis', port=6379, db=1)
  keys = r.keys('courses_list_*')
  if keys:
    r.delete(*keys)


def invalidate_lessons_cache():
  """
    Удаляет весь кэш списка занятий
  """

  r = redis.Redis(host='redis', port=6379, db=1)
  keys = r.keys('lessons_list_*')
  if keys:
    r.delete(*keys)
