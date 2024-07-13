from flask import Flask, request
from celery import Celery
import smtplib
from email.mime.text import MIMEText
import logging
import emoji
from datetime import datetime
from dotenv import load_dotenv
import os

app = Flask(__name__)
load_dotenv()

app.config['CELERY_BROKER_URL'] = 'pyamqp://guest@localhost//'
app.config['CELERY_RESULT_BACKEND'] = 'rpc://'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

log_file = os.path.expanduser("~/messaging_system.log")
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@celery.task
def send_email(recipient):
    sender = os.getenv('EMAIL_SENDER')
    password = os.getenv('EMAIL_PASSWORD')

    logging.info(f"Attempting to send email from {sender} to {recipient}")
    logging.info(f"Sender: {sender}, Password: {'*' * len(password) if password else 'Not set'}")

    msg = MIMEText("This is a test email sent from a Messaging System.")
    msg['Subject'] = "Test Email"
    msg['From'] = sender
    msg['To'] = recipient

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            logging.info("Connected to SMTP server {emoji.emojize(':hourglass_flowing_sand:')} ...")
            smtp.login(sender, password)
            logging.info("Logged in Successfully {emoji.emojize(':white_check_mark:')}")
            smtp.send_message(msg)
            logging.info(f"Email sent to {recipient}")
        logging.info(f"Email sent {emoji.emojize(':envelope_with_arrow:')} to {recipient}")
        return f"Email sent to {recipient}"
    except Exception as e:
        error_message = f"Failed to send email to {recipient}. Error: {str(e)} {emoji.emojize(':cross_mark:')}"
        logging.error(error_message)
        return error_message

    # with smtplib.SMTP('localhost') as smtp:
        # smtp.sendmail(sender, [recipient], msg.as_string()) 

@app.route('/')
def handle_request():
    if 'sendmail' in request.args:
        recipient = request.args.get('sendmail')
        logging.info(f"Received request to send email to {recipient}")
        task = send_email.delay(recipient)
        logging.info(f"Email task queued with id {task.id}")
        return f"Email task queued for {recipient}"
    elif 'talktome' in request.args:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logging.info(f"Talktome request received at {current_time}")
        return f"Request logged at {current_time}"
    else:
        return "Invalid request"
    
if __name__ == '__main__':
    app.run(debug=True)