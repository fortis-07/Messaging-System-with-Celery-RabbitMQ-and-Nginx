# Import necessary modules from Flask and other packages
from flask import Flask, request  # Flask for creating the web application, request to handle incoming requests
from tasks import send_mail, log_message  # Custom tasks for sending emails and logging messages
import logging  # Python's logging module for logging messages

# Initialize the Flask application
app = Flask(__name__)

# Set up logging configuration
# Log messages will be saved to /var/log/messaging_system.log with INFO level and above
logging.basicConfig(filename='/var/log/messaging_system.log', level=logging.INFO)

# Define a route for the root URL ('/')
@app.route('/')
def index():
    # Get 'sendmail' and 'talktome' parameters from the request URL
    sendmail = request.args.get('sendmail')
    talktome = request.args.get('talktome')
    
    # If 'sendmail' parameter is present in the request
    if sendmail:
        # Queue the task of sending an email using Celery (asynchronously)
        send_mail.delay(sendmail)
        # Return a message indicating that the email has been queued
        return f"Email to {sendmail} queued."
    
    # If 'talktome' parameter is present in the request
    if talktome:
        # Queue the task of logging a message using Celery (asynchronously)
        log_message.delay()
        # Return a message indicating that the message has been logged
        return "Message logged."

    # If neither parameter is present, return a default message
    return "Hello, use ?sendmail=<email> or ?talktome"

# Run the Flask application
# The app will run in debug mode, which is useful for development as it provides detailed error messages
if __name__ == '__main__':
    app.run(debug=True)
