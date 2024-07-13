## Messaging System with RabbitMQ/Celery and Python Application behind Nginx
## Overview
This project demonstrates how to create a messaging system using RabbitMQ for task queuing and Celery for background task processing, integrated with a Python Flask application. The application can send emails and log the current time based on HTTP request parameters. Nginx is configured as a reverse proxy server to serve the application, and ngrok can be used to expose the local application endpoint to the public.

## Features
RabbitMQ & Celery Integration: Efficient task queuing and worker management.

Flask Web Application: Handle incoming HTTP requests to trigger background tasks.

Email Sending: Asynchronous email sending using Celery tasks.

Logging: Record log messages to a file.

Nginx Reverse Proxy: Serve the application through Nginx.

Ngrok: Expose the local application endpoint to the public.

## Prerequisites
Python 3.10+
RabbitMQ
Celery
Redis
Nginx
ngrok
## Setting Up RabbitMQ and Celery
Install RabbitMQ

``` sudo apt-get install rabbitmq-server ```

Start RabbitMQ Server

``` sudo systemctl start rabbitmq-server ```

## Create a RabbitMQ User and Set Permissions

``` sudo rabbitmqctl add_user myuser mypassword ```

```sudo rabbitmqctl set_permissions -p / myuser ".*" ".*" ".*"```

```sudo rabbitmqctl set_user_tags myuser administrator```

## Configure Celery in Your Flask Application
### Update app.py:

```from flask import Flask, request
from celery import Celery
import smtplib
from email.mime.text import MIMEText
import logging
from datetime import datetime
import os
app = Flask(__name__)
celery = Celery(app.name, broker='pyamqp://guest:guest@localhost//')
log_dir = '/var/log'
os.makedirs(log_dir, exist_ok=True)
log_path = os.path.join(log_dir, 'messaging_system.log')
logging.basicConfig(filename=log_path, level=logging.INFO)
SENDER_EMAIL = 'fortismanuel@gmail.com'
SENDER_PASSWORD = 'evoddpabuclykxye'
@celery.task
def send_email(recipient):
    sender = SENDER_EMAIL
    password = SENDER_PASSWORD
    subject = "Test Email"
    body = "This is a test email sent from the messaging system by HNGDevOps."
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
        smtp_server.login(sender, password)
        smtp_server.sendmail(sender, recipient, msg.as_string())
        logging.info(f"Email sent to {recipient} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
@celery.task
def log_current_time():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logging.info(f"Talktome request received at {current_time}")
@app.route('/')
def handle_request():
    if 'sendmail' in request.args:
        recipient = request.args.get('sendmail')
        send_email.delay(recipient)
        return f"Email queued for sending to {recipient}" 
    elif 'talktome' in request.args:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_current_time.delay()
        return f"Current time logged: {current_time}"  
    else:
        return "Invalid request. Use ?sendmail or ?talktome parameter."
if __name__ == '__main__':
    app.run(debug=True)
```

## Run Celery Worker

``` celery -A app worker --loglevel=info```

# Setting Up Nginx 
## Install Nginx

``` sudo apt-get install nginx```

## Configure Nginx
~ Edit the Nginx configuration file, typically located at /etc/nginx/sites-available/default:~


``` server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```
## Restart Nginx
```sudo systemctl restart nginx ```

## Exposing Local Application with ngrok
## Download and Install ngrok

``` wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip```

```unzip ngrok-stable-linux-amd64.zip```

```sudo mv ngrok /usr/local/bin```

## Expose Your Application

```ngrok http 5000```
ngrok will provide a public URL to access your local application.


## Message Brokers
Message brokers act as intermediaries between different services, ensuring reliable communication. They store incoming requests in a queue and serve them sequentially to receiving services. By decoupling services in this manner, you enhance scalability and performance. RabbitMQ is a message broker that implements the Advanced Message Queuing Protocol (AMQP). It facilitates communication between different components of a distributed system by sending messages between them.


## Celery
Celery is a distributed task queue framework that allows you to run asynchronous tasks in the background. It is often used for long-running or scheduled background tasks in web applications.


## Conclusion
By following this guide, you will have a fully functional messaging system with RabbitMQ, Celery, Flask, Nginx, and ngrok. This setup ensures efficient task queuing, robust worker management, and public accessibility for your local development environment.
