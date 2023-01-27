""" This module fetches rabbit MQ message and calls appropriate function."""

# Standard imports
import os
import json
import pydantic

# Third party imports
from dotenv import load_dotenv
import pika

# internal imports
from input_config_model import InputConfigModel
from scenario_processor import process_scenario

load_dotenv()


with pika.BlockingConnection(pika.ConnectionParameters(
        os.getenv('RABBITMQ_HOST'),
        os.getenv('RABBITMQ_PORT'),
        credentials=pika.PlainCredentials(os.getenv('RABBITMQ_USER'), 
        os.getenv('RABBITMQ_PASSWORD'))
    )) as connection:

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

    # Create the callback function
    def callback(ch, method, properties, body):
        # Decode the message
        
        try:
            message = json.loads(body.decode('utf-8'))
            # Do something with the message
            print(f'Submitted message : {message}')
            input_config_pydantic= pydantic.parse_obj_as(InputConfigModel, message)
            process_scenario(input_config_pydantic)
            print(f'Completed processing...')
            # ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            print(f"Errro Awk: {e}")

    channel.basic_consume(queue='evolve_notify',
        on_message_callback=callback, auto_ack=True)

    channel.start_consuming()
