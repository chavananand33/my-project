from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from config import DevelopmentConfig
from flask import jsonify
import datetime
from dotenv import load_dotenv

import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")

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

app.config.from_object("config.Config")

db = SQLAlchemy(app)

# ===========================
# DATABASE MODELS
# ===========================

# from werkzeug.security import generate_password_hash, check_password_hash

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

# The "Brain" of your chatbot populated with your resume data
RESUME_DATA = {
    "basics": {
        "name": "Anand Chavan", # [cite: 1]
        "location": "Pune, Maharashtra, India", # [cite: 2]
        "summary": "Experienced in building AI-driven automation using Python, LLM APIs, and LangChain." # [cite: 4]
    },
    "experience": [
        {
            "company": "IBM India Pvt. Ltd.", # [cite: 24]
            "role": "Support Engineer", # [cite: 24]
            "impact": "Reduced incident resolution time by 25% through structured RCA." # 
        },
        {
            "company": "JIO Platforms Limited", # [cite: 29]
            "role": "Deputy Manager", # [cite: 29]
            "impact": "Maintained 99.9% system uptime for telecom activation workflows." # 
        }
    ],
    "skills": {
        "ai_tools": ["ChatGPT", "Google Gemini", "Perplexity", "Claude"], # [cite: 9]
        "infrastructure": ["Unix/Linux Server Operations", "Shell Scripting"], # [cite: 10, 11]
        "databases": ["Oracle (11g/19c) " "&" "PostgreSQL"] # [cite: 12, 19, 28]
    },
    "contacts": {
        "MSISDN": ["+91 9730343050"], # [cite: 9]
        "EMAIL": ["chavananand33@gmail.com"]
    },    
    "education": "Computer Engineering degree from Pune University with Distinction and is committed to continuous learning, specifically in Python development and AI engineering." # [cite: 39]
}


def get_portfolio_response(message):

    user_msg = message.lower().strip()
    
    # 1. Greeting Logic (Indented inside the function)
    if any(word in user_msg for word in ["hi", "hello", "hey", "greetings", "personal"]):
        # Access strings directly as we discussed to avoid letter-splitting
        my_name = RESUME_DATA['basics']['name'] # [cite: 1]
        my_location = RESUME_DATA['basics']['location'] # [cite: 2]
        my_summary = RESUME_DATA['basics']['summary'] # [cite: 4]
        return f"Hi, I'm {my_name}. I'm based in {my_location}. {my_summary}"
    
    # 3. Handle Experience/History
    if any(word in user_msg for word in ["work", "history","experience", "career", "background", "years", "telecom", "job", "company", "role", "ibm", "jio"]):
        ibm = RESUME_DATA['experience'][0]
        jio = RESUME_DATA['experience'][1]
        return (f"Anand has a strong background in Python,AI Automation Engineering, Python, Generative AI, Telecom IT and Enterprise System. "
                f"At {ibm['company']}, he {ibm['impact']} "
                f"Additionally, at {jio['company']}, he {jio['impact']}"
                "He's currently specializing in Python & AI Engineering. Check the 'Experience' section for more details!")

    # 4. Handle Education
    if any(word in user_msg for word in ["education", "degree", "college", "university", "study", "graduate", "bachelor", "learning", "upskill"]):
        return f"According to his resume, Anand holds a {RESUME_DATA['education']}"

    # 5. Handle Skills & Tools
    if any(word in user_msg for word in ["skill", "tool", "ai", "know", "tech","stack", "coding", "python", "flask", "tools", "languages", "frameworks", "expert"]):
        tools = ", ".join(RESUME_DATA['skills']['ai_tools'])
        infra = ", ".join(RESUME_DATA['skills']['infrastructure'])
        database = ", ".join(RESUME_DATA['skills']['databases'])
        return f"Anand is skilled in AI tools like {tools}, infra management like {infra} and database like {database}."

    # 6. Handle Specific Projects
    if any(word in user_msg for word in ["project", "build", "portfolio","apps", "automation", "github", "developed", "made", "link"]):
        return """
               He recently built an AI Portfolio Chatbot with Visitor Analytics using Python, LLM APIs, LangChain, PostgreSQL technologies.<br><br>
               <a href="https://my-project-gu7s.onrender.com/" target="_blank">
               <button style="background-color:#007BFF; color:white; padding:8px 18px; border:none; border-radius:6px; font-size:12px; cursor:pointer;">
               View Project
               </button>
               </a>
               """
  # 7. Contacts
    if any(word in user_msg for word in ["contact","email", "linkedin", "reach", "message", "talk", "connect", "hire", "phone"]):
        # Access strings directly to keep them readable
        my_msisdn = RESUME_DATA['contacts']['MSISDN'] # "+91-9730343050"
        my_email = RESUME_DATA['contacts']['EMAIL']   # "chavananand33@gmail.com"
        
        return (f"The best way to reach me is via LinkedIn or the contact form on this website.\n"
                f"I'm always open to discussing new opportunities!\n"
                f"Below are my coordinates:\n"
                f"MSISDN: {my_msisdn}\n"
                f"Email: {my_email}")

  # 8. Resume
    if any(word in user_msg for word in ["cv", "download", "pdf", "file", "document", "resume"]):
        return """
               You can download the full CV by clicking the 'Download Resume' button on website or Click on below Download Resume button :<br><br>
               <a href="{{ url_for('static', filename='resume.pdf') }} 
               <button style="background-color:#007BFF; color:white; padding:8px 18px; border:none; border-radius:6px; font-size:12px; cursor:pointer;">
               Download Resume
               </button>
               </a>
               """

  # 2. Fallback Logic (Also indented inside the function)
    return "I can tell you about Anand's work at IBM/Jio, his education, or his AI projects. What would you like to know?"
    

@app.route("/chat", methods=["POST"])
def chat():
    # 1. Get data from the request correctly
    data = request.json
    user_query = data.get('message', '')
    
    # 2. Get the bot's response using your resume-reading logic [cite: 17, 18]
    # We use your resume data like your 7.6+ years of experience [cite: 4]
    bot_reply = get_portfolio_response(user_query)

    # 3. Save to database BEFORE the return statement
    try:
        chat_record = ChatMessage(
            user_message=user_query,
            bot_reply=bot_reply
        )
        db.session.add(chat_record)
        db.session.commit()
    except Exception as e:
        print(f"Database Error: {e}")
        # We roll back if there's an error to keep the session clean
        db.session.rollback()

    # 4. Final Return - Use ONE key that matches your JS (e.g., "response")
    return jsonify({"response": bot_reply})

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

