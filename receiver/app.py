import connexion
from connexion import NoContent
import requests
import logging
import logging.config
import yaml

from datetime import datetime
import json
from pykafka import KafkaClient
import os

if "TARGET_ENV" in os.environ and os.environ["TARGET_ENV"] == "test":
    print("In Test Environment")
    app_conf_file = "/config/app_conf.yml"
    log_conf_file = "/config/log_conf.yml"
else:
    print("In Dev Environment")
    app_conf_file = "app_conf.yml"
    log_conf_file = "log_conf.yml"

with open(app_conf_file, 'r') as f:
    app_config = yaml.safe_load(f.read())

# External Logging Configuration
with open(log_conf_file, 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

# # External Application Configuration
# with open('./app_conf.yml', 'r') as f:
#     app_config = yaml.safe_load(f.read())

# # External Loggin Configuration
# with open('log_conf.yml', 'r') as f:
#     log_config = yaml.safe_load(f.read())
#     logging.config.dictConfig(log_config)
    
logger = logging.getLogger('basicLogger')

logger.info("App Conf File: {}".format(app_conf_file))
logger.info("Log Conf File: {}".format(log_conf_file))

def add_baggage_domestic(body):
    # Logs receieves and returns event with status code INFO
    
    logger.info('Received event Add Domestic Baggage - ID: {}'.format(body['baggage_id']))
    
    # post_request_domestic = requests.post(app_config['event_domestic']['url'], json=body) TODO
    client = KafkaClient(hosts='{}:{}'.format(app_config["events"]["hostname"], app_config["events"]["port"]))
    topic = client.topics['{}'.format(app_config["events"]["topic"])]
    producer = topic.get_sync_producer()
    
    msg = {
        "type": "domestic",
        "datetime": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "payload": body
    }
    
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode("utf-8"))
    
    logger.info('Returned event Add Domestic Baggage - ID: {}'.format(body['baggage_id']))
    # logger.info('hello this is a code change')
    
    return NoContent, 201
    
def add_baggage_international(body):
    # Logs receieves and returns event with status code INFO
    
    logger.info('Received event Add International Baggage - ID: {}'.format(body['baggage_id']))
    
    # post_request_international = requests.post(app_config['event_international']['url'], json=body) TODO
    client = KafkaClient(hosts='{}:{}'.format(app_config["events"]["hostname"], app_config["events"]["port"]))
    topic = client.topics['{}'.format(app_config["events"]["topic"])]
    producer = topic.get_sync_producer()
    
    msg = {
        "type": "international",
        "datetime": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "payload": body
    }
    
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode("utf-8"))
    
    logger.info('Returned event Add International Baggage - ID: {}'.format(body['baggage_id']))
    
    return NoContent, 201


app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api('openapi.yaml', base_path='/receiver', strict_validation=True, validate_responses=True)

if __name__ == '__main__':
    app.run(port=8080)