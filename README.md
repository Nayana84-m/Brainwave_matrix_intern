Student Stress Level Visualization App

Description:
A Flask web app to visualize student stress levels over time using a bar chart. Users can input their daily stress data (low, medium, high) and see their stress levels plotted.

Technologies Used:
Flask (Web Framework)
Matplotlib (Charts & Visualizations)
Pandas (Data Handling)
Gunicorn (WSGI Server for Production)

Setup
1. Clone the Repo:
git clone https://github.com/Nayana84-m/Brainwave_Matrix_Intern.git
cd Brainwave_Matrix_Intern

2. Create a Virtual Environment:
python -m venv venv
source venv/bin/activate  

3. Install Dependencies:
pip install -r requirements.txt

4. Run the App Locally:
flask run
Visit http://localhost:5000 in your browser.

---
Project Structure:

Brainwave_Matrix_Intern/
│
├── app.py           # Flask app
├── requirements.txt # Dependencies
├── templates/       # HTML files
│   ├── index.html
│   └── summary.html
└── static/          # Static files (CSS)

Contributing-
Feel free to fork, make changes, and create a pull request.
