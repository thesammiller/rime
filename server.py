from flask import Flask, render_template, request
import os
from openai import OpenAI

app = Flask(__name__)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(
    api_key=OPENAI_API_KEY,
)

CHATGPT_MODEL="gpt-3.5-turbo"

messages = [ {"role": "system", "content":  
              "You are a intelligent assistant."} ] 

@app.route('/', methods=['GET', 'POST'])
def form():
    return render_template('form.html')

@app.route('/hello', methods=['GET', 'POST'])
def hello():
    message = request.form['comments']
    messages.append( 
            {"role": "user", "content": message}, 
        )
    chat_completion = client.chat.completions.create(
        messages=messages,
        model="gpt-3.5-turbo",
    )
    reply = chat_completion.choices[0].message.content
    messages.append({"role": "assistant", "content": reply})
    say_greeting=request.form['say']
    to_name=request.form['to']
    return render_template('greeting.html', comments=reply)

if __name__ == "__main__":
    app.run(app.run(debug=True, host="0.0.0.0", port=8000))
