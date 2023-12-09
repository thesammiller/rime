import os
import re

from flask import Flask, render_template, request
from markupsafe import Markup
from openai import OpenAI

app = Flask(__name__,template_folder='./templates', static_folder='./static')

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
    # Join together the different parts of the
    reply = "".join([i.message.content  for i in chat_completion.choices])
    formatted_text = re.sub(r'```(\w+)?\s*(.*?)```', r'<pre><code>\2</code></pre>', reply, flags=re.DOTALL)
    messages.append({"role": "assistant", "content": Markup(formatted_text)})
    return render_template('form.html', comments=messages)

if __name__ == "__main__":
    app.run(app.run(debug=True, host="0.0.0.0", port=8000))
