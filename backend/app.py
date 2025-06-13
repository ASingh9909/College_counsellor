from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests
# from dotenv import load_dotenv # We'll use this later if you set up a .env file

# Load environment variables (if you use a .env file)
# load_dotenv()

app = Flask(__name__)
CORS(app) # Enable CORS for all routes, allowing frontend to call backend

# Novita AI Configuration
NOVITA_API_BASE_URL = os.getenv('NOVITA_API_BASE_URL', 'https://api.novita.ai/v3/openai')
NOVITA_API_KEY = os.getenv('NOVITA_API_KEY') # You'll need to set this environment variable
NOVITA_MODEL = "deepseek/deepseek-r1-0528"

@app.route('/')
def home():
    return "Career Counsellor Backend is running!"

@app.route('/api/counsel', methods=['POST'])
def get_college_suggestions():
    if not NOVITA_API_KEY:
        return jsonify({'error': 'Novita AI API key is not configured.'}), 500

    try:
        student_data = request.json
        if not student_data:
            return jsonify({'error': 'No student data provided.'}), 400

        # Construct the prompt for Novita AI based on student_data
        # This is a simplified example. You'll need to craft a more detailed prompt.
        user_prompt_content = f"Based on the following student profile, suggest suitable colleges:\n"
        user_prompt_content += f"GPA: {student_data.get('gpa', 'N/A')}\n"
        user_prompt_content += f"Interests: {student_data.get('interests', 'N/A')}\n"
        user_prompt_content += f"Projects: {student_data.get('projects', 'N/A')}\n"
        user_prompt_content += f"Extracurriculars: {student_data.get('extracurriculars', 'N/A')}\n"
        user_prompt_content += f"About: {student_data.get('about', 'N/A')}"

        payload = {
            "model": NOVITA_MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": "You are an expert career counsellor specializing in college admissions. Provide a list of suitable colleges based on the student's profile."
                },
                {
                    "role": "user",
                    "content": user_prompt_content
                }
            ],
            "response_format": { "type": "text" }
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {NOVITA_API_KEY}"
        }

        response = requests.post(f"{NOVITA_API_BASE_URL}/chat/completions", json=payload, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)

        novita_response = response.json()
        # Assuming the response structure is like OpenAI's, where the content is in choices[0].message.content
        # You might need to adjust this based on Novita AI's actual response structure
        if novita_response.get('choices') and len(novita_response['choices']) > 0:
            suggestion = novita_response['choices'][0].get('message', {}).get('content', 'No suggestion provided.')
        else:
            suggestion = 'Could not retrieve suggestion from Novita AI.'
            app.logger.error(f"Novita AI response format unexpected: {novita_response}")

        return jsonify({'suggestion': suggestion})

    except requests.exceptions.RequestException as e:
        app.logger.error(f"Error calling Novita AI: {e}")
        return jsonify({'error': f'Failed to connect to Novita AI: {str(e)}'}), 503 # Service Unavailable
    except Exception as e:
        app.logger.error(f"An unexpected error occurred: {e}")
        return jsonify({'error': f'An unexpected error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    # It's recommended to set the port via an environment variable for flexibility
    port = int(os.environ.get('PORT', 5001)) 
    app.run(debug=True, port=port)