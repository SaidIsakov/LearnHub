from openai import OpenAI
from decouple import config
import json

def ai_give_recommendations(context: dict) -> dict:

  client = OpenAI(api_key=config('OPENAI_API_KEY'))

  prompt = f"""
    Ты персональный наставник LearnHub.
    Ты анализируешь статистику обучения студента.
    Не придумывай фактов. Используй только информацию из контекста.

    Контекст:
    {context}

    Верни СТРОГО в формате JSON:
    {{
      "summary": "Краткое резюме успеваемости (максимум 200 символов)",
      "strengths": ["Сильная сторона 1", "Сильная сторона 2"],
      "weaknesses": ["Слабая сторона 1", "Слабая сторона 2"],
      "next_goal": "Конкретная цель на следующую неделю (максимум 200 символов)",
      "motivation": "Мотивирующее сообщение студенту (максимум 200 символов)"
    }}
    """

  response = client.chat.completions.create(
    model="gpt-5.4-mini",
    messages=[
      {"role": "user", "content": prompt}
    ]
  )

  content = response.choices[0].message.content

  return json.loads(content)
