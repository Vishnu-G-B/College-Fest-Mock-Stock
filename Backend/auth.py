from flask_wtf.csrf import Blueprint, request
from flask import make_response, session
from flask_cors import CORS
import json
import database
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_required,
    JWTManager,
)
import string

auth_bp = Blueprint("auth", __name__, url_prefix="/api/v1/auth")

CORS(auth_bp)

# No error checking with supabase

@auth_bp.route("/signup", methods=["POST"])
def sign_up():
    if request.method == "POST":
        username: str = request.json.get("email", None)
        password: str = request.json.get("password", None)
        confirm_password: str = request.json.get("confirmPassword", None)
        valid_username: list[bool, str] = validate_email(email=username)
        valid_password: list[bool, str] = validate_password(password=password)
        valid_confirm_password: list[bool, str] = [
            False, "Confirm Password not equal to password"]
        if valid_password[0] == True:
            valid_confirm_password = validate_confirm_password(
                password=password, confirm_password=confirm_password
            )
        if valid_username[0] and valid_password[0] and valid_confirm_password[0]:
            client = database.Supa()
            user = client.sign_user_up(username, password)
            # print(user.user.id)
            # print(user.session)
            # flask.g.user = {'user_id': user.user.id, 'session': user.session}
            # global_var.user = {'user_id': user.user.id, 'session': user.session}
            # resp = make_response()
            # resp.set_cookie('user', json.dumps({'user_id': user.user.id, 'session': user.session}))
            return json.dumps({"status": "success"})
        else:
            return json.dumps(
                {
                    "status": "failure",
                    "email_message": f"{valid_username[1]}",
                    "password_message": f"{valid_password[1]}",
                    "confirm_password_message": f"{valid_confirm_password[1]}",
                }
            )

# No error checking with supabase


@auth_bp.route("/login", methods=["POST"])
def login():
    if request.method == "POST":
        client = database.Supa()
        email_id: str = request.json.get("email", None)
        password: str = request.json.get("password", None)
        client.sign_user_out()
        user = client.sign_user_in(email_id, password)
        data = client.create_users_funds(user.user.id)
        # global_var.user = {'user_id': user.user.id, 'session': user.session}
        return json.dumps({'user_id': user.user.id})
        

def validate_email(email: str) -> bool:
    if email is not None:
        if len(email) > 4:
            if " " not in email:
                return [True, "validated"]
            else:
                return [False, "user name should be at least 4 characters long"]
        else:
            return [False, "user name should not contain any space"]
    else:
        return [False, "username cannot be empty"]


def validate_password(password: str) -> list[bool, str]:
    special_characters = string.punctuation
    if password is not None:
        if len(password) > 6:
            if any(list(map(lambda char: char in special_characters, password))):
                if password.isalnum:
                    return [True, "validated"]
                else:
                    return [
                        False,
                        "your password should contain at least on numeric number",
                    ]
            else:
                return [
                    False,
                    "your password should contain at least one special character",
                ]
        else:
            return [False, "password should be longer than 6 characters"]
    else:
        return [False, "password field cannot be empty"]


def validate_confirm_password(password: str, confirm_password: str) -> list[bool, str]:
    if confirm_password != password:
        return [False, "confirm password not equal to password"]
    else:
        return [True, "validated"]
