from flask import Flask, request, jsonify
import openai
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Replace with your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/ask', methods=['POST'])
def ask_gpt():
    # Get the prompt from POST request
    user_prompt = request.json.get("prompt", "")

    # Construct the new prompt
    full_prompt = ("You are a helpful travel planner in Australia, based on the answers to the "
                   "questions below, construct a travel plan for the user.\n" + str(user_prompt))

    # Send it to ChatGPT and get the response
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful travel planner."},
            {"role": "user", "content": full_prompt}
        ]
    )

    # Extract the message content from the response
    message_content = response.choices[0].message.content

    # Return as a JSON response
    return jsonify({"response": message_content})

if __name__ == "__main__":
    app.run(debug=True, port=5001)
