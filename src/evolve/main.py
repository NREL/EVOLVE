""" This module contains functions, class, methods to interact with RABBIT MQ and
push the report generation messages. """

import pika
import json

# establish a connection with RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost',
credentials=pika.PlainCredentials('user', 'pass')
))
channel = connection.channel()

channel.exchange_declare(
    exchange='evolve',
    exchange_type='direct'
)
channel.queue_declare(queue='evolve_notify')

channel.queue_bind(
    exchange='evolve',
    queue='evolve_notify',
    routing_key='evolve.notify'
)

def callback(ch, method, properties, body):
    payload = body 
    print(f' Notifying >> {payload}')
    # ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(on_message_callback=callback, 
queue='evolve_notify'
)

# close the connection
channel.start_consuming()