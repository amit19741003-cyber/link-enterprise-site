from flask import Flask, render_template, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import requests
import os

app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY", "change-this-secret-key")
app.permanent_session_lifetime = timedelta(minutes=16)

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        if username == "link73876@yahoo.com" and password == "Benap@73876":
            session.permanent = True
            session["logged_in"] = True
            return redirect("/inbox")

        return "Invalid Credentials"

    return """
    <form method="POST">
        <input name="username" placeholder="Username"><br><br>
        <input name="password" type="password" placeholder="Password"><br><br>
        <button type="submit">Login</button>
    </form>
    """

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
    if not session.get("logged_in"):
        return redirect("/login")

    messages = WhatsAppMessage.query.order_by(
        WhatsAppMessage.id.desc()
    ).limit(200).all()

    # Convert timestamps to IST
    ist = ZoneInfo("Asia/Kolkata")
    for msg in messages:
        if msg.timestamp:
            msg.timestamp = msg.timestamp.astimezone(ist)

    return render_template("inbox.html", messages=messages)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


# =========================
# START APP
# =========================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
