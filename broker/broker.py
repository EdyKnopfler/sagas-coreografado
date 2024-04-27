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
channel.exchange_declare(exchange='errors', exchange_type='direct')
channel.queue_declare(queue='errors')
channel.queue_bind(
    exchange='errors', queue='errors', routing_key='errors')

queue_arguments = {
    'x-dead-letter-exchange': 'errors',
    'x-dead-letter-routing-key': 'errors'
}


def sagas_service_setup(queue_this, queue_prev=None, queue_next=None):
    channel.exchange_declare(exchange='sagas', exchange_type='direct')

    if queue_prev:
        _new_queue(queue_prev)

    _new_queue(queue_this)
    
    if queue_next:
        _new_queue(queue_next)

    channel.basic_qos(prefetch_count=1)


def publish(queue_name, message):
    print('Publising to', queue_name, message)
    channel.basic_publish(
        exchange='sagas', 
        routing_key=queue_name, 
        body=json.dumps(message)
    )


def start_consuming(queue_this, callback, queue_prev=None, queue_next=None):

    def _on_request(ch, method, properties, body):

        def _handle_success(action, result_message):
            print('Handling success')
            ch.basic_ack(delivery_tag=method.delivery_tag)
            queue = queue_next if action == 'proceed' else queue_prev

            if queue:
                publish(queue, {
                    'action': action,
                    'data': result_message,
                })


        def _handle_error(failed_message):
            print('Handling error', e)
            ch.basic_reject(delivery_tag=method.delivery_tag, requeue=False)

            if queue_prev:
                publish(queue_prev, {
                    'action': 'undo',
                    'data': failed_message,
                })

        try:
            print('Received on', queue_this)
            message = json.loads(body)
            action = message.get('action', 'proceed')
            data = message.get('data', {})
            result = callback(action, data)
            _handle_success(action, result)
        except Exception as e:
            _handle_error(data)
            
    
    channel.basic_consume(
        queue=queue_this, 
        on_message_callback=_on_request, 
        auto_ack=False
    )

    channel.start_consuming()


def _new_queue(queue_name):
    channel.queue_declare(queue=queue_name, arguments=queue_arguments)

    channel.queue_bind(
        exchange='sagas', 
        queue=queue_name,
        routing_key=queue_name
    )


