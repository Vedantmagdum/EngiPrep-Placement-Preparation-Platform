import psycopg2
from config import Config

def get_connection():
    connection = psycopg2.connect(
        host=Config.DB_HOST,
        port=Config.DB_PORT,
        database=Config.DB_NAME,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD
    )

    return connection

#  ya line la call kela code ha from db import get_topic_id, insert_generated_question, question_exists

def get_topic_id(topic_name):
    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT topic_id
            FROM aptitude_topics
            WHERE LOWER(topic_name) = LOWER(%s)
            """,
            (topic_name,)
        )

        result = cursor.fetchone()

        if result:
            return result[0]

        return None

    finally:
        cursor.close()
        conn.close()

def question_exists(topic_id, question_text):
    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT question_id
            FROM aptitude_questions
            WHERE topic_id = %s
            AND LOWER(TRIM(question_text)) = LOWER(TRIM(%s))
            LIMIT 1
            """,
            (topic_id, question_text)
        )

        result = cursor.fetchone()

        if result:
            return True

        return False

    finally:
        cursor.close()
        conn.close()
        
def insert_generated_question(topic_id, question):
    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO aptitude_questions
            (
                topic_id,
                question_text,
                option_a,
                option_b,
                option_c,
                option_d,
                correct_answer,
                difficulty,
                explanation
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING question_id
            """,
            (
                topic_id,
                question.question,
                question.option_a,
                question.option_b,
                question.option_c,
                question.option_d,
                question.correct_answer,
                "Medium",
                question.explanation
            )
        )

        question_id = cursor.fetchone()[0]

        conn.commit()

        return question_id

    except Exception:
        conn.rollback()
        raise

    finally:
        cursor.close()
        conn.close()