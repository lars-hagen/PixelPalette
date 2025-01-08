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

# Style-specific prompt enhancements
STYLE_PROMPTS = {
    'natural': 'Create a natural, photorealistic image of',
    'vivid': 'Create a vibrant and colorful image of',
    'anime': 'Create an anime-style illustration of',
    'fantasy': 'Create a magical fantasy artwork of',
    'cyberpunk': 'Create a futuristic cyberpunk scene of',
    'minimalist': 'Create a clean, minimalist representation of',
    'watercolor': 'Create a delicate watercolor painting of',
    'retro': 'Create a vintage, retro-styled image of'
}

@app.route("/api/generate", methods=["POST"])
def generate_image():
    try:
        data = request.json
        prompt = data.get("prompt")
        quality = data.get("quality", "standard")
        style = data.get("style", "natural")
        
        if not prompt:
            return jsonify({"error": "No prompt provided"}), 400

        # Get style-specific prompt
        style_prefix = STYLE_PROMPTS.get(style, STYLE_PROMPTS['natural'])
        enhanced_prompt = f"{style_prefix} {prompt}"

        # Call DALL-E API
        response = openai.images.generate(
            model="dall-e-3",
            prompt=enhanced_prompt,
            size="1024x1024",
            quality=quality,
            n=1,
            style=style if style in ['natural', 'vivid'] else 'natural'  # DALL-E only supports natural/vivid
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