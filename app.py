from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

def save_reflection(gratitude, message, kind_work):
    with open("reflections.txt", "a") as file:
        file.write(f"Gratitude for Today: {gratitude}\n")
        file.write(f"Message for Future You: {message}\n")
        file.write(f"Kind Work You Did: {kind_work}\n")
        file.write("-" * 40 + "\n")

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        gratitude = request.form.get("gratitude")
        message = request.form.get("message")
        kind_work = request.form.get("kind_work")

        if gratitude and message and kind_work:
            save_reflection(gratitude, message, kind_work)  # Save or process the reflection data
            return render_template("index.html", success=True)
        else:
            return render_template("index.html", error="Please fill in all fields!")

    return render_template("index.html")

@app.route('/garden')
def garden():
    reflections = []

    if os.path.exists('reflections.txt'):
        with open('reflections.txt', 'r') as file:
            reflections_data = file.readlines()

            for i in range(0, len(reflections_data), 4):
                if i + 2 < len(reflections_data):
                    if "Gratitude for Today:" in reflections_data[i] and \
                       "Message for Future You:" in reflections_data[i+1] and \
                       "Kind Work You Did:" in reflections_data[i+2]:

                        gratitude = reflections_data[i].strip().split(": ", 1)[1]
                        message = reflections_data[i+1].strip().split(": ", 1)[1]
                        kind_work = reflections_data[i+2].strip().split(": ", 1)[1]

                        reflection = {
                            "gratitude": gratitude,
                            "message": message,
                            "kind_work": kind_work
                        }
                        reflections.append(reflection)

    reflections.reverse()

    return render_template('garden.html', reflections=reflections)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
