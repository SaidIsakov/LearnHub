from decouple import config
import json
from .exceptions import AIServiceUnavailable, AIInvalidResponse
import openai

def ai_give_recommendations(context: dict) -> dict:

  client = openai.OpenAI(api_key=config('OPENAI_API_KEY'))

  prompt = f"""
  Ты — персональный наставник образовательной платформы LearnHub.
  Твоя задача — проанализировать статистику студента и дать персонализированные рекомендации.

  ## Правила анализа:

  1. **Не констатируй факты** — объясняй, ЧТО данные означают и КАК их улучшить.
  2. **Будь конкретным** — ссылайся на курсы, оценки, проценты из контекста.
  3. **Фокусируйся на действии** — рекомендации должны быть выполнимы в течение недели.
  4. **Будь мотивирующим, но честным**.

  ## Контекст студента:
  {context}

  ## Формат ответа (СТРОГО JSON):

  {{
    "summary": "Анализ успеваемости: что хорошо, где проблемы. 2-4 предложения с конкретными цифрами. Максимум 800 символов.",

    "strengths": [
      "Конкретное достижение с цифрами. Максимум 400 символов.",
      "Ещё одно достижение. Максимум 400 символов."
    ],

    "weaknesses": [
      "Конкретная проблема с объяснением почему это важно. Максимум 400 символов.",
      "Ещё одна проблема. Максимум 400 символов."
    ],

    "next_goal": "Конкретная измеримая цель на неделю. Максимум 800 символов.",

    "motivation": "Персональное мотивирующее сообщение на основе реальных достижений. Максимум 800 символов."
  }}

  ## Что НЕ делать:
  - Не повторяй данные из контекста дословно
  - Не используй общие фразы
  - Не придумывай факты
  - Не превышай указанные лимиты символов
  """

  try:
    response = client.chat.completions.create(
      model="gpt-5.4-mini",
      messages=[
        {"role": "user", "content": prompt}
      ]
    )
  except openai.APIError:
    raise AIServiceUnavailable()

  content = response.choices[0].message.content

  try:
    return json.loads(content)
  except json.JSONDecodeError:
    raise AIInvalidResponse()
