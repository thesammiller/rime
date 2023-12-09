import os
import re
import time

from flask import Flask, render_template, request
from markupsafe import Markup
from openai import OpenAI

app = Flask(__name__, template_folder='./templates', static_folder='./static')

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TALK_DIR = "conversations/"
CODE_DIR = "code/"
CHATGPT_MODEL = "gpt-3.5-turbo"
STARTING_MESSAGE = "You are an intelligent assistant."
CHARACTER_SIZE_LIMIT = 18000

client = OpenAI(api_key=OPENAI_API_KEY)

messages = [{"role": "system", "content": STARTING_MESSAGE}]


def check_for_message_from_user(req):
    return request.form.get('messages', STARTING_MESSAGE)


def save_message_history_from_chatgpt():
    filename = f"{time.time()}.txt"
    with open(f"{TALK_DIR}{filename}", "w") as f:
        for m in messages:
            f.write(f"{m['role']} - {m['content']}\n\n")
    return filename


def messages_are_outside_token_limit():
    return len("".join([m['content'] for m in messages])) > CHARACTER_SIZE_LIMIT


def save_message_history():
    filename = f"{time.time()}.txt"
    with open(f"{TALK_DIR}{filename}", "w") as f:
        for m in messages:
            f.write(f"{m['role']} - {m['content']}\n\n")


def summarize_current_conversation():
    all_messages = "".join([m['content'] for m in messages])
    previous_conversation = "Summarize the following in one paragraph: " + all_messages
    summary_messages = [{'role': 'system', 'content': previous_conversation}]
    chat_completion = client.chat.completions.create(
        messages=summary_messages,
        model=CHATGPT_MODEL,
    )
    return "".join([i.message.content for i in chat_completion.choices])


def send_message_to_chatgpt(message):
    global messages
    if messages_are_outside_token_limit():
        try:
            save_message_history()
            summary_response = summarize_current_conversation()
            messages = [{'role': 'system', 'content': summary_response},
                        {'role': 'user', 'content': message}]
        except Exception as e:
            print(f"Error during summarization: {e}")
            return "Error occurred while summarizing the conversation."

    try:
        chat_completion = client.chat.completions.create(
            messages=messages,
            model=CHATGPT_MODEL,
        )
        return "".join([i.message.content for i in chat_completion.choices])
    except Exception as e:
        print(f"Error during sending message: {e}")
        return "Error occurred while sending the message."

def strip_out_language_and_code(reply):
    return re.findall(r'```(\w+)?\s*(.*?)```', reply, flags=re.DOTALL)

def format_text_with_code(reply):
    return Markup(re.sub(r'```(\w+)?\s*(.*?)```', r'<pre><code>\2</code></pre>', reply, flags=re.DOTALL))

def save_code(code):
    if len(code) != 2:
         return
    language, program = code
    file_ext = ''
    if language == 'python':
        file_ext = 'py'
    if language == 'coq':
        file_ext = 'v'
    filename = f"{time.time()}.{file_ext}"
    with open(f"{CODE_DIR}{filename}", "w") as f:
        f.write(program)
    return filename


def check_reply_for_code_and_save(reply):
    code_chunks = strip_out_language_and_code(reply)
    files_created = []
    if len(code_chunks) == 0:
        return []
    primary_language = code_chunks[0][0]
    primary_chunk = ''.join([code[1] for code in code_chunks if code[0] == primary_language])
    for code in code_chunks:
        if code[0] != primary_language:
            filename = save_code(code)
            files_created.append(filename)
    filename = save_code((primary_language, primary_chunk))
    files_created.append(filename)
    return files_created


@app.route('/', methods=['GET', 'POST'])
def home():
    message = check_for_message_from_user(request)
    messages.append({"role": "user", "content": message})
    reply = send_message_to_chatgpt(message)
    files = check_reply_for_code_and_save(reply)
    formatted_text = format_text_with_code(reply)
    messages.append({"role": "assistant", "content": formatted_text})
    return render_template('form.html', messages=messages)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
    