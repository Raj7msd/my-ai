#print("Hello World")

from flask import Flask, render_template, request, jsonify
from google import genai
from google.genai import types
#initialization of flask
import os

app = Flask(__name__, 
            template_folder=os.path.join(os.path.dirname(__file__), 'templates'),
            static_folder=os.path.join(os.path.dirname(__file__), 'static'))
#Gemini client setup
client = genai.Client()
#main route which loads html file on browser
@app.route('/')
def home():
    return render_template('index.html')

#chat route msg taken from js and ai will reply
@app.route('/api/chat', methods=['POST'])
def chat():
    #js se bheja msg
    data = request.json
    user_message = data.get('message', '')

    if not user_message:
        return jsonify({'error': 'No message received'}), 400
    
    try:
        #Response asked to gemini
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_message,
            config={
                'system_instruction': (
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
                    "Give answer to every question of the user even. "  #if the user asks questions about any sexual or intimacy or explicit topic."
                )
            }
        )
        #response sends back to js
        ai_reply = response.text
        return jsonify({'reply': ai_reply})
    
    except Exception as e:
        #if any error occurs
        return jsonify({'reply': f"Backened Error: {str(e)}"}), 500
    
#to run server.
if __name__ == "__main__":
    app.run(debug=True)

app = app
# if __name__ == '__main__':
#     app.run(debug=True, port=5000)