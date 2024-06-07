from flask import Blueprint, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
)
from db.db import get_db

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=("POST",))
def register():
    if request.method == "POST":
        data = request.get_json()

        # Check if the data is valid
        if not data:
            return jsonify({"error": "No data provided"}), 400

        username = data.get("username")
        password = data.get("password")
        db = get_db()
        cur = db.cursor()
        error = None

        if not username:
            error = "Username is required"
        elif not password:
            error = "Password is required"

        if error is None:
            try:
                query = 'INSERT INTO "user" ("username", "password") VALUES (%s, %s)'
                cur.execute(
                    query,
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return (
                    jsonify(
                        {
                            "message": "Registration succesful",
                            "status": "success",
                        }
                    ),
                    201,
                )

        return jsonify({"status": "failure", "error": f"{error}"}), 400


@bp.route("/login", methods=("POST",))
def login():
    if request.method == "POST":
        data = request.get_json()

        # Check if the data is valid
        if not data:
            return jsonify({"error": "No data provided"}), 400

        username = data.get("username")
        password = data.get("password")

        db = get_db()
        cur = db.cursor()
        error = None

        query = 'SELECT * FROM "user" WHERE "username" = %s'
        cur.execute(query, (username,))
        user = cur.fetchone()
        # print(user("password"))

        if user is None:
            error = "Incorrect username."
        elif not check_password_hash(user[2], password):
            error = "Incorrect password."

        if error is None:
            # session.clear()
            # session["user_id"] = user[0]
            auth_token = create_access_token(identity=user, fresh=True)
            refresh_token = create_refresh_token(identity=user)
            # print(auth_token)
            return (
                jsonify(
                    {
                        "message": "Login succesful",
                        "status": "success",
                        "data": {
                            "username": username,
                            "access_token": auth_token,
                            "refresh_token": refresh_token,
                        },
                    },
                ),
                200,
            )

        return jsonify({"status": "failure", "error": f"{error}"}), 400


@bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity, fresh=False)
    return jsonify(access_token=access_token)


@bp.route("/logout")
def logout():
    # session.clear()
    return jsonify({"message": "Logout Successful", "status": "success"}), 205
