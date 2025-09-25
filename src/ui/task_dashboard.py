
from flask import Flask, render_template
import os

app = Flask(__name__, template_folder="templates")

@app.route('/')
def dashboard():
    with open('data/logs/alex_current.log', 'r') as f:
        logs = f.read()
    return render_template('dashboard.html', logs=logs)

if __name__ == '__main__':
    os.makedirs("templates", exist_ok=True)
    with open("templates/dashboard.html", "w") as f:
        f.write("<h1>Alex Dashboard</h1><pre>{{ logs }}</pre>")
    app.run(port=5000)