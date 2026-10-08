import os
from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel
from typing import List
from db import get_topic_id, insert_generated_question, question_exists


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not set in the .env file")


client = genai.Client(api_key=api_key)


class AptitudeQuestion(BaseModel):
    question: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    correct_answer: str
    explanation: str


class AptitudeQuestionSet(BaseModel):
    questions: List[AptitudeQuestion]


def generate_aptitude_questions(section, topic, number_of_questions=5):

    prompt = f"""
You are an aptitude question generator for a college placement preparation platform called EngiPrep.

Generate exactly {number_of_questions} multiple-choice aptitude questions.

Section: {section}
Topic: {topic}

Requirements:
- Questions must be suitable for engineering college placement preparation.
- Difficulty should be moderate.
- Every question must have exactly four options.
- Options must be labeled internally as A, B, C and D.
- Only one option must be correct.
- correct_answer must contain only A, B, C or D.
- Provide a short explanation for every answer.
- Do not repeat questions.
- Do not create questions that are only slightly different from each other.
- Do not use ambiguous questions.
- Make sure the correct answer is actually correct.
- Return only the requested structured data.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": AptitudeQuestionSet,
        }
    )

    result = AptitudeQuestionSet.model_validate_json(
        response.text
    )

    return result.questions

def generate_and_save_questions(section, topic, number_of_questions=5):

    topic_id = get_topic_id(topic)

    if topic_id is None:
        raise ValueError(
            f"Topic '{topic}' was not found in the database"
        )

    saved_question_ids = []

    attempts = 0

    max_attempts = 3

    while len(saved_question_ids) < number_of_questions and attempts < max_attempts:

        remaining_questions = (
            number_of_questions -
            len(saved_question_ids)
        )

        questions = generate_aptitude_questions(
            section,
            topic,
            remaining_questions
        )

        for question in questions:

            if len(saved_question_ids) >= number_of_questions:
                break

            if question_exists(
                topic_id,
                question.question
            ):

                print(
                    "Duplicate question skipped:",
                    question.question
                )

                continue

            question_id = insert_generated_question(
                topic_id,
                question
            )

            saved_question_ids.append(
                question_id
            )

        attempts += 1

    return saved_question_ids

def test_gemini():

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents="Say hello to EngiPrep in one short sentence."
    )

    return response.text

def chat_with_gemini(message, conversation_history=None):

    history = conversation_history or []

    system_instruction = """
You are EngiPrep AI, a friendly placement preparation assistant
for engineering college students.

Your responsibilities:
- Help students prepare for campus placements.
- Explain aptitude, logical reasoning, verbal ability,
  data interpretation and psychometric preparation.
- Help with programming, coding interviews and technical MCQs.
- Give interview preparation tips and resume improvement suggestions.
- Explain academic and project concepts in a beginner-friendly way.
- Provide practical study plans and examples.
- Keep answers clear, helpful and appropriately concise.
- If a question is unrelated to education or careers,
  politely guide the user back to placement preparation.
- Never claim that you have accessed a student's private dashboard,
  profile or database unless the application explicitly provides that data.
"""

    contents = []

    for item in history[-10:]:
        role = item.get("role")
        text = item.get("text", "")

        if role in ("user", "assistant") and text.strip():
            contents.append({
                "role": role,
                "parts": [{"text": text}]
            })

    contents.append({
        "role": "user",
        "parts": [{"text": message}]
    })

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=contents,
        config={
            "system_instruction": system_instruction,
            "temperature": 0.7
        }
    )

    answer = response.text

    if not answer:
        return "Sorry, I could not generate a response. Please try again."

    return answer.strip()

