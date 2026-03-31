from flask import Flask, render_template_string, send_file, request
from PIL import Image, ImageDraw, ImageFont
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
    <title>GDG Certificate Download</title>
    <style>
        body {
            font-family: Arial;
            background: linear-gradient(135deg, #667eea, #764ba2);
            text-align: center;
            padding: 50px;
            color: white;
        }

        .header-title {
            font-size: 36px;
            font-weight: bold;
        }

        .badge {
            display: inline-block;
            background: white;
            color: black;
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 14px;
            margin-bottom: 30px;
        }

        .card {
            background: white;
            color: black;
            padding: 30px;
            border-radius: 12px;
            width: 400px;
            margin: auto;
        }

        select, button {
            width: 100%;
            padding: 12px;
            margin-top: 15px;
            font-size: 16px;
            border-radius: 6px;
        }

        button {
            background: #667eea;
            color: white;
            border: none;
            cursor: pointer;
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
    <h2>🎓 Download Your Certificate</h2>

    <form action="/download" method="post">
        <select name="name" required>
            <option value="">Select Your Name</option>
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

# ---------------- Certificate ----------------
def generate_certificate(name):
    try:
        img = Image.open("UIUX.png")
        draw = ImageDraw.Draw(img)

        font = ImageFont.truetype("font.ttf", 55)

        bbox = draw.textbbox((0, 0), name, font=font)
        text_width = bbox[2] - bbox[0]

        x = (img.width - text_width) // 2
        y = 500

        draw.text((x, y), name, fill=(30,30,80), font=font)

        safe_name = name.replace(" ", "_")
        file_path = f"{safe_name}.pdf"

        img.save(file_path)

        return file_path

    except Exception as e:
        return str(e)

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

    if not os.path.exists(file_path):
        return f"Error: {file_path}"

    return send_file(file_path, as_attachment=True)

# ---------------- Run ----------------
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)