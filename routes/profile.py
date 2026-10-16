
from flask import Blueprint, render_template, request, redirect, session, url_for
from db import get_connection

profile = Blueprint("profile", __name__)


@profile.route("/profile", methods=["GET", "POST"])
def profile_page():

    if "user_id" not in session:
        return redirect(url_for("login_page"))

    user_id = session["user_id"]

    conn = get_connection()
    cursor = conn.cursor()

    try:
        if request.method == "POST":

            full_name = request.form.get("full_name", "").strip()
            email = request.form.get("email", "").strip()
            phone = request.form.get("phone", "").strip()
            city = request.form.get("city", "").strip()

            college_name = request.form.get("college_name", "").strip()
            branch = request.form.get("branch", "").strip()
            semester = request.form.get("semester") or None
            cgpa = request.form.get("cgpa") or None
            graduation_year = request.form.get("graduation_year") or None

            competitions = request.form.get("competitions", "")
            academic_achievements = request.form.get(
                "academic_achievements", ""
            ).strip()

            skills = request.form.get("skills", "")
            strengths = request.form.get("strengths", "").strip()
            weaknesses = request.form.get("weaknesses", "").strip()

            project_title = request.form.get(
                "project_title", ""
            ).strip()
            project_technologies = request.form.get(
                "project_technologies", ""
            ).strip()
            project_description = request.form.get(
                "project_description", ""
            ).strip()
            project_github = request.form.get(
                "project_github", ""
            ).strip()

            linkedin = request.form.get("linkedin", "").strip()
            github = request.form.get("github", "").strip()
            resume_link = request.form.get("resume_link", "").strip()

            cursor.execute("""
                UPDATE users
                SET full_name = %s,
                    email = %s
                WHERE user_id = %s
            """, (full_name, email, user_id))

            cursor.execute("""
                SELECT profile_id
                FROM student_profile
                WHERE user_id = %s
            """, (user_id,))

            existing_profile = cursor.fetchone()

            if existing_profile:
                cursor.execute("""
                    UPDATE student_profile
                    SET college_name = %s,
                        branch = %s,
                        semester = %s,
                        cgpa = %s,
                        phone = %s,
                        city = %s,
                        linkedin = %s,
                        github = %s,
                        resume_link = %s,
                        strengths = %s,
                        weaknesses = %s,
                        academic_achievements = %s,
                        graduation_year = %s,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE user_id = %s
                """, (
                    college_name,
                    branch,
                    semester,
                    cgpa,
                    phone,
                    city,
                    linkedin,
                    github,
                    resume_link,
                    strengths,
                    weaknesses,
                    academic_achievements,
                    graduation_year,
                    user_id
                ))
            else:
                cursor.execute("""
                    INSERT INTO student_profile (
                        user_id,
                        college_name,
                        branch,
                        semester,
                        cgpa,
                        phone,
                        city,
                        linkedin,
                        github,
                        resume_link,
                        strengths,
                        weaknesses,
                        academic_achievements,
                        graduation_year
                    )
                    VALUES (
                        %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s, %s
                    )
                """, (
                    user_id,
                    college_name,
                    branch,
                    semester,
                    cgpa,
                    phone,
                    city,
                    linkedin,
                    github,
                    resume_link,
                    strengths,
                    weaknesses,
                    academic_achievements,
                    graduation_year
                ))

            cursor.execute("""
                DELETE FROM competitions
                WHERE user_id = %s
            """, (user_id,))

            for competition in competitions.split(","):
                competition = competition.strip()

                if competition:
                    cursor.execute("""
                        INSERT INTO competitions (
                            user_id, competition_name
                        )
                        VALUES (%s, %s)
                    """, (user_id, competition))

            cursor.execute("""
                DELETE FROM student_skills
                WHERE user_id = %s
            """, (user_id,))

            for skill in skills.split(","):
                skill = skill.strip()

                if skill:
                    cursor.execute("""
                        INSERT INTO skills (skill_name)
                        VALUES (%s)
                        ON CONFLICT (skill_name) DO NOTHING
                    """, (skill,))

                    cursor.execute("""
                        SELECT skill_id
                        FROM skills
                        WHERE skill_name = %s
                    """, (skill,))

                    skill_record = cursor.fetchone()

                    if skill_record:
                        cursor.execute("""
                            INSERT INTO student_skills (
                                user_id, skill_id, skill_level
                            )
                            VALUES (%s, %s, %s)
                            ON CONFLICT (user_id, skill_id)
                            DO UPDATE SET
                                last_updated = CURRENT_TIMESTAMP
                        """, (user_id, skill_record[0], 50))

            if project_title:
                cursor.execute("""
                    SELECT project_id
                    FROM projects
                    WHERE user_id = %s
                    ORDER BY project_id DESC
                    LIMIT 1
                """, (user_id,))

                existing_project = cursor.fetchone()

                if existing_project:
                    cursor.execute("""
                        UPDATE projects
                        SET project_title = %s,
                            description = %s,
                            technologies = %s,
                            github_link = %s
                        WHERE project_id = %s
                    """, (
                        project_title,
                        project_description,
                        project_technologies,
                        project_github,
                        existing_project[0]
                    ))
                else:
                    cursor.execute("""
                        INSERT INTO projects (
                            user_id,
                            project_title,
                            description,
                            technologies,
                            github_link,
                            project_status
                        )
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (
                        user_id,
                        project_title,
                        project_description,
                        project_technologies,
                        project_github,
                        "Completed"
                    ))

            conn.commit()

            return redirect(url_for("dashboard.dashboard_page"))

        cursor.execute("""
            SELECT full_name, email
            FROM users
            WHERE user_id = %s
        """, (user_id,))
        user = cursor.fetchone()

        profile = {}

        cursor.execute("""
            SELECT
                college_name,
                branch,
                semester,
                cgpa,
                phone,
                city,
                linkedin,
                github,
                resume_link,
                strengths,
                weaknesses,
                academic_achievements,
                graduation_year
            FROM student_profile
            WHERE user_id = %s
        """, (user_id,))

        profile_data = cursor.fetchone()

        if profile_data:
            profile = {
                "college_name": profile_data[0],
                "branch": profile_data[1],
                "semester": profile_data[2],
                "cgpa": profile_data[3],
                "phone": profile_data[4],
                "city": profile_data[5],
                "linkedin": profile_data[6],
                "github": profile_data[7],
                "resume_link": profile_data[8],
                "strengths": profile_data[9],
                "weaknesses": profile_data[10],
                "academic_achievements": profile_data[11],
                "graduation_year": profile_data[12]
            }

        cursor.execute("""
            SELECT competition_name
            FROM competitions
            WHERE user_id = %s
            ORDER BY competition_name
        """, (user_id,))

        competitions = ", ".join(
            row[0] for row in cursor.fetchall() if row[0]
        )

        cursor.execute("""
            SELECT s.skill_name
            FROM student_skills ss
            JOIN skills s ON s.skill_id = ss.skill_id
            WHERE ss.user_id = %s
            ORDER BY s.skill_name
        """, (user_id,))

        skills = ", ".join(
            row[0] for row in cursor.fetchall() if row[0]
        )

        cursor.execute("""
            SELECT
                project_title,
                technologies,
                description,
                github_link
            FROM projects
            WHERE user_id = %s
            ORDER BY project_id DESC
            LIMIT 1
        """, (user_id,))

        project_data = cursor.fetchone()

        project = {}

        if project_data:
            project = {
                "project_title": project_data[0],
                "project_technologies": project_data[1],
                "project_description": project_data[2],
                "project_github": project_data[3]
            }

        return render_template(
            "profile.html",
            user=user,
            profile=profile,
            competitions=competitions,
            skills=skills,
            project=project
        )

    except Exception:
        conn.rollback()
        raise

    finally:
        cursor.close()
        conn.close()
