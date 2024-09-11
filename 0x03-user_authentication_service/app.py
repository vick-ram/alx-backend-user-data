#!/usr/bin/env python3
from flask import Flask, jsonify, request, abort, make_response, redirect
from auth import Auth


app = Flask(__name__)

AUTH = Auth()


@app.route('/')
def index():
    """Simple endpoint"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST', 'GET'])
def register_user():
    """An endpoint to register new users"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            user = AUTH.register_user(email=email, password=password)
            return jsonify({"email": user.email, "message": "user created"})
        except ValueError:
            return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login():
    """Creates a login session for the user"""
    email = request.form.get('email')
    password = request.form.get('password')

    if not AUTH.valid_login(email=email, password=password):
        abort(401)

    session_id = AUTH.create_session(email)

    if session_id is None:
        abort(401)

    response = make_response(jsonify({
        "email": email,
        "message": "logged in"
    }))
    response.set_cookie("session_id", session_id)

    return response


@app.route('/sessions', methods=['DELETE'])
def logout():
    """Logs out the user by destroying their session"""
    session_id = request.cookies.get('session_id')

    if session_id is None:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)

    if user is None:
        abort(403)

    AUTH.destroy_session(user.id)

    return redirect('/')


@app.route('/profile', methods=['GET'])
def profile():
    """Retrieve user profile information"""
    session_id = request.cookies.get('session_id')

    if session_id is None:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)

    if user is None:
        abort(403)

    return jsonify({"email": user.email})


@app.route('reset_password', methods=['PUT'])
def update_password():
    """Updates the reset password"""
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')

    try:
        AUTH.update_password(reset_token=reset_token, password=new_password)
    except ValueError:
        abort(403)

    return jsonify({
        "email": email,
        "message": "Password updated"
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
