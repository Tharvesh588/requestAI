from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Set your API key and API request URL
GOOGLE_API_KEY = "AIzaSyD1BYgSqmwXC73CpRtjet1c6FemX9mUf2U"
API_REQUEST_URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={GOOGLE_API_KEY}"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_prompt = request.form.get("prompt")

        # Prepare the data for the API request
        request_data = {
            "contents": [
                {
                    "role": "user",
                    "parts": [
                        {"text": user_prompt}
                    ]
                }
            ]
        }

        headers = {"Content-Type": "application/json"}

        try:
            response = requests.post(API_REQUEST_URL, headers=headers, json=request_data)
            response.raise_for_status()  # Check for request errors

            response_data = response.json()

            # Extract content from the response
            response_text = response_data.get('candidates', [])[0].get('content', {}).get('parts', [])[0].get('text', '')

            return jsonify({"response": response_text})

        except requests.exceptions.RequestException as e:
            return jsonify({"error": str(e)})

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
