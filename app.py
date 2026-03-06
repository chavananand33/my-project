from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from config import DevelopmentConfig
from flask import jsonify
import datetime
from dotenv import load_dotenv

import os
import os

class Config:
    SECRET_KEY = os.getenv("555de27cd2aa0f1c5c3f8322c89172667d7cadef487391f986ef90da7287599c", "dev-secret")

    db_url = os.getenv("postgresql://anand:e8RXIdlv28Mmyww3pqr6G7ssRBOLeQoY@dpg-d6l8tphaae7s7382f4o0-a/portfolio_ai_uo50")

    if db_url and db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)

    SQLALCHEMY_DATABASE_URI = db_url or "sqlite:///local.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True

PORT = int(os.environ.get("PORT", 5000))

load_dotenv()

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

print("SECRET KEY:", app.config.get("SECRET_KEY"))


db = SQLAlchemy(app)

# ===========================
# DATABASE MODELS
# ===========================

from werkzeug.security import generate_password_hash, check_password_hash

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(120))
    subject = db.Column(db.String(200))
    message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

class Counter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    visits = db.Column(db.Integer, default=0)

class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_message = db.Column(db.Text)
    bot_reply = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)


with app.app_context():
    db.create_all()

# ===========================
# ROUTES
# ===========================



@app.route("/contact", methods=["POST"])
def contact():
    new_message = Message(
        name=request.form.get("name"),
        email=request.form.get("email"),
        subject=request.form.get("subject"),
        message=request.form.get("message")
    )

    db.session.add(new_message)
    db.session.commit()

    flash("Message sent successfully!")
    return redirect(url_for("home"))

# ===========================
# MAIN
# ===========================

from flask import session

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        admin = Admin.query.filter_by(username=username).first()

        if admin and check_password_hash(admin.password, password):
            session["admin"] = admin.id
            return redirect(url_for("admin_dashboard"))
        else:
            flash("Invalid username or password")

    return render_template("admin_login.html")

from datetime import datetime, date

@app.route("/admin/dashboard")
def admin_dashboard():

    if "admin" not in session:
        return redirect(url_for("admin_login"))

    messages = Message.query.order_by(Message.created_at.desc()).all()

    total_messages = Message.query.count()

    today = date.today()
    today_messages = Message.query.filter(
        db.func.date(Message.created_at) == today
    ).count()

    chat_messages = ChatMessage.query.order_by(
        ChatMessage.created_at.desc()
    ).all()

    return render_template(
        "admin_dashboard.html",
        messages=messages,
        chat_messages=chat_messages,
        total_messages=total_messages,
        today_messages=today_messages
    )

@app.route("/admin/delete/<int:id>")
def delete_message(id):

    # Check if admin is logged in
    if "admin" not in session:
        return redirect(url_for("admin_login"))

    message = Message.query.get(id)

    if message:
        db.session.delete(message)
        db.session.commit()

    return redirect(url_for("admin_dashboard"))

@app.route("/admin/logout")
def admin_logout():
    session.pop("admin", None)
    flash("Logged out successfully.")
    return redirect(url_for("admin_login"))

def get_portfolio_response(message):

    if "experience" in message:
        return "Anand has 7.6+ years of experience in Telecom IT, Enterprise Applications, and AI-driven automation and currently upskilling in Python and ML Engineering. For detailed work history go to Experience Form on this website."

    elif "skills" in message:
        return "Key skills include Python, Flask, SAP CRM, Telecom IT Systems, AI Automation, and Machine Learning fundamentals."

    elif "projects" in message:
        return "Projects include AI-powered portfolio chatbot, automation tools, telecom application support systems, and ML learning initiatives."

    elif "education" in message:
        return "Anand holds a Bachelor's degree and is continuously upskilling in AI, Machine Learning, and Python development."

    elif "contact" in message:
        return "You can contact Anand via LinkedIn on https://linkedin.com/in/anand-chavan-7615b9118 or through the contact form on this website and Feel free to reach out."

    elif "resume" in message:
        return "You can download the resume using the Download Resume button in the hero section."

    else:
        return "Sorry!! I can only help you with information about Experience, Skills, Projects, Education, Contact or Resume. Please ask something related to these."

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "").lower()

    reply = get_portfolio_response(user_message)

    # Save to database
    chat_record = ChatMessage(
        user_message=user_message,
        bot_reply=reply
    )

    db.session.add(chat_record)
    db.session.commit()

    return jsonify({"reply": reply})


from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object("config.Config")

db = SQLAlchemy(app)

class Counter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    visits = db.Column(db.Integer, default=0)

with app.app_context():
    db.create_all()

@app.route("/")
def home():

    counter = db.session.get(Counter, 1)

    if not counter:
        counter = Counter(id=1, visits=0)
        db.session.add(counter)
        db.session.commit()

    counter.visits += 1
    db.session.commit()

    return render_template("index.html", visits=counter.visits,
        years_exp="7.6+",
        companies="3+",
        sla="99.99%"
    )
if __name__ == "__main__":
    app.run(debug=True)

