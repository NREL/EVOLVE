""" This module contains functions, class, methods to interact with RABBIT MQ and
push the report generation messages. """

import pika
import os


def publish_message(message: str):
    """ Function to publish a message. """
    with pika.BlockingConnection(
        pika.ConnectionParameters(
            os.getenv("RABBITMQ_HOST"),
            os.getenv("RABBITMQ_PORT"),
            credentials=pika.PlainCredentials(
                os.getenv("RABBITMQ_USER"), os.getenv("RABBITMQ_PASSWORD")
            ),
        )
    ) as connection:

        channel = connection.channel()

        channel.exchange_declare(exchange="evolve", exchange_type="direct")

        channel.queue_declare(queue="evolve_notify")

        print(f"message published >> {message}")
        channel.basic_publish(
            exchange="evolve", routing_key="evolve.notify", body=message
        )

