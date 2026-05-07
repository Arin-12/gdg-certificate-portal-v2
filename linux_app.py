from flask import Flask, render_template_string, send_file, request
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import pandas as pd
import os

app = Flask(__name__)

# Load students
df = pd.read_csv("linux_data.csv")
students = df["Name"].dropna().tolist()

# ---------------- UI ----------------
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
<title>GDG Certificate</title>

<style>
body {
    font-family: Arial;
    background: linear-gradient(135deg, #141E30, #243B55);
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
    text-align: center;
}

.header-subtitle {
    font-size: 16px;
    margin-bottom: 10px;
    text-align: center;
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
    padding: 35px;
    border-radius: 12px;
    width: 90%;
    max-width: 500px;
    margin-top: 10px;
}

h2 {
    text-align: center;
    margin-bottom: 20px;
}

input, button {
    width: 100%;
    padding: 10px;
    margin-top: 12px;
    font-size: 16px;
    border-radius: 6px;
    border: 1px solid #ccc;
    box-sizing: border-box;
}

button {
    background: #2d8f5a;
    color: white;
    border: none;
    cursor: pointer;
}

button:hover {
    background: #26774b;
}

.suggestions {
    background: white;
    border: 1px solid #ccc;
    max-height: 150px;
    overflow-y: auto;
    margin-top: 5px;
    border-radius: 6px;
}

.suggestions div {
    padding: 8px;
    cursor: pointer;
}

.suggestions div:hover {
    background: #eee;
}
</style>

</head>

<body>

<div class="header-title">🐧 LINUX UNLOCKED</div>
<div class="header-subtitle">Hands-on Linux Workshop</div>
<div class="badge">📅 24th April | GDG On Campus MIT-A × Red Hat Academy</div>

<div class="card">
<h2>🎓 Download Certificate</h2>

<form action="/download" method="post">

<input type="text" id="searchBox" placeholder="Search your name..." autocomplete="off" required>
<input type="hidden" name="name" id="selectedName">

<div id="suggestions" class="suggestions"></div>

<button type="submit">Download Certificate</button>

</form>

</div>

<script>
const students = {{ students | tojson }};
const searchBox = document.getElementById("searchBox");
const suggestions = document.getElementById("suggestions");
const selectedName = document.getElementById("selectedName");

searchBox.addEventListener("input", function() {
    let value = this.value.toLowerCase();
    suggestions.innerHTML = "";

    if (value === "") return;

    let filtered = students.filter(name =>
        name.toLowerCase().includes(value)
    );

    filtered.slice(0, 5).forEach(name => {
        let div = document.createElement("div");
        div.innerText = name;

        div.onclick = () => {
            searchBox.value = name;
            selectedName.value = name;
            suggestions.innerHTML = "";
        };

        suggestions.appendChild(div);
    });
});
</script>

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
    c.drawImage("LINUX.png", 0, 0, width=842, height=595)

    # Name
    c.setFont("Poppins", 30)
    c.setFillColorRGB(0.16, 0.16, 0.47)

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