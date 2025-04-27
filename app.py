from flask import Flask, render_template, request, redirect
import os
import sqlite3

app = Flask(__name__)

def save_reflection(gratitude, message, wish):
    conn = sqlite3.connect('reflections.db')
    c = conn.cursor()
    c.execute('INSERT INTO reflections (gratitude, message, wish) VALUES (?, ?, ?)',
              (gratitude, message, wish))
    conn.commit()
    conn.close()

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        gratitude = request.form.get("gratitude")
        message = request.form.get("message")
        wish = request.form.get("wish")

        if gratitude and message and wish:
            save_reflection(gratitude, message, wish)
            return render_template("index.html", success=True)
        else:
            return render_template("index.html", error="Please fill the fields.")

    return render_template("index.html")

@app.route('/garden')
def garden():
    conn = sqlite3.connect('reflections.db')
    c = conn.cursor()
    c.execute('SELECT gratitude, message, wish FROM reflections')
    reflections = c.fetchall()
    conn.close()
    return render_template('garden.html', reflections=reflections)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
