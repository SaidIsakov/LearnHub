from apps.courses.ai.ai_assistant import ask_ai_about_lesson
from .models import ChatMessage
from rest_framework.exceptions import ValidationError


class LessonAIService:

  @staticmethod
  def ask(lesson, user, question) -> str:
    """
      Задаем вопрос AI и сохраняем ответ
    """
    if not question:
      raise ValidationError({
          "question": ["Question is required."]
      })

    answer = ask_ai_about_lesson(lesson.content, question)

    ChatMessage.objects.create(
        lesson=lesson,
        user=user,
        question=question,
        answer=answer
    )

    return answer

