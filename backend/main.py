from flask import Flask
from application.config import LocalDevelopmentConfig
from application.database import db
from flask_cors import CORS
from flask_uploads import UploadSet, IMAGES, configure_uploads
from datetime import datetime, timedelta
from application.models import *
import redis
import threading
import schedule
import time
from email.message import EmailMessage
import smtplib
import ssl
from dotenv import load_dotenv
import os


# from flask_bcrypt import Bcrypt
# import os


app = None
UPLOAD_FOLDER="static/images"
def create_app():
    app=Flask(__name__)
    print("starting local development")
    app.config['UPLOADED_PHOTOS_DEST'] = 'static/images'
    app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    app.app_context().push()
    return app

# def create_database_if_not_exists():
#         print("hello")
#         db.create_all()
#         b = Bcrypt()
#         pass_hash = b.generate_password_hash("admin")
#         admin = Users(email="admin@email.com", username="admin", password=pass_hash, admin=True)
#         db.session.add(admin)
#         db.session.commit()

app=create_app()
CORS(app)
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
# CORS(app, resources={r"/*": {"origins": "http://localhost:8080"}})
redis_cli = redis.Redis(host="localhost", port=6379, password="", decode_responses=True)
# create_database_if_not_exists()

load_dotenv()
email_address = os.getenv("EMAIL_ADDRESS")
email_password = os.getenv("EMAIL_PASSWORD")


previous_day_5pm = datetime.now().replace(hour=17, minute=0, second=0,
                                          microsecond=0) - timedelta(days=1)
today_5pm = datetime.now().replace(hour=18, minute=0, second=0, microsecond=0)

def send_email(email, subject, message):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = email_address
    msg['To'] = str(email)
    msg.set_content(message)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(email_address, email_password)
        server.send_message(msg)


def dailyReport():
    with app.app_context():
        users = Users.query.all()
        for user in users:
            username = user.username
            email = user.email
            tickets=Tickets.query.filter_by(user_id=user.id).all()
            total_tickets = 0
            if datetime.now().day == 1:
                monthlyReport()
                continue
            for ticket in tickets:
                ticket_created_on = ticket.created_at
                if previous_day_5pm <= ticket_created_on <= today_5pm:
                    total_tickets += ticket.quantity

            body = f"Hi {username},\n\nYou have booked {total_tickets} tickets today .\n\nRegards,\nTeam BookMyEvent"
            print(body)
            # send_mail(email, "Daily Report", body)
            send_email(email, "Daily Report", body)
            print("Mail Sent")

def monthlyReport():
    with app.app_context():
        users = Users.query.all()
        now = datetime.now()
        for user in users:
            username = user.username
            email = user.email
            tickets=Tickets.query.filter_by(user_id=user.id).all()
            total_tickets = 0
            for ticket in tickets:
                ticket_created_on = ticket.created_at
                if ticket_created_on.month == now.month:
                    total_tickets += ticket.quantity

            body = f"Hi {username},\n\nYou have booked {total_tickets} tickets this month .\n\nRegards,\nTeam BookMyEvent"
            send_email(email, "Monthly Report", body)
            print("Mail Sent")

def Scheduled():

    schedule.every().day.at("23:15").do(dailyReport)

    while True:
        schedule.run_pending()
        time.sleep(1)



from application.controllers import *

if __name__ == '__main__':
    t1 = threading.Thread(target=Scheduled)
    t1.start()
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)
    t1.join()
