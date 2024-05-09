from flask import Flask, render_template, request
import random
import google.generativeai as genai

app = Flask(__name__)

# Dummy API key - replace with your actual key.
API_KEY = "xxxxxxxxx"
genai.configure(api_key=API_KEY)

# File to String
def file_to_string(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return "The file was not found."
    except Exception as e:
        return f"An error occurred: {e}"

# Load job descriptions from files (simulated here as strings for demonstration).
job_1 = file_to_string("job_1.txt")
job_2 = file_to_string("job_2.txt")
job_3 = file_to_string("job_3.txt")
job_4 = file_to_string("job_4.txt")
job_5 = file_to_string("job_5.txt")
all_jobs = [job_1, job_2, job_3, job_4, job_5]

# Set up the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 0,
    "max_output_tokens": 8192,
}
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]
model = genai.GenerativeModel(model_name="gemini-1.0-pro-latest",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

@app.route('/', methods=['GET', 'POST'])
def index():
    display_output = ""
    position_var = request.form.get('position', '')
    paygrade_var = request.form.get('paygrade', '')
    additional_details_var = request.form.get('additional_details', '')

    if request.method == 'POST':
        job_prompt = ("Make a verbose Department of Energy position description for the following position add extra info to make it more convincing if necessary --" + position_var +
                      " the paygrade for this position is " + paygrade_var +
                      " Here are additional details for this position these must be in the response no matter what but in a professional way--- " + additional_details_var +
                      " Use the following example as a format for creating this position description---" + random.choice(all_jobs))

        convo = model.start_chat(history=[
            {"role": "user", "parts": [job_prompt]},
            {"role": "model", "parts": ["Hello! 👋 How can I help you today?"]}
        ])
        convo.send_message("YOUR_USER_INPUT")
        display_output = convo.last.text

    # Pass the variables back to the template to maintain their state in the form
    return render_template('index.html', output=display_output, position=position_var, paygrade=paygrade_var, additional_details=additional_details_var)

if __name__ == '__main__':
    app.run(debug=True)

