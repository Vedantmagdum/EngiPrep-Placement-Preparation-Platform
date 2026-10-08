from flask import Blueprint, request, jsonify, render_template, session, redirect
from db import get_connection

profile = Blueprint("profile", __name__)


# ==========================================
# OPEN PROFILE PAGE + LOAD EXISTING DATA
# ==========================================

@profile.route("/profile")
def profile_page():

    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            u.full_name,
            u.email,
            p.phone,
            p.city,
            p.college,
            p.branch,
            p.semester,
            p.cgpa,
            p.graduation_year,
            p.competitions,
            p.academic_achievements,
            p.skills,
            p.strengths,
            p.weaknesses,
            p.project_title,
            p.project_technologies,
            p.project_description,
            p.project_github,
            p.linkedin,
            p.github,
            p.resume_link
        FROM users u
        LEFT JOIN profiles p
            ON u.user_id = p.user_id
        WHERE u.user_id = %s
    """, (user_id,))

    profile_data = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template(
        "profile.html",
        profile=profile_data
    )


# ==========================================
# SAVE / UPDATE PROFILE
# ==========================================

@profile.route("/profile/save", methods=["POST"])
def save_profile():

    if "user_id" not in session:
        return jsonify({"message": "Please login first"}), 401

    data = request.get_json()
    user_id = session["user_id"]

    conn = get_connection()
    cursor = conn.cursor()

    try:

        # --------------------------------------
        # UPDATE USERS TABLE
        # --------------------------------------

        cursor.execute("""
            UPDATE users
            SET full_name = %s,
                email = %s
            WHERE user_id = %s
        """, (
            data.get("full_name"),
            data.get("email"),
            user_id
        ))


        # --------------------------------------
        # INSERT / UPDATE PROFILES TABLE
        # --------------------------------------

        cursor.execute("""
            INSERT INTO profiles
            (
                user_id,
                phone,
                college,
                branch,
                year,
                cgpa,
                skills,
                city,
                semester,
                graduation_year,
                competitions,
                academic_achievements,
                strengths,
                weaknesses,
                project_title,
                project_technologies,
                project_description,
                project_github,
                linkedin,
                github,
                resume_link
            )
            VALUES (
                %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s
            )

            ON CONFLICT (user_id)
            DO UPDATE SET

                phone = EXCLUDED.phone,
                college = EXCLUDED.college,
                branch = EXCLUDED.branch,
                year = EXCLUDED.year,
                cgpa = EXCLUDED.cgpa,
                skills = EXCLUDED.skills,
                city = EXCLUDED.city,
                semester = EXCLUDED.semester,
                graduation_year = EXCLUDED.graduation_year,
                competitions = EXCLUDED.competitions,
                academic_achievements = EXCLUDED.academic_achievements,
                strengths = EXCLUDED.strengths,
                weaknesses = EXCLUDED.weaknesses,
                project_title = EXCLUDED.project_title,
                project_technologies = EXCLUDED.project_technologies,
                project_description = EXCLUDED.project_description,
                project_github = EXCLUDED.project_github,
                linkedin = EXCLUDED.linkedin,
                github = EXCLUDED.github,
                resume_link = EXCLUDED.resume_link
        """, (

            user_id,

            data.get("phone"),
            data.get("college"),
            data.get("branch"),

            # Existing "year" column
            data.get("graduation_year"),

            data.get("cgpa"),
            data.get("skills"),

            data.get("city"),
            data.get("semester"),
            data.get("graduation_year"),

            data.get("competitions"),
            data.get("academic_achievements"),

            data.get("strengths"),
            data.get("weaknesses"),

            data.get("project_title"),
            data.get("project_technologies"),
            data.get("project_description"),
            data.get("project_github"),

            data.get("linkedin"),
            data.get("github"),
            data.get("resume_link")
        ))

        conn.commit()

        return jsonify({
            "message": "Profile saved successfully"
        })

    except Exception as e:

        conn.rollback()

        print("PROFILE SAVE ERROR:", e)

        return jsonify({
            "message": str(e)
        }), 500

    finally:

        cursor.close()
        conn.close()