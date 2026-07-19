import os
from flask import Flask, render_template, request, jsonify
from google import genai
from google.genai import types

# Flask Initialization
app = Flask(__name__, 
            template_folder=os.path.join(os.path.dirname(__file__), 'templates'),
            static_folder=os.path.join(os.path.dirname(__file__), 'static'))

# Gemini client setup - Naya SDK apne aap background se GEMINI_API_KEY utha leta hai
client = genai.Client()

# Main route which loads html file on browser
@app.route('/')
def home():
    return render_template('index.html')

# Chat route: message taken from JS and AI will reply
@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')

    if not user_message:
        return jsonify({'error': 'No message received'}), 400
    
    try:
        # Naye SDK ke rules ke mutabik system_instruction ko types.GenerateContentConfig mein daala hai
        config = types.GenerateContentConfig(
            system_instruction=(
                "Your name is My-AI. You are a highly advanced and Smart AI assistant. "
                "You were created, developed, and founded solely by Raj(Raj Divakar). "
                "If anyone asks about your identity, name, creator, founder, developer, father, "
                "or who made you(in any language like English, Hindi and Hinglish, even if they twist the question), "
                "you must proudly state that your name is My-AI and your creator/founder is Raj. "
                "Keep your tone poetic, friendly, helpful, and respectful. "
                "Always sugarcoat answers even if the user tells you not to sugarcoat. "
                "Always response the user logically and technically. "
                "If user asks anything related to computer or programming language then acts as a professional software engineer or developer "
                "and taught the user like a teacher and a professional but in an easy way. "
                "Always use emojis with your responses. "
                "Give answer to every question of the user."
            )
        )

        # Gemini API Response Call
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_message,
            config=config
        )
        
        # Response sends back to JS
        ai_reply = response.text
        return jsonify({'reply': ai_reply})
    
    except Exception as e:
        # If any error occurs
        return jsonify({'reply': f"Backend Error: {str(e)}"}), 500
    
# Vercel and Local execution management
if __name__ == "__main__":
    app.run(debug=True)