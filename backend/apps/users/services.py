from django.db.models import Sum
from apps.assignments.models import Assignment, AssignmentStatus, Submission
from apps.users.ai_recommendation import ai_give_recommendations
from apps.users.models import AIRecommendation
from django.db.models import Count, Q, Subquery, OuterRef
from apps.courses.models import CourseMember, ChatMessage



def get_recommendation_context(user) -> dict:
  """
    Главная функция, которая собирает весь контекст для AI
  """

  return {
    "courses": get_courses_stats(user),
    **get_user_general_stats(user),
    "pending_assignments": get_pending_assignments_count(user),
    "completion_rate": get_completion_rate(user),
    "recent_questions": get_recent_questions(user),
    "last_grades": get_last_grades(user)
  }


def get_user_general_stats(user) -> dict:
  """
  Собирает общую статистику
  """
  submitted = user.submissions.filter(status=AssignmentStatus.SUBMITTED)
  total_submissions = submitted.count()
  if total_submissions > 0:
    total_grade = submitted.aggregate(Sum('grade'))['grade__sum'] or 0
    average_grade = total_grade / total_submissions
  else:
    average_grade = 0

  return {
      "average_grade": average_grade,
      "total_submissions": user.submissions.count(),
    }


def get_courses_stats(user):
  """
  Собирает статистику по курсам
  """
  courses_data = []

  memberships = user.course_memberships.select_related("course").annotate(
      lessons_total=Count("course__lessons", distinct=True),
      assignments_total=Count("course__lessons__assignments",
      filter=Q(
        course__lessons__is_published=True,
        course__lessons__course__is_published=True
        ),
        distinct=True
      ),
      assignments_submitted=Count("course__lessons__assignments__submissions", filter=Q(
        course__lessons__assignments__submissions__status=AssignmentStatus.SUBMITTED,
        course__lessons__assignments__submissions__student=user
      ),
      distinct=True
    )
  )

  for membership in memberships:
    course = membership.course
    courses_data.append({
      "title": course.title,
      "lessons_total": membership.lessons_total,
      "assignments_submitted": membership.assignments_submitted or 0,
      "assignments_total": membership.assignments_total
    })
  return courses_data


def get_pending_assignments_count(user) -> int:
  """
  Считает задания со статусом в процессе
  """
  return Assignment.objects.filter(
            submissions__student=user,
            submissions__status = AssignmentStatus.PENDING
         ).count()


def get_completion_rate(user) -> int:
  """
    Считает процент завершения курса
  """
  stats = get_courses_stats(user)
  submitted = sum(course['assignments_submitted'] for course in stats)
  total = sum(course["assignments_total"] for course in stats)

  if total == 0:
    return 0

  return round(submitted / total * 100)


def get_recent_questions(user) -> list:
  """
    Получаем последние 5 вопросов к AI
  """
  return list(
    ChatMessage.objects.filter(
    user=user
  ).order_by('-created_at')[:5].values_list('question', flat=True)
  )

def get_last_grades(user) -> list:
  """
    Последние оценки
  """
  return list(
    user.submissions.filter(
    status=AssignmentStatus.SUBMITTED
  ).order_by('-submitted_at')[:5].values('assignment__title', 'grade')
  )

class RecommendationService:

  @staticmethod
  def generate(user):
    context = get_recommendation_context(user)
    ai_recommendations = ai_give_recommendations(context)

    AIRecommendation.objects.update_or_create(
        user = user,
        defaults = {
          "summary": ai_recommendations['summary'],
          "strengths": ai_recommendations['strengths'],
          "weaknesses": ai_recommendations['weaknesses'],
          "next_goal":  ai_recommendations['next_goal'],
          "motivation":  ai_recommendations['motivation']
        }
      )

    return ai_recommendations
