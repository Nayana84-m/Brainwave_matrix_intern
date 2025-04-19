from flask import Flask,
render_template, request
import pandas as pd
import matplotlib.pyplot as plt
import os
import io
import base64

app = Flask(__name__)
CSV_FILE = 'wellness_data.csv'

# Map feelings to stress level
feeling_to_stress = {
    "Very Relaxed": 1,
    "Relaxed": 3,
    "Neutral": 5,
    "Tired": 6,
    "Stressed": 8,
    "Very Stressed": 10
}

# Create CSV file with required columns if it doesn't exist
if not os.path.exists(CSV_FILE):
    pd.DataFrame(columns=["name", "sleep_hours", "stress_level", "activity", "day"]).to_csv(CSV_FILE, index=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        sleep = float(request.form['sleep_hours'])
        feeling = request.form['feeling']
        stress = feeling_to_stress.get(feeling, 5)  # Default to 5 if unknown
        activity = request.form['activity']
        day = request.form['day']

        # Save to CSV
        new_entry = pd.DataFrame([[name, sleep, stress, activity, day]],
                                 columns=["name", "sleep_hours", "stress_level", "activity", "day"])
        new_entry.to_csv(CSV_FILE, mode='a', header=False, index=False)
        return render_template('wellness_form.html', message="Thank you for submitting!")
    return render_template('wellness_form.html', message='')

@app.route('/summary')
def summary():
    try:
        df = pd.read_csv(CSV_FILE)
        if df.empty:
            return "CSV file is empty."

        # Graph for average stress level per day
        img = io.BytesIO()
        df.groupby("day")["stress_level"].mean().reindex(
            ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        ).plot(kind='bar', color='#64b5f6')
        plt.title("Average Stress Level per Day")
        plt.ylabel("Stress Level (0-10)")
        plt.ylim(0, 10)
        plt.tight_layout()
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode('utf-8')

        # Suggest activities for high stress levels
        avg_stress = df["stress_level"].mean()
        if avg_stress >= 8:
            suggestions = ["Meditation", "Go for a walk", "Listen to music", "Talk to a friend"]
        elif avg_stress >= 5:
            suggestions = ["Light exercise", "Journaling", "Take deep breaths", "Watch a favorite movie"]
        else:
            suggestions = ["Keep up the good work!", "Maintain balance", "Enjoy relaxing activities"]

        return render_template("summary.html", plot_url=plot_url, suggestions=suggestions)

    except Exception as e:
        return f"Error generating summary: {e}"
