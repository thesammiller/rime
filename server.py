from flask import Flask, render_template, request
import os
from openai import OpenAI

app = Flask(__name__)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(
    api_key=OPENAI_API_KEY,
)

CHATGPT_MODEL="gpt-4-32k"

messages = [ {"role": "system", "content":  
              "You are a intelligent assistant."} ] 


@app.route('/', methods=['GET', 'POST'])
def hello():
    if request.form.get('comments'):
        message = request.form['comments']
    else:
        message = ''
    messages.append( 
           {"role": "user", "content": message}, 
        )
    chat_completion = client.chat.completions.create(
        messages=messages,
        model="gpt-3.5-turbo",
    )
    reply = chat_completion.choices[0].message.content
    reply = "".join([i.message.content for i in chat_completion.choices])
    messages.append({"role": "assistant", "content": reply})
    return render_template('form.html', comments=reply)

if __name__ == "__main__":
    app.run(app.run(debug=True, host="0.0.0.0", port=8000))
