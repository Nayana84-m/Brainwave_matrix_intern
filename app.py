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
        if __name__ == "__main__":
            app.run(debug=True)
    return render_template('wellness_form.html', message='')

@app.route('/summary')
def summary():
    df = pd.read_csv(CSV_FILE)
    if df.empty:
        return "No data available yet."

    df.groupby("day")["stress_level"].mean().plot(kind='bar', color='skyblue')
    plt.ylabel("Avg Stress Level")
    plt.title("Average Stress Level per Day")
    plt.tight_layout()
    plt.savefig("static/summary.png")
    plt.clf()

    return '<h3>Average Stress Level per Day</h3><img src="/static/summary.png"/>'

if _name_ == '_main_':
    app.run(debug=True)
