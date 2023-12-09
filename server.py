from flask import Flask, render_template, request

app = Flask(__name__)



@app.route('/', methods=['GET', 'POST'])
def form():
    return render_template('form.html')

@app.route('/hello', methods=['GET', 'POST'])
def hello():
    say_greeting=request.form['say']
    to_name=request.form['to']
    comments=request.form['comments']
    return render_template('greeting.html', say=say_greeting, to=to_name, comments=comments)

if __name__ == "__main__":
    app.run(app.run(debug=True, host="0.0.0.0", port=8000))
