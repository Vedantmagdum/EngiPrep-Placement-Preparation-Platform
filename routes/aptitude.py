from flask import Blueprint, render_template, request, session, redirect, url_for

from db import get_connection
from api_service import generate_and_save_questions


aptitude = Blueprint("aptitude", __name__)


QUESTIONS_PER_TEST = 5
QUESTION_BANK_SIZE = 10


@aptitude.route("/Aptitude")
def aptitude_page():

    if "user_id" not in session:
        return redirect(url_for("login_page"))

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT section_id, section_name
        FROM aptitude_sections
        ORDER BY section_id
    """)

    sections = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "Preparation/Aptitude.html",
        sections=sections
    )


@aptitude.route("/Aptitude/<int:section_id>")
def topics(section_id):

    if "user_id" not in session:
        return redirect(url_for("login_page"))

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT topic_id, topic_name
        FROM aptitude_topics
        WHERE section_id = %s
        ORDER BY topic_id
    """, (section_id,))

    topics = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "Preparation/AptitudeTopics.html",
        topics=topics,
        section_id=section_id
    )


@aptitude.route("/Aptitude/Test/<int:topic_id>", methods=["GET", "POST"])
def test(topic_id):

    if "user_id" not in session:
        return redirect(url_for("login_page"))

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            t.topic_name,
            s.section_name
        FROM aptitude_topics t
        JOIN aptitude_sections s
            ON t.section_id = s.section_id
        WHERE t.topic_id = %s
    """, (topic_id,))

    topic_info = cursor.fetchone()

    if not topic_info:
        cursor.close()
        conn.close()
        return "Topic not found", 404

    topic_name = topic_info[0]
    section_name = topic_info[1]


    if request.method == "GET":

        cursor.execute("""
            SELECT COUNT(*)
            FROM aptitude_questions
            WHERE topic_id = %s
        """, (topic_id,))

        question_count = cursor.fetchone()[0]

        cursor.close()
        conn.close()


        if question_count < QUESTION_BANK_SIZE:

            questions_needed = QUESTION_BANK_SIZE - question_count

            try:

                generate_and_save_questions(
                    section_name,
                    topic_name,
                    questions_needed
                )

            except Exception as e:

                print(
                    "Gemini question generation failed:",
                    e
                )


        conn = get_connection()
        cursor = conn.cursor()


        cursor.execute("""
            SELECT
                question_id,
                question_text,
                option_a,
                option_b,
                option_c,
                option_d
            FROM aptitude_questions
            WHERE topic_id = %s
            ORDER BY RANDOM()
            LIMIT %s
        """, (topic_id, QUESTIONS_PER_TEST))


        questions = cursor.fetchall()


        question_ids = [
            question[0]
            for question in questions
        ]


        session["aptitude_question_ids"] = question_ids
        session["aptitude_topic_id"] = topic_id


        cursor.close()
        conn.close()


        return render_template(
            "Preparation/AptitudeTest.html",
            questions=questions,
            topic_id=topic_id
        )


    question_ids = session.get(
        "aptitude_question_ids",
        []
    )


    if not question_ids:

        cursor.close()
        conn.close()

        return redirect(
            url_for(
                "aptitude.test",
                topic_id=topic_id
            )
        )


    cursor.execute("""
        SELECT
            question_id,
            question_text,
            option_a,
            option_b,
            option_c,
            option_d,
            correct_answer,
            explanation
        FROM aptitude_questions
        WHERE topic_id = %s
        AND question_id = ANY(%s)
    """, (
        topic_id,
        question_ids
    ))


    questions = cursor.fetchall()


    question_map = {
        question[0]: question
        for question in questions
    }


    ordered_questions = [
        question_map[question_id]
        for question_id in question_ids
        if question_id in question_map
    ]


    questions = ordered_questions


    total_questions = len(questions)

    correct_answers = 0

    result_questions = []


    for question in questions:

        question_id = question[0]

        question_text = question[1]

        option_a = question[2]

        option_b = question[3]

        option_c = question[4]

        option_d = question[5]

        correct_answer = question[6]

        explanation = question[7]


        selected_answer = request.form.get(
            f"question_{question_id}"
        )


        if selected_answer == correct_answer:

            correct_answers += 1


        if selected_answer == "A":

            selected_text = option_a

        elif selected_answer == "B":

            selected_text = option_b

        elif selected_answer == "C":

            selected_text = option_c

        elif selected_answer == "D":

            selected_text = option_d

        else:

            selected_text = "Not answered"


        if correct_answer == "A":

            correct_text = option_a

        elif correct_answer == "B":

            correct_text = option_b

        elif correct_answer == "C":

            correct_text = option_c

        else:

            correct_text = option_d


        result_questions.append({

            "question": question_text,

            "selected_answer": selected_answer,

            "selected_text": selected_text,

            "correct_answer": correct_answer,

            "correct_text": correct_text,

            "explanation": explanation

        })


    if total_questions > 0:

        percentage = (
            correct_answers /
            total_questions
        ) * 100

    else:

        percentage = 0


    score = correct_answers


    cursor.execute("""
        INSERT INTO aptitude_attempts
        (
            user_id,
            topic_id,
            total_questions,
            correct_answers,
            score,
            percentage
        )
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (

        session["user_id"],

        topic_id,

        total_questions,

        correct_answers,

        score,

        percentage

    ))


    conn.commit()


    session.pop(
        "aptitude_question_ids",
        None
    )

    session.pop(
        "aptitude_topic_id",
        None
    )


    cursor.close()
    conn.close()


    return render_template(

        "Preparation/AptitudeResult.html",

        total_questions=total_questions,

        correct_answers=correct_answers,

        score=score,

        percentage=round(
            float(percentage),
            2
        ),

        topic_id=topic_id,

        result_questions=result_questions

    )