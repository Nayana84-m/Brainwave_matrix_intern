from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
import os

app = Flask(__name__)
CSV_FILE = 'wellness_data.csv'

if not os.path.exists(CSV_FILE):
    pd.DataFrame(columns=["name", "sleep_hours", "stress_level", "activity", "day"]).to_csv(CSV_FILE, index=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        sleep = float(request.form['sleep_hours'])
        stress = int(request.form['stress_level'])
        activity = request.form['activity']
        day = request.form['day']

        new_entry = pd.DataFrame([[name, sleep, stress, activity, day]], 
                                 columns=["name", "sleep_hours", "stress_level", "activity", "day"])
        new_entry.to_csv(CSV_FILE, mode='a', header=False, index=False)

        return render_template('wellness_form.html', message="Thank you for submitting!")
    return render_template('wellness_form.html', message='')

@app.route('/summary')
def summary():
    if not os.path.exists(CSV_FILE) or os.path.getsize(CSV_FILE) == 0:
        return "No data available yet. Please submit the form first."

    df = pd.read_csv(CSV_FILE)
    if "day" not in df.columns or "stress_level" not in df.columns:
        return "Required data columns not found."

    plt.figure(figsize=(8, 4))
    df.groupby("day")["stress_level"].mean().plot(kind='bar', color='skyblue')
    plt.title("Average Stress Level by Day")
    plt.ylabel("Stress Level")
    plt.xlabel("Day")
    plt.tight_layout()
    plt.savefig(STATIC_IMAGE)
    return render_template("summary.html", image_file=STATIC_IMAGE)

if __name__ == '__main__':
    app.run(debug=True)
