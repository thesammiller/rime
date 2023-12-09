import os
import re
import time

from flask import Flask, render_template, request
from markupsafe import Markup
from openai import OpenAI

app = Flask(__name__,template_folder='./templates', static_folder='./static')

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ROOT_DIR="conversations/"
CHATGPT_MODEL="gpt-3.5-turbo"
STARTING_MESSAGE="You are an intelligent assistant."
# To avoid the 4097 token size limit
# "Token" can be variable number of characters
CHARACTER_SIZE_LIMIT=20096

client = OpenAI(
    api_key=OPENAI_API_KEY,
)

messages = [ {"role": "system", "content": STARTING_MESSAGE} ]


def check_for_message_from_user(req):
    return request.form['messages'] if req.form.get('messages') else STARTING_MESSAGE


def save_message_history_from_chatgpt():
    filename = f"{time.time()}.txt"
    with open(ROOT_DIR + filename, "w") as f:
        for m in messages:
            f.write('{role} - {content}\n\n'.format(**m))
    return filename


# Check if the conversation history is too long
def messages_are_outside_token_limit():
    return len("".join([m['content'] for m in messages])) > (CHARACTER_SIZE_LIMIT)


def save_message_history():
    filename = f"{time.time()}.txt"
    with open(ROOT_DIR + filename, "w") as f:
        for m in messages:
            f.write("{role} - {content}\n\n".format(**m))

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
    # Token length is variable, but 22k is a good character count
    if messages_are_outside_token_limit():
        # Summarize the conversation if it's too long
        try:
            save_message_history()
            summary_response = summarize_current_conversation()
            # Re-initialize Messages with summary and next message from user
            messages = [{'role': 'system', 'content': summary_response},
                        {'role': 'user', 'content': message}]
        except Exception as e:
            print(f"Error during summarization: {e}")
            return "Error occurred while summarizing the conversation."

    # Send the updated conversation to ChatGPT
    try:
        chat_completion = client.chat.completions.create(
            messages=messages,
            model=CHATGPT_MODEL,
        )
        return "".join([i.message.content for i in chat_completion.choices])
    except Exception as e:
        print(f"Error during sending message: {e}")
        return "Error occurred while sending the message."


def format_text_with_code(reply):
    return Markup(re.sub(r'```(\w+)?\s*(.*?)```', r'<pre><code>\2</code></pre>', reply, flags=re.DOTALL))


@app.route('/', methods=['GET', 'POST'])
def home():
    message = check_for_message_from_user(request)
    messages.append(
           {"role": "user", "content": message},
        )
    reply = send_message_to_chatgpt(message)
    formatted_text = format_text_with_code(reply)
    messages.append({"role": "assistant", "content": formatted_text})
    return render_template('form.html', messages=messages)

if __name__ == "__main__":
    app.run(app.run(debug=True, host="0.0.0.0", port=8000))
