from django.db.models import Sum
from apps.assignments.models import Assignment, AssignmentStatus, Submission
from apps.users.ai_recommendation import ai_give_recommendations
from apps.users.models import AIRecommendation



def get_recommendation_context(user) -> dict:
  """
    Главная функция, которая собирает весь контекст для AI
  """

  return {
    "courses": get_courses_stats(user),
    **get_user_general_stats(user),
    "pending_assignments": get_pending_assignments_count(user)
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

  for membership in user.course_memberships.all():
    course = membership.course
    courses_data.append({
      "title": course.title,
      "lessons_total": course.lessons.count(),
      "assignments_submitted": user.submissions.filter(
          status=AssignmentStatus.SUBMITTED,
          assignment__lesson__course=course
          ).count(),
      "assignments_total": Assignment.objects.filter(
          lesson__course=course,
          lesson__is_published=True,
          lesson__course__is_published=True
        ).count(),
    })
  return courses_data


def get_pending_assignments_count(user):
  """
  Считает задания со статусом в процессе
  """
  return Assignment.objects.filter(
            submissions__student=user,
            submissions__status = AssignmentStatus.PENDING
         ).count()


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
