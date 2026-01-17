import os
import uuid
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_file
from llm import get_reply
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

app = Flask(__name__)

conversation_history = []
SESSION_ID = f"ANON-{uuid.uuid4().hex[:6]}"

END_WORDS_EN = ["end", "stop", "that's all"]
END_WORDS_TE = ["చాలు", "ఆపండి"]

def generate_pdf():
    os.makedirs("reports", exist_ok=True)
    path = f"reports/{SESSION_ID}.pdf"

    c = canvas.Canvas(path, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width/2, height-50, "ANONYMOUS HARASSMENT COMPLAINT REPORT")

    c.setFont("Helvetica", 10)
    c.drawCentredString(width/2, height-70, "Confidential – Internal Use Only")

    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, height-110, "Anonymous ID:")
    c.setFont("Helvetica", 11)
    c.drawString(180, height-110, SESSION_ID)

    c.drawString(50, height-130, "Generated On:")
    c.drawString(180, height-130, datetime.now().strftime("%d %B %Y, %I:%M %p"))

    c.line(50, height-150, width-50, height-150)

    text = c.beginText(50, height-180)
    text.setFont("Helvetica", 10)
    text.setLeading(15)

    for msg in conversation_history:
        role = "Student" if msg["role"] == "user" else "Support Bot"
        text.textLine(f"{role}: {msg['content']}")
        text.textLine("")

    c.drawText(text)

    c.setFont("Helvetica-Oblique", 9)
    c.drawCentredString(
        width/2,
        40,
        "This report was generated anonymously using AI-based Harassment Support System."
    )

    c.save()
    return path

@app.route("/")
def index():
    return render_template("index.html", session_id=SESSION_ID)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    msg = data.get("message")
    lang = data.get("language", "English")

    lower = msg.lower()

    if any(w in lower for w in END_WORDS_EN) or any(w in msg for w in END_WORDS_TE):
        pdf_path = generate_pdf()
        return jsonify({
            "reply": "Your report has been generated.",
            "pdf": True
        })

    reply = get_reply(msg, conversation_history, lang)
    conversation_history.append({"role": "user", "content": msg})
    conversation_history.append({"role": "assistant", "content": reply})

    return jsonify({"reply": reply, "pdf": False})

@app.route("/download")
def download():
    return send_file(f"reports/{SESSION_ID}.pdf", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
