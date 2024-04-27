import pika
import os
import json


credentials = pika.PlainCredentials(
    os.getenv('RABBITMQ_USER', 'usuario'),
    os.getenv('RABBITMQ_PASSWORD', 'senha')
)

connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        os.getenv('RABBITMQ_HOST', 'localhost'),
        int(os.getenv('RABBITMQ_PORT', '5672')), 
        os.getenv('RABBITMQ_VHOST', '/'),
        credentials
    )
)

channel = connection.channel()


def sagas_service_setup(queue_this, queue_prev=None, queue_next=None):
    channel.exchange_declare(exchange='sagas', exchange_type='direct')

    if queue_prev:
        _new_queue(queue_prev)

    _new_queue(queue_this)
    
    if queue_next:
        _new_queue(queue_next)

    channel.basic_qos(prefetch_count=1)


def publish(queue_name, message):
    channel.basic_publish(
        exchange='sagas', 
        routing_key=queue_name, 
        body=json.dumps(message)
    )


def start_consuming(queue_name, callback):
    channel.basic_consume(
        queue=queue_name, 
        on_message_callback=callback, 
        auto_ack=False
    )

    channel.start_consuming()


def _new_queue(queue_name):
    channel.queue_declare(queue=queue_name)

    channel.queue_bind(
        exchange='sagas', 
        queue=queue_name,
        routing_key=queue_name
    )