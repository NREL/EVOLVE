""" This module contains functions, class, methods to interact with RABBIT MQ and
push the report generation messages. """

import pika
import json
import os


def publish_message(message: str):

    # establish a connection with RabbitMQ server
    with pika.BlockingConnection(pika.ConnectionParameters(os.getenv('RABBITMQ_HOST'), os.getenv('RABBITMQ_PORT'),
        credentials=pika.PlainCredentials(os.getenv('RABBITMQ_USER'), os.getenv('RABBITMQ_PASSWORD'))
    )) as connection:

        channel = connection.channel()
        
        channel.exchange_declare(
            exchange='evolve',
            exchange_type='direct'
        )

        # create the queue to which the message will be delivered
        channel.queue_declare(queue='evolve_notify')

        # publish a message
        print(f'message published >> {message}' )
        channel.basic_publish(exchange='evolve', 
            routing_key='evolve.notify', 
            body=message
        )



if __name__ == '__main__':
    publish_message("hello")

 