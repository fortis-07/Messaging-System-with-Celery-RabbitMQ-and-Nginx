# Import necessary modules
from celery import Celery  # Celery for creating and managing tasks
import smtplib  # smtplib for sending emails
import logging  # logging for logging messages
from datetime import datetime  # datetime for getting the current date and time

# Initialize a Celery application
# 'tasks' is the name of the Celery application
# The broker parameter specifies the message broker to use (RabbitMQ in this case)
app = Celery('tasks', broker='pyamqp://guest@localhost//')

# Define a Celery task for sending emails
@app.task
def send_mail(email):
    # Use Python's smtplib to send an email
    # Connect to the local SMTP server
    with smtplib.SMTP('localhost') as server:
        # Send an email from 'youremail@example.com' to the specified recipient
        # The email has a subject 'Test' and a body 'This is a test email.'
        server.sendmail('youremail@example.com', email, 'Subject: Test\n\nThis is a test email.')
        # Print a confirmation message to the console
        print(f"Email sent to {email}")

# Define a Celery task for logging the current time
@app.task
def log_message():
    # Log the current date and time using Python's logging module
    logging.info(f"Current time: {datetime.now()}")
    # Print a confirmation message to the console
    print("Message logged")
