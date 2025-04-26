from flask import Flask, render_template, request, redirect
import os

app = Flask(__name__)

def save_reflection(gratitude, message, wish):
    with open("reflections.txt", "a") as file:
        file.write(f"Gratitude for Today: {gratitude}\n")
        file.write(f"One positive affirmation: {message}\n")
        file.write(f"A Wish I'm sending to Universe: {wish}\n")
        file.write("\n")

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
    reflections = []

    if os.path.exists('reflections.txt'):
        with open('reflections.txt', 'r') as file:
            reflections_data = file.readlines()

            for i in range(0, len(reflections_data), 4):
                if i + 2 < len(reflections_data):
                    if "Gratitude for Today:" in reflections_data[i] and \
                       "One positive affirmation:" in reflections_data[i+1] and \
                       "A Wish I'm sending to Universe:" in reflections_data[i+2]:

                        gratitude = reflections_data[i].strip().split(": ", 1)[1]
                        message = reflections_data[i+1].strip().split(": ", 1)[1]
                        wish = reflections_data[i+2].strip().split(": ", 1)[1]

                        reflection = {
                            "gratitude": gratitude,
                            "message": message,
                            "wish": wish
                        }
                        reflections.append(reflection)
                        print (reflections)

    reflections.reverse()

    return render_template('garden.html', reflections=reflections)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
