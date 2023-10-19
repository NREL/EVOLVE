""" This module fetches rabbit MQ message and calls appropriate function."""

# Standard imports
import os
import json
import time
import logging

# Third party imports
from dotenv import load_dotenv
import pika

# internal imports
from agent.agent_config import AgentConfig
from agent.scenario_processor import process_scenario

load_dotenv()
logger = logging.getLogger(__name__)
logging.basicConfig(format="%(asctime)s %(message)s", level=logging.DEBUG)


MAX_RETRIES = 5
RETRY_DELAY = 10
retry = 0

while retry <= MAX_RETRIES:
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                os.getenv("RABBITMQ_HOST"),
                os.getenv("RABBITMQ_PORT"),
                credentials=pika.PlainCredentials(
                    os.getenv("RABBITMQ_USER"), os.getenv("RABBITMQ_PASSWORD")
                ),
            )
        )
        logger.debug("Connected Successfully")
        break
    except Exception as e:
        logger.debug("Retry %s >> %s", retry, str(e))
        retry += 1
        time.sleep(RETRY_DELAY)


channel = connection.channel()
channel.exchange_declare(exchange="evolve", exchange_type="direct")
channel.queue_declare(queue="evolve_notify")
channel.queue_bind(exchange="evolve", queue="evolve_notify", routing_key="evolve.notify")


# Create the callback function
def callback(ch, method, properties, body):
    # Decode the message

    try:
        message = json.loads(body.decode("utf-8"))
        # Do something with the message
        logger.debug("Submitted message : %s", message)
        input_config_pydantic = AgentConfig.model_validate(message)
        process_scenario(input_config_pydantic)
        logger.debug("Completed processing...")
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as err:
        ch.basic_ack(delivery_tag=method.delivery_tag)
        logger.debug("Errro Awk: %s", str(err))


channel.basic_consume(queue="evolve_notify", on_message_callback=callback)

channel.start_consuming()
