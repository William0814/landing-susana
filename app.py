from asyncio import sleep
from flask import Flask, redirect, render_template, request, flash, url_for
from percistence.form import Form, db
from datetime import datetime
from classes.tolgee import TolgeeManager
from threading import Thread
import requests, os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
current_year = datetime.now().year

# --- Config base ---
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

db.init_app(app)
tolgee = TolgeeManager(api_key=os.getenv('TOLGEE_API_KEY'), default_lang='en-US', api_url=os.getenv('TOLGEE_API_URL'))

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
FROM_EMAIL       = os.getenv("MAIL_USERNAME")     
TO_EMAIL         = os.getenv("MAIL_USERNAME")  

def send_email_async(subject: str, body: str, to_email: str):
    try:
        r = requests.post(
            "https://api.sendgrid.com/v3/mail/send",
            headers={
                "Authorization": f"Bearer {SENDGRID_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "personalizations": [{"to": [{"email": to_email}]}],
                "from": {"email": FROM_EMAIL},
                "subject": subject,
                "content": [{"type": "text/plain", "value": body}],
            },
            timeout=10,
        )
        if r.status_code not in (200, 202):
            app.logger.error("SendGrid error %s: %s", r.status_code, r.text)
    except Exception:
        app.logger.exception("Failed to send email (SendGrid)")

@app.context_processor
def inject_url_for_lang():
    from flask import url_for
    def url_for_lang(endpoint, **values):
        lang = request.args.get('lang', 'de-DE')
        if lang: values['lang'] = lang
        return url_for(endpoint, **values)
    return dict(url_for_lang=url_for_lang)

@app.route("/", methods=['GET', 'POST'])
def home():
    lang = request.args.get('lang', 'de-DE')
    context = tolgee.get_translation(lang)

    if request.method == 'POST':
        name    = request.form['name'].strip()
        email   = request.form['email'].strip()
        message = request.form['message'].strip()
        phone = request.form.get('phone').strip()
        date    = datetime.now()
        acceptPolitic = request.form.get('demo-copy') == 'on'

        db.session.add(Form(name=name, email=email, message=message, date=date, phone=phone, acceptPolitic=acceptPolitic))
        db.session.commit()

        body = f"Name: {name}\nEmail: {email}\nMessage: {message}\nPhone: {phone}\nAccept Privacy Policy: {acceptPolitic}"
        Thread(target=send_email_async,
               args=("New Message from your CV!!", body, TO_EMAIL),
               daemon=True).start()
        flash(f"Hi , your message has been sent successfully!", "success")
       
        return redirect(url_for('home', lang=lang))
    sleep(4)
    return render_template('index.html', current_year=current_year, **context)

@app.route('/firma')
def firma():
    lang = request.args.get('lang', 'de-DE')
    return render_template('firma.html', current_year=current_year, **tolgee.get_translation(lang))

@app.route('/services')
def services():
    lang = request.args.get('lang', 'de-DE')
    return render_template('services.html', current_year=current_year, **tolgee.get_translation(lang))

@app.route("/about-me")
def about_me():
    lang = request.args.get('lang', 'de-DE')
    return render_template('aboutMe.html', current_year=current_year,  **tolgee.get_translation(lang))

@app.route("/impresum")
def impresum():
    lang = request.args.get('lang', 'de-DE')
    return render_template('impresum.html', current_year=current_year, **tolgee.get_translation(lang))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)