from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from openai import OpenAI # Changed from requests to OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app) # Enable CORS for all routes, allowing frontend to call backend

# Novita AI Configuration
NOVITA_API_BASE_URL = os.getenv('NOVITA_API_BASE_URL', 'https://api.novita.ai/v3/openai')
NOVITA_API_KEY = os.getenv('NOVITA_API_KEY') # You'll need to set this environment variable
NOVITA_MODEL = "meta-llama/llama-3.2-1b-instruct"

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

        client = OpenAI(
            base_url=NOVITA_API_BASE_URL,
            api_key=NOVITA_API_KEY,
        )

        user_prompt_content = f"Based on the following student profile, suggest suitable colleges:\n"
        user_prompt_content += f"GPA: {student_data.get('gpa', 'N/A')}\n"
        user_prompt_content += f"Interests: {student_data.get('interests', 'N/A')}\n"
        user_prompt_content += f"Projects: {student_data.get('projects', 'N/A')}\n"
        user_prompt_content += f"Extracurriculars: {student_data.get('extracurriculars', 'N/A')}\n"
        user_prompt_content += f"About: {student_data.get('about', 'N/A')}"

        # Using the NOVITA_MODEL variable which was updated previously
        # The sample code uses stream=True, but for a simple API response, stream=False is usually preferred.
        # If streaming is desired, the frontend and this backend logic would need to be adapted.
        # For now, let's assume non-streaming for simplicity in a typical API request/response.
        chat_completion_res = client.chat.completions.create(
            model=NOVITA_MODEL, # Using the globally defined and updated model
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert career counsellor specializing in college admissions. Provide a list of suitable colleges based on the student's profile."
                },
                {
                    "role": "user",
                    "content": user_prompt_content
                }
            ],
            stream=False, # Set to False for a single response, True if streaming is intended and handled
            max_tokens=512 # As per sample code
        )

        if chat_completion_res.choices and len(chat_completion_res.choices) > 0:
            suggestion = chat_completion_res.choices[0].message.content
        else:
            suggestion = 'Could not retrieve suggestion from Novita AI.'
            app.logger.error(f"Novita AI response format unexpected: {chat_completion_res}")

        return jsonify({'suggestion': suggestion})

    # Catching OpenAI specific errors if any, and general exceptions
    except Exception as e: # Broad exception for now, can be refined to catch specific OpenAI API errors
        app.logger.error(f"Error calling Novita AI (OpenAI SDK): {e}")
        # It's good practice to return a more generic error to the client for security.
        return jsonify({'error': f'An error occurred while processing your request.'}), 500

if __name__ == '__main__':
    # It's recommended to set the port via an environment variable for flexibility
    port = int(os.environ.get('PORT', 5001)) 
    app.run(debug=True, port=port)