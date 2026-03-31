from flask import Flask, render_template_string, send_file, request
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import pandas as pd
import os

app = Flask(__name__)

# Load students
df = pd.read_csv("UIUX.csv")
students = df["Full Name (as you want on the certificate)"].dropna().tolist()

# ---------------- UI ----------------
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
<title>GDG Certificate</title>

<style>
body {
    font-family: Arial;
    background: linear-gradient(135deg, #667eea, #764ba2);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 100vh;
    margin: 0;
    color: white;
}

.header-title {
    font-size: 38px;
    font-weight: bold;
    margin-bottom: 8px;
}

.header-subtitle {
    font-size: 16px;
    margin-bottom: 10px;
}

.badge {
    background: white;
    color: black;
    padding: 6px 12px;
    border-radius: 20px;
    margin-bottom: 25px;
}

.card {
    background: white;
    color: black;
    padding: 25px;
    border-radius: 12px;
    width: 90%;
    max-width: 400px;
    margin-top: 10px;
}

h2 {
    text-align: center;
    margin-bottom: 20px;
}

select, button {
    width: 100%;
    padding: 10px;
    margin-top: 12px;
    font-size: 16px;
    border-radius: 6px;
    border: 1px solid #ccc;
}

button {
    background: #667eea;
    color: white;
    border: none;
    cursor: poniter;
}

button:hover {
    background: #5a67d8;
}
</style>

</head>

<body>

<div class="header-title">🎨 THE UI/UX DESIGN MINDSET</div>
<div class="badge">📅 13th March | GDG On Campus MIT-A</div>

<div class="card">
<h2>🎓 Download Certificate</h2>

<form action="/download" method="post">
<select name="name" required>
<option value="">Select your name</option>
{% for student in students %}
<option value="{{student}}">{{student}}</option>
{% endfor %}
</select>

<button type="submit">Download Certificate</button>
</form>

</div>

</body>
</html>
"""

# ---------------- PDF ----------------
def generate_certificate(name):
    safe_name = name.replace(" ", "_")
    file_path = f"{safe_name}.pdf"

    pdfmetrics.registerFont(TTFont('Poppins', 'font.ttf'))
    c = canvas.Canvas(file_path, pagesize=landscape(A4))

    # Background
    c.drawImage("UIUX.png", 0, 0, width=842, height=595)

    # Name
    c.setFont("Poppins", 30)
    text_width = pdfmetrics.stringWidth(name, "Poppins", 30)
    x = (842 - text_width) / 2
    y = 294
    c.drawString(x, y, name)

    c.save()
    return file_path

# ---------------- Routes ----------------
@app.route('/')
def home():
    return render_template_string(HTML_PAGE, students=students)

@app.route('/download', methods=['POST'])
def download():
    name = request.form['name']

    if name not in students:
        return "Invalid Name!"

    file_path = generate_certificate(name)
    return send_file(file_path, as_attachment=True)

# ---------------- Run ----------------
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
