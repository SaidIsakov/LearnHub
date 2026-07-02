from openai import OpenAI
from decouple import config

def ask_ai_about_lesson(lesson_content: str,  question: str) -> str:
  """
    Отправляет вопрос в OpenAI c контекстом вопроса
  """

  client = OpenAI(api_key=config('OPENAI_API_KEY'))

  prompt = f"""
  Вот материал урока:
  {lesson_content}

  Вопрос студента: {question}

  Ответь на вопрос используя информацию из материала урока выше.
  Если в материале нет ответа - скажи об этом честно.
  """

  response = client.chat.completions.create(
    model="gpt-5.4-mini",
    messages=[
      {"role": "user", "content": prompt}
    ]
  )

  return response.choices[0].message.content
