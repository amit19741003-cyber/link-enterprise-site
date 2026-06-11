from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import requests
import os

app = Flask(__name__)

# PostgreSQL / Neon Database Configuration
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# =========================
# DATABASE MODEL
# =========================
class WhatsAppMessage(db.Model):
    __tablename__ = "whatsapp_messages"

    id = db.Column(db.BigInteger, primary_key=True)
    mobile_number = db.Column(db.String(20), nullable=False)
    message_text = db.Column(db.Text)
    direction = db.Column(db.String(10), nullable=False)
    message_type = db.Column(db.String(20), default="text")
    whatsapp_message_id = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    status = db.Column(db.String(30), default="received")


# =========================
# WEBSITE ROUTES
# =========================

@app.route("/")
def empty_index():
    return render_template('index.html')


@app.route("/index")
def index():
    return render_template('index.html')


@app.route("/index.html")
def index2():
    return render_template('index.html')


@app.route("/categories2.html")
def try_categories():
    return render_template('categories2.html')


@app.route("/categories.html")
def categories():
    return render_template('categories.html')


@app.route("/categories")
def categories2():
    return render_template('categories.html')


@app.route("/categories-thermal-paper.html")
def thermal():
    return render_template('thermal_paper.html')


@app.route("/categories-thermal-paper")
def thermal2():
    return render_template('thermal_paper.html')


@app.route("/cart.html")
def cart():
    return render_template('cart.html')


@app.route("/cart")
def cart2():
    return render_template('cart.html')


@app.route("/privacy-policy")
def priva():
    return render_template('privacy-policy.html')


@app.route("/terms-and-conditions")
def terms():
    return render_template('terms.html')


# =========================
# WHATSAPP WEBHOOK VERIFY
# =========================

@app.route("/webhook", methods=["GET"])
def verify_webhook():

    VERIFY_TOKEN = os.getenv(
        "VERIFY_TOKEN",
        "linkenterprise123"
    )

    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200

    return "Forbidden", 403


# =========================
# RECEIVE WHATSAPP MESSAGES
# =========================

@app.route("/webhook", methods=["POST"])
def receive_message():

    data = request.get_json()

    try:
        value = data["entry"][0]["changes"][0]["value"]

        if "messages" in value:

            msg = value["messages"][0]

            sender = msg["from"]
            msg_type = msg["type"]

            text = ""

            if msg_type == "text":
                text = msg["text"]["body"]

            message = WhatsAppMessage(
                mobile_number=sender,
                message_text=text,
                direction="incoming",
                message_type=msg_type,
                whatsapp_message_id=msg.get("id"),
                status="received"
            )

            db.session.add(message)
            db.session.commit()

            print(f"{sender}: {text}")

    except Exception as e:
        print("Webhook Error:", e)

    return "EVENT_RECEIVED", 200


# =========================
# SIMPLE WHATSAPP INBOX
# =========================
from zoneinfo import ZoneInfo
@app.route("/inbox")
def inbox():

    messages = WhatsAppMessage.query.order_by(
        WhatsAppMessage.id.desc()
    ).limit(100).all()

    html = "<h1>Link Enterprise WhatsApp Inbox</h1>"

    for msg in messages:

        ist_time = ""

        if msg.timestamp:
            ist_time = msg.timestamp.astimezone(
                ZoneInfo("Asia/Kolkata")
            ).strftime("%d-%m-%Y %I:%M:%S %p")

        html += f"""
        <div style='margin-bottom:20px'>
            <b>{msg.mobile_number}</b><br>
            {msg.message_text or ''}<br>
            {msg.direction}<br>
            {ist_time}
        </div>
        <hr>
        """

    return html


# =========================
# START APP
# =========================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
