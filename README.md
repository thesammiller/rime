
# Rime

This is a simple, HTML-based chatbot interface for ChatGPT.

Features include:
- Code formatting.
- Saved message history.

## Installation

This project requires Python3 and the following libraries, which can be installed with `pip3`:

`pip3 install openai`

`pip3 install flask`

Please create a folder for message history to be saved. The default is `conversations` but can be updated in the `ROOT_DIR` variable in `server.py`.

## Running
Set the environment variable `OPENAI_API_KEY` with the appropriate OpenAI API Key.

Run `python3 server.py`.

Navigate to `localhost:8000`

## Design Philosophy

Proudly, and poorly, supporting the philosophy of [HTML First](https://html-first.com/).

Flask was chosen due to [Mozilla docs](https://developer.mozilla.org/en-US/docs/Learn/Forms/Sending_and_retrieving_form_data).

