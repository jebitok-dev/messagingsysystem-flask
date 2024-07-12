from flask import Flask, request
from celery import Celery
import smtplib
from email.mime.text import MIMEText
import logging
from datetime import datetime
import os

app = Flask(__name__)

app.config['CELERY_BROKER_URL'] = 'pyamqp://guest@localhost//'
app.config['CELERY_RESULT_BACKEND'] = 'rpc://'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

log_file = os.path.expanduser("~/messaging_system.log")
logging.basicConfig(filename=log_file, level=logging.INFO)

@celery.task
def send_email(recipient):
    sender = "your_email@example.com"
    msg = MIMEText("This is a test email sent from a Messaging System.")
    msg['Subject'] = "Test Email"
    msg['From'] = sender
    msg['To'] = recipient

    with smtplib.SMTP('localhost') as smtp:
        smtp.sendmail(sender, [recipient], msg.as_string())

@app.route('/')
def handle_request():
    if 'sendmail' in request.args:
        recipient = request.args.get('sendmail')
        send_email.delay(recipient)
        return f"Email task queued for {recipient}"
    elif 'talktome' in request.args:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logging.info(f"Talktome request received at {current_time}")
        return f"Request logged at {current_time}"
    else:
        return "Invalid request"
    
if __name__ == '__main__':
    app.run(debug=True)