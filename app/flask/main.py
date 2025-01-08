from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configure OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/api/generate", methods=["POST"])
def generate_image():
    try:
        data = request.json
        prompt = data.get("prompt")
        
        if not prompt:
            return jsonify({"error": "No prompt provided"}), 400

        # Call DALL-E API
        response = openai.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )

        return jsonify({
            "url": response.data[0].url,
            "revised_prompt": response.data[0].revised_prompt
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy"})

if __name__ == "__main__":
    app.run(debug=True) 