from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from db import get_connection

auth = Blueprint("auth", __name__)

# ---------------- SIGNUP ----------------

@auth.route("/signup", methods=["POST"])
def signup():

    data = request.get_json()

    full_name = data["full_name"]
    username = data["username"]
    email = data["email"]
    password = data["password"]

    hashed_password = generate_password_hash(password)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM users
        WHERE email=%s OR username=%s
    """, (email, username))

    existing = cursor.fetchone()

    if existing:
        cursor.close()
        conn.close()
        return jsonify({"message":"User already exists"}),400

    cursor.execute("""
        INSERT INTO users
        (full_name, username, email, password_hash)
        VALUES(%s,%s,%s,%s)
    """,(full_name,username,email,hashed_password))

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"message":"Signup Successful"}),201


# ---------------- LOGIN ----------------

@auth.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    username = data["username"]
    password = data["password"]

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT user_id, password_hash
        FROM users
        WHERE username=%s
    """, (username,))

    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user and check_password_hash(user[1], password):

        session["user_id"] = user[0]

        return jsonify({
            "message": "Login Successful"
        })

    return jsonify({
        "message": "Invalid Username or Password"
    }), 401