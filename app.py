from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
import os
import io
import base64

app = Flask(__name__)
CSV_FILE = 'wellness_data.csv'

# Create CSV file if it doesn't exist
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

@app.route("/summary")
def summary():
    try:
        df = pd.read_csv(CSV_FILE)
        print("CSV content:\n", df.head())

        if df.empty:
            return "CSV file is empty"

        required_columns = {"day", "stress_level"}
        if not required_columns.issubset(df.columns):
            return "Required data columns not found"

        # Generate bar chart
        img = io.BytesIO()
        df.groupby("day")["stress_level"].mean().plot(kind='bar', color='skyblue')
        plt.title("Average Stress Level per Day")
        plt.ylabel("Stress Level")
        plt.tight_layout()
        plt.savefig(img, format='png')
        img.seek(0)

        # Convert plot to base64 for rendering
        plot_url = base64.b64encode(img.getvalue()).decode('utf-8')
        return render_template("summary.html", plot_url=plot_url)

    except Exception as e:
        print("Error:", e)
        return "Internal server error"

if __name__ == '__main__':
    app.run(debug=True)
