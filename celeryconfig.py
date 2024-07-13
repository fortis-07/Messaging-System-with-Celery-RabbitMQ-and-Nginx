# The broker URL for Celery is responsible for sending and receiving messages between Celery workers and the client
# Here, the broker URL is configured to use RabbitMQ (with default guest user) running on localhost
broker_url = 'pyamqp://guest@localhost//'

# The result backend is used to store the results of Celery tasks
# Here, the result backend is configured to use RPC (Remote Procedure Call)
result_backend = 'rpc://'
