""" This module fetches rabbit MQ message and calls appropriate function."""

# Standard imports
import os
import json
import pydantic
import time
import logging

# Third party imports
from dotenv import load_dotenv
import pika

# internal imports
from input_config_model import InputConfigModel
from scenario_processor import process_scenario

load_dotenv()
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)


MAX_RETRIES = 5
RETRY_DELAY = 10
retry = 0

while retry <= MAX_RETRIES:
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            os.getenv('RABBITMQ_HOST'), os.getenv('RABBITMQ_PORT'),
            credentials=pika.PlainCredentials(os.getenv('RABBITMQ_USER'), 
            os.getenv('RABBITMQ_PASSWORD'))
        ))
        logger.debug('Connected Successfully')
        break
    except Exception as e:
        logger.debug(f"Retry {retry} >> {str(e)}")
        retry +=1 
        time.sleep(RETRY_DELAY)


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
        logger.debug(f'Submitted message : {message}')
        input_config_pydantic= pydantic.parse_obj_as(InputConfigModel, message)
        process_scenario(input_config_pydantic)
        logger.debug(f'Completed processing...')
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        logger.debug(f"Errro Awk: {e}")

channel.basic_consume(queue='evolve_notify',
    on_message_callback=callback)

channel.start_consuming()
