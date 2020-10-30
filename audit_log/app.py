import connexion
from connexion import NoContent
import json
import requests

from datetime import datetime

import yaml
import logging
import logging.config
from pykafka import KafkaClient
from pykafka.common import OffsetType

# loading yaml config
with open('./app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())

# loading logs config
with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)
    
logger = logging.getLogger('basicLogger')

def get_baggage_domestic(index):
    """ Get Domestic Baggages in History """
    hostname = "{}:{}".format(app_config["events"]["hostname"], app_config["events"]["port"])
    client = KafkaClient(hosts=hostname)
    topic = client.topics[app_config["events"]["topic"]]
    
    # Here we reset the offset on start so that we retrieve
    # messages at the beginning of the message queue.
    # To prevent the for loop from blocking, we set the timeout to
    # 100ms. There is a risk that this loop never stops if the
    # index is large and messages are constantly being received!
    consumer = topic.get_simple_consumer(reset_offset_on_start=True, consumer_timeout_ms=100)
    
    logger.info("Retrieving Domestic Baggage at index {}".format(index))
    
    count = 0
    for msg in consumer:
        msg_str = msg.value.decode("utf-8")
        msg = json.loads(msg_str)
        
        payload = msg["payload"]
        
        # Find the event at the index you want and
        # return code 200
        # i.e., return event, 200
        if msg["type"] == "domestic":
            if count == index:
                return payload, 200
            
            count += 1
        
    logger.error("Could not find Domestic Baggage at index {}".format(index))
    return { "message": "Not Found" }, 404

def get_baggage_international(index):
    """ Get International Baggages in History """
    hostname = "{}:{}".format(app_config["events"]["hostname"], app_config["events"]["port"])
    client = KafkaClient(hosts=hostname)
    topic = client.topics[app_config["events"]["topic"]]
    
    # Here we reset the offset on start so that we retrieve
    # messages at the beginning of the message queue.
    # To prevent the for loop from blocking, we set the timeout to
    # 100ms. There is a risk that this loop never stops if the
    # index is large and messages are constantly being received!
    consumer = topic.get_simple_consumer(reset_offset_on_start=True, consumer_timeout_ms=100)
    
    logger.info("Retrieving International Baggage at index {}".format(index))
    
    count = 0
    for msg in consumer:
        msg_str = msg.value.decode("utf-8")
        msg = json.loads(msg_str)
        
        payload = msg["payload"]
        
        # Find the event at the index you want and
        # return code 200
        # i.e., return event, 200
        if msg["type"] == "international":
            if count == index:
                return payload, 200
            
            count += 1
        
    logger.error("Could not find International Baggage at index {}".format(index))
    return { "message": "Not Found" }, 404

app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api('audit_api.yaml', base_path='/', strict_validation=True, validate_responses=True)

if __name__ == '__main__':
    app.run(port=8110)