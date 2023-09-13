# from flask import Flask, request, jsonify
# import openai
# from flask_cors import CORS
# import os
# import json
# from flask_bcrypt import Bcrypt
# import smtplib
# from email.message import EmailMessage
# import random
# import time
# import google.cloud.firestore as firestore


# app = Flask(__name__)
# CORS(app)
# bcrypt = Bcrypt(app)

# # SMTP settings
# SMTP_SERVER = "smtp.gmail.com"
# SMTP_PORT = 587
# SMTP_USERNAME = os.getenv("GOOGLE_MAIL")
# SMTP_PASSWORD = os.getenv("GOOGLE_PASSWORD")
# SENDER_EMAIL = os.getenv("GOOGLE_MAIL")


# # Replace with your OpenAI API key
# openai.api_key = os.getenv("OPENAI_API_KEY")

# # Use the application default credentials
# db = firestore.Client.from_service_account_json('instantchat.json')

# @app.route('/ask', methods=['POST'])
# def ask_gpt():
#     # Get the prompt from POST request
#     user_prompt = request.json.get("prompt", "")

#     # Construct the new prompt
#     full_prompt = ("You are a helpful travel planner in Australia, based on the answers to the "
#                    "questions below, construct a travel plan for the user.\n" + str(user_prompt))

#     # Send it to ChatGPT and get the response
#     response = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role": "system", "content": "You are a helpful travel planner."},
#             {"role": "user", "content": full_prompt}
#         ]
#     )

#     # Extract the message content from the response
#     message_content = response.choices[0].message.content

#     # Return as a JSON response
#     return jsonify({"response": message_content})


# def send_email(recipient, subject, body):
#     msg = EmailMessage()
#     msg.set_content(body)
#     msg["Subject"] = subject
#     msg["From"] = SENDER_EMAIL
#     msg["To"] = recipient

#     with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
#         server.starttls()
#         server.login(SMTP_USERNAME, SMTP_PASSWORD)
#         server.send_message(msg)


# def generate_verification_code():
#     return str(random.randint(100000, 999999))


# @app.route('/signup', methods=['POST'])
# def signup():
#     username = request.json.get("username")
#     password = request.json.get("password")
#     email = request.json.get("username")

#     # Load users and verification codes from the JSON files
#     with open("users.json", "r") as file:
#         users_data = json.load(file)

#     with open("verification_codes.json", "r") as file:
#         codes_data = json.load(file)

#     # Check if user already exists
#     for user in users_data["users"]:
#         if user["username"] == username:
#             return jsonify({"error": "Email already exists!"}), 400

#     # Hash the password
#     hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

#     # Append new user to the list
#     users_data["users"].append({
#         "username": username,
#         "password": hashed_password,
#         "email": email,
#         "verified": False
#     })

#     # Generate verification code
#     code = generate_verification_code()

#     # Store the verification code and its expiration time (let's say 10 minutes)
#     expiration_time = time.time() + 600
#     codes_data["codes"].append({
#         "username": username,
#         "code": code,
#         "expires_at": expiration_time
#     })

#     # Send verification email
#     send_email(email, "Email Verification",
#                f"Your verification code is: {code}")

#     # Save back to the JSON files
#     with open("users.json", "w") as file:
#         json.dump(users_data, file)

#     with open("verification_codes.json", "w") as file:
#         json.dump(codes_data, file)

#     return jsonify({"message": "User registered successfully! Please verify your email."})


# @app.route('/verify', methods=['POST'])
# def verify_email():
#     username = request.json.get("username")
#     code = request.json.get("code")

#     # Load verification codes from the JSON file
#     with open("verification_codes.json", "r") as file:
#         codes_data = json.load(file)

#     # Check if the code is valid and not expired
#     for item in codes_data["codes"]:
#         if item["username"] == username and item["code"] == code:
#             if time.time() > item["expires_at"]:
#                 return jsonify({"error": "Verification code has expired!"}), 400
#             else:
#                 # Mark user as verified
#                 with open("users.json", "r") as file:
#                     users_data = json.load(file)
#                 for user in users_data["users"]:
#                     if user["username"] == username:
#                         user["verified"] = True
#                 with open("users.json", "w") as file:
#                     json.dump(users_data, file)
#                 return jsonify({"message": "Email verified successfully!"})

#     return jsonify({"error": "Invalid verification code!"}), 400


# @app.route('/resend_verification', methods=['POST'])
# def resend_verification():
#     username = request.json.get("username")

#     # Load users and verification codes from the JSON files
#     with open("users.json", "r") as file:
#         users_data = json.load(file)

#     with open("verification_codes.json", "r") as file:
#         codes_data = json.load(file)

#     email = None
#     for user in users_data["users"]:
#         if user["username"] == username:
#             email = user["email"]
#             break

#     if not email:
#         return jsonify({"error": "User not found!"}), 400

#     # Generate a new verification code
#     code = generate_verification_code()

#     # Update the verification code and its expiration time
#     for item in codes_data["codes"]:
#         if item["username"] == username:
#             item["code"] = code
#             item["expires_at"] = time.time() + 600

#     # Send verification email
#     send_email(email, "Email Verification",
#                f"Your verification code is: {code}")

#     # Save back to the verification codes JSON file
#     with open("verification_codes.json", "w") as file:
#         json.dump(codes_data, file)

#     return jsonify({"message": "Verification email resent successfully!"})


# @app.route('/login', methods=['POST'])
# def login():
#     username = request.json.get("username")
#     password = request.json.get("password")
#     email = request.json.get("username")

#     # Load users from the JSON file
#     with open("users.json", "r") as file:
#         data = json.load(file)

#     # Check if user exists, password matches, and email is verified
#     for user in data["users"]:
#         if user["username"] == username and bcrypt.check_password_hash(user["password"], password):
#             if not user.get("verified", False):
#                 return jsonify({"error": "Please verify your email before logging in!"}), 401
#             return jsonify({"message": "Login successful!"})

#     return jsonify({"error": "Invalid username or password!"}), 401



# if __name__ == "__main__":
#     app.run(debug=True, port=5001)


from flask import Flask, request, jsonify
import openai
from flask_cors import CORS
import os
import google.cloud.firestore as firestore
from flask_bcrypt import Bcrypt
import smtplib
from email.message import EmailMessage
import random
import time

app = Flask(__name__)
CORS(app)
bcrypt = Bcrypt(app)

# Firestore initialization
db = firestore.Client.from_service_account_json('instantchat.json')

# SMTP settings
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = os.getenv("GOOGLE_MAIL")
SMTP_PASSWORD = os.getenv("GOOGLE_PASSWORD")
SENDER_EMAIL = os.getenv("GOOGLE_MAIL")

# Replace with your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/ask', methods=['POST'])
def ask_gpt():
    user_prompt = request.json.get("prompt", "")
    full_prompt = ("You are a helpful travel planner in Australia, based on the answers to the "
                   "questions below, construct a travel plan for the user.\n" + str(user_prompt))
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful travel planner."},
            {"role": "user", "content": full_prompt}
        ]
    )
    message_content = response.choices[0].message.content
    return jsonify({"response": message_content})

def send_email(recipient, subject, body):
    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = recipient
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.send_message(msg)

def generate_verification_code():
    return str(random.randint(100000, 999999))

@app.route('/signup', methods=['POST'])
def signup():
    username = request.json.get("username")
    password = request.json.get("password")
    email = request.json.get("username")

    # Check if user already exists
    users_ref = db.collection('users')
    user = users_ref.document(username).get()
    if user.exists:
        return jsonify({"error": "Email already exists!"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    users_ref.document(username).set({
        "username": username,
        "password": hashed_password,
        "email": email,
        "verified": False
    })

    code = generate_verification_code()
    codes_ref = db.collection('verification_codes')
    codes_ref.document(username).set({
        "username": username,
        "code": code,
        "expires_at": time.time() + 600
    })

    send_email(email, "Email Verification", f"Your verification code is: {code}")
    return jsonify({"message": "User registered successfully! Please verify your email."})

@app.route('/verify', methods=['POST'])
def verify_email():
    username = request.json.get("username")
    code = request.json.get("code")

    codes_ref = db.collection('verification_codes')
    verification_data = codes_ref.document(username).get().to_dict()
    if verification_data and verification_data["code"] == code:
        if time.time() > verification_data["expires_at"]:
            return jsonify({"error": "Verification code has expired!"}), 400
        else:
            users_ref = db.collection('users')
            user_data = users_ref.document(username).get().to_dict()
            if user_data:
                user_data["verified"] = True
                users_ref.document(username).set(user_data)
                return jsonify({"message": "Email verified successfully!"}), 200

    return jsonify({"error": "Invalid verification code!"}), 400

@app.route('/resend_verification', methods=['POST'])
def resend_verification():
    username = request.json.get("username")

    users_ref = db.collection('users')
    user_data = users_ref.document(username).get().to_dict()
    if not user_data:
        return jsonify({"error": "User not found!"}), 400

    email = user_data["email"]
    code = generate_verification_code()

    codes_ref = db.collection('verification_codes')
    codes_ref.document(username).set({
        "username": username,
        "code": code,
        "expires_at": time.time() + 600
    })

    send_email(email, "Email Verification", f"Your verification code is: {code}")
    return jsonify({"message": "Verification email resent successfully!"})

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get("username")
    password = request.json.get("password")

    users_ref = db.collection('users')
    user_data = users_ref.document(username).get().to_dict()
    if user_data and bcrypt.check_password_hash(user_data["password"], password):
        if not user_data.get("verified", False):
            return jsonify({"message": "Please verify your email before logging in!", "isVerified":False}), 200
        return jsonify({"message": "Login successful!", "isVerified":True})

    return jsonify({"error": "Invalid username or password!"}), 401

if __name__ == "__main__":
    app.run(debug=True, port=5001)
