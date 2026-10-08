# /signup and /login routes are handled by auth.py.
# auth.py contains the authentication and authorization logic
# for signup and login, including password hashing and
# checking whether the user already exists in the database.

from flask import Flask, render_template, session, redirect
from db import get_connection
from config import Config

from routes.auth import auth
from routes.profile import profile
from routes.chatbot import chatbot
from routes.aptitude import aptitude


app = Flask(__name__)

app.config.from_object(Config)

app.secret_key = "abcd"


# =====================================================
# REGISTER BLUEPRINTS
# =====================================================

app.register_blueprint(auth)
app.register_blueprint(profile)
app.register_blueprint(chatbot)
app.register_blueprint(aptitude)


# =====================================================
# HOME
# =====================================================

@app.route("/")
def home():
    return render_template("index.html")


# =====================================================
# LOGIN PAGE
# =====================================================

@app.route("/login")
def login_page():
    return render_template("login.html")


# =====================================================
# SIGNUP PAGE
# =====================================================

@app.route("/signup")
def signup_page():
    return render_template("signup.html")

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")


# =====================================================
# PREPARATION PAGE
# =====================================================

@app.route("/Preparation")
def preparation_page():
    return render_template("Preparation.html")


# =====================================================
# DASHBOARD
# =====================================================

@app.route("/Dashboard")
def dashboard_page():

    # -------------------------------------------------
    # Check whether user is logged in
    # -------------------------------------------------

    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]

    conn = get_connection()
    cursor = conn.cursor()


    # =================================================
    # 1. GET USER PROFILE
    # =================================================

    cursor.execute("""
        SELECT
            u.full_name,
            u.username,
            u.email,

            p.college,
            p.branch,
            p.semester,
            p.cgpa,
            p.skills,
            p.city,

            p.linkedin,
            p.github,
            p.resume_link,

            p.competitions,
            p.academic_achievements,
            p.strengths,
            p.weaknesses,

            p.project_title,
            p.project_technologies,
            p.project_description,
            p.project_github,

            p.graduation_year

        FROM users u

        LEFT JOIN profiles p
            ON u.user_id = p.user_id

        WHERE u.user_id = %s
    """, (user_id,))

    profile_data = cursor.fetchone()


    # =================================================
    # 2. TOTAL APTITUDE TESTS
    # =================================================

    cursor.execute("""
        SELECT COUNT(*)
        FROM aptitude_attempts
        WHERE user_id = %s
    """, (user_id,))

    test_count = cursor.fetchone()[0]


    # =================================================
    # 3. AVERAGE APTITUDE SCORE
    # =================================================

    cursor.execute("""
        SELECT COALESCE(AVG(percentage), 0)
        FROM aptitude_attempts
        WHERE user_id = %s
    """, (user_id,))

    average_score = cursor.fetchone()[0]


    # =================================================
    # 4. COUNT USER SKILLS
    # =================================================

    skill_count = 0

    if profile_data and profile_data[7]:

        skill_count = len([
            skill.strip()
            for skill in profile_data[7].split(",")
            if skill.strip()
        ])


    # =================================================
    # 5. COUNT PROJECTS
    # =================================================

    project_count = 0

    if profile_data and profile_data[16]:
        project_count = 1


    # =================================================
    # 6. APTITUDE TEST HISTORY
    # =================================================

    cursor.execute("""
        SELECT
            aa.attempt_id,
            t.topic_name,
            aa.total_questions,
            aa.correct_answers,
            aa.score,
            aa.percentage,
            aa.attempted_at

        FROM aptitude_attempts aa

        JOIN aptitude_topics t
            ON aa.topic_id = t.topic_id

        WHERE aa.user_id = %s

        ORDER BY aa.attempted_at DESC
    """, (user_id,))

    aptitude_history = cursor.fetchall()


    # =================================================
    # 7. SECTION-WISE PERFORMANCE
    # =================================================

    cursor.execute("""
        SELECT
            s.section_name,
            COUNT(aa.attempt_id),
            COALESCE(AVG(aa.percentage), 0)

        FROM aptitude_sections s

        LEFT JOIN aptitude_topics t
            ON s.section_id = t.section_id

        LEFT JOIN aptitude_attempts aa
            ON t.topic_id = aa.topic_id
            AND aa.user_id = %s

        GROUP BY
            s.section_id,
            s.section_name

        ORDER BY s.section_id
    """, (user_id,))

    section_progress = cursor.fetchall()


    # =================================================
    # 8. TOPIC-WISE PERFORMANCE
    # =================================================

    cursor.execute("""
        SELECT
            s.section_name,
            t.topic_name,
            COUNT(aa.attempt_id),
            COALESCE(AVG(aa.percentage), 0)

        FROM aptitude_topics t

        JOIN aptitude_sections s
            ON t.section_id = s.section_id

        LEFT JOIN aptitude_attempts aa
            ON t.topic_id = aa.topic_id
            AND aa.user_id = %s

        GROUP BY
            s.section_id,
            s.section_name,
            t.topic_id,
            t.topic_name

        ORDER BY
            s.section_id,
            t.topic_id
    """, (user_id,))

    topic_progress = cursor.fetchall()


    # =================================================
    # 9. STRONG TOPICS
    # =================================================

    strong_topics = [
        topic
        for topic in topic_progress
        if topic[2] > 0 and topic[3] >= 80
    ]


    # =================================================
    # 10. IMPROVING TOPICS
    # =================================================

    improving_topics = [
        topic
        for topic in topic_progress
        if topic[2] > 0 and 50 <= topic[3] < 80
    ]


    # =================================================
    # 11. WEAK TOPICS
    # =================================================

    weak_topics = [
        topic
        for topic in topic_progress
        if topic[2] > 0 and topic[3] < 50
    ]


    # =================================================
    # 12. NOT ATTEMPTED TOPICS
    # =================================================

    not_attempted_topics = [
        topic
        for topic in topic_progress
        if topic[2] == 0
    ]


    # =================================================
    # CLOSE DATABASE
    # =================================================

    cursor.close()
    conn.close()


    # =================================================
    # 13. SEND DATA TO DASHBOARD
    # =================================================

    return render_template(
        "Dashboard.html",

        profile=profile_data,

        test_count=test_count,

        skill_count=skill_count,

        project_count=project_count,

        average_score=round(float(average_score), 2),

        aptitude_history=aptitude_history,

        topic_progress=topic_progress,

        section_progress=section_progress,

        strong_topics=strong_topics,

        improving_topics=improving_topics,

        weak_topics=weak_topics,

        not_attempted_topics=not_attempted_topics
    )


# =====================================================
# RUN APPLICATION
# =====================================================

if __name__ == "__main__":
    app.run(debug=True)