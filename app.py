# Import necessary modules from Flask, Celery, and other packages
from flask import Flask, request  # Flask for creating the web application, request to handle incoming requests
from celery import Celery  # Celery for background task processing
import smtplib  # SMTP library for sending emails
from email.mime.text import MIMEText  # Library for creating email messages
import logging  # Logging library for recording log messages
from datetime import datetime  # DateTime library for handling dates and times
import os  # OS library for handling file and directory operations

# Create the Flask app
app = Flask(__name__)

# Create the Celery app with RabbitMQ as the broker
# The broker URL is specified; update this if needed
celery = Celery(app.name, broker='pyamqp://guest:guest@localhost//')

# Ensure the log directory exists and configure logging
log_dir = '/var/log'
os.makedirs(log_dir, exist_ok=True)  # Create the log directory if it doesn't exist
log_path = os.path.join(log_dir, 'messaging_system.log')  # Define the path to the log file
logging.basicConfig(filename=log_path, level=logging.INFO)  # Configure logging to write to the log file

# Set sensitive information directly
SENDER_EMAIL = 'fortismanuel@gmail.com'  # Sender's email address
SENDER_PASSWORD = 'evoddpabuclykxye'  # Sender's email password (use environment variables for security in production)

# Define a Celery task to send an email
@celery.task
def send_email(recipient):
    sender = SENDER_EMAIL
    password = SENDER_PASSWORD
    subject = "Test Email"
    body = "This is a test email sent from the messaging system by HNGDevOps."
    
    # Create the email message
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient
    
    # Send the email using SMTP with SSL
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
        smtp_server.login(sender, password)  # Login to the SMTP server
        smtp_server.sendmail(sender, recipient, msg.as_string())  # Send the email
        # Log the email sending event with a timestamp
        logging.info(f"Email sent to {recipient} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Define a Celery task to log the current time
@celery.task
def log_current_time():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Get the current time
    logging.info(f"Talktome request received at {current_time}")  # Log the time of the "talktome" request

# Define the main route for the Flask app
@app.route('/')
def handle_request():
    # Check if 'sendmail' parameter is in the request URL
    if 'sendmail' in request.args:
        recipient = request.args.get('sendmail')  # Get the recipient email from the request
        send_email.delay(recipient)  # Queue the send_email task using Celery
        return f"Email queued for sending to {recipient}"  # Return a response to the client
    
    # Check if 'talktome' parameter is in the request URL
    elif 'talktome' in request.args:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Get the current time
        log_current_time.delay()  # Queue the log_current_time task using Celery
        return f"Current time logged: {current_time}"  # Return a response to the client
    
    # If neither parameter is present, return an invalid request response
    else:
        return "Invalid request. Use ?sendmail or ?talktome parameter."

# Run the Flask app in debug mode
if __name__ == '__main__':
    app.run(debug=True)
