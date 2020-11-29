import connexion
from connexion import NoContent

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base
from domestic_baggage import DomesticBaggage
from international_baggage import InternationalBaggage
import datetime

import yaml
import logging
import logging.config

import json
from pykafka import KafkaClient
from pykafka.common import OffsetType
from threading import Thread
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

# loading yaml config
# with open('./app_conf.yml', 'r') as f:
#     app_config = yaml.safe_load(f.read())
    
    
# # loading logs config
# with open('log_conf.yml', 'r') as f:
#     log_config = yaml.safe_load(f.read())
#     logging.config.dictConfig(log_config)
    
logger = logging.getLogger('basicLogger')

logger.info("App Conf File: {}".format(app_conf_file))
logger.info("Log Conf File: {}".format(log_conf_file))

DB_ENGINE = create_engine('mysql+pymysql://{}:{}@{}:{}/{}'.format(
    app_config['datastore']['user'],
    app_config['datastore']['password'],
    app_config['datastore']['hostname'],
    app_config['datastore']['port'],
    app_config['datastore']['db']
    ))
Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)


def add_baggage_domestic(body):
    """ logs domestic baggage (operationID from openapi) into database """
    
    # logs connecting to db
    logger.info('Connecting to DB. Hostname:{}, Port: {}'.format(app_config['datastore']['hostname'], app_config['datastore']['port']))
    
    session = DB_SESSION()
    
    baggage_d = DomesticBaggage(
        body['baggage_id'],
        body['weight_kg'],
        body['destination_province'],
        body['postal-code'],
        body['timestamp']    
    )
    
    session.add(baggage_d)
    
    session.commit()
    session.close()
    
    # logs debug (dev process)
    logger.debug('Stored event Domestic Baggage request with unique id of {}'.format(body['baggage_id']))
    
    return NoContent, 201
    
def add_baggage_international(body):
    """ logs international baggage (operationID from openapi) into database """
    
    # logs connecting to db
    logger.info('Connecting to DB. Hostname:{}, Port: {}'.format(app_config['datastore']['hostname'], app_config['datastore']['port']))
    
    session = DB_SESSION()
    
    baggage_i = InternationalBaggage(
        body['baggage_id'],
        body['weight_kg'],
        body['destination'],
        body['timestamp']
    )
    
    session.add(baggage_i)
    
    session.commit()
    session.close()
    
    # logs debug (dev process)
    logger.debug('Stored event International Baggage request with unique id of {}'.format(body['baggage_id']))
    
    return NoContent, 201

def get_baggage_domestic(timestamp):
    """ Gets new international baggage info after the timestamp """
    
    session = DB_SESSION()
    
    timestamp_datetime = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
    print(timestamp_datetime)
    
    domestic_list = session.query(DomesticBaggage).filter(DomesticBaggage.date_created >= timestamp_datetime)
    
    results_list = []
    
    for baggage in domestic_list:
        results_list.append(baggage.to_dict())
        
    session.close()
    
    logger.info('Query for Domestic Baggage Info after {} returns {} results'.format(timestamp, len(results_list)))
    
    return results_list, 200

def get_baggage_international(timestamp):
    """ Gets new international baggage info after the timestamp """
    
    session = DB_SESSION()
    
    timestamp_datetime = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
    print(timestamp_datetime)
    
    international_list = session.query(InternationalBaggage).filter(InternationalBaggage.date_created >= timestamp_datetime)
    
    results_list = []
    
    for baggage in international_list:
        results_list.append(baggage.to_dict())
        
    session.close()
    
    logger.info('Query for International Baggage Info after {} returns {} results'.format(timestamp, len(results_list)))
    
    return results_list, 200

def process_messages():
    """ Process event messages via multi-threading """
    hostname = "{}:{}".format(app_config["events"]["hostname"], app_config["events"]["port"])
    
    client = KafkaClient(hosts=hostname)
    topic = client.topics[app_config["events"]["topic"]]
    
    # Create a consume on a consumer group, that only reads new messages
    # (uncommitted messages) when the service re-starts (i.e., it doesn't
    # read all the old messages from the history in the message queue).
    
    consumer = topic.get_simple_consumer(
        consumer_group='event_group',
        reset_offset_on_start=False,
        auto_offset_reset=OffsetType.LATEST
    )
    
    # testing out balanced consumer
    # consumer = topic.get_balanced_consumer(
    #     consumer_group='event_group',
    #     zookeeper_connect=zookeeper,
    #     reset_offset_on_start=False,
    #     auto_offset_reset=OffsetType.LATEST
    # )
    
    # This is blocking - it will wait for a new message
    for msg in consumer:
        logger.info('PASSES THROUGH CONSUMER')
        msg_str = msg.value.decode('utf-8')
        msg = json.loads(msg_str)
        logger.info("Message: {}".format(msg))
        
        payload = msg["payload"]
        logger.info('PAYLOAD: {}'.format(payload))
        
        if msg["type"] == "domestic":
            # Stores event domestic from payload to DB
            add_baggage_domestic(payload)
        elif msg["type"] == "international":
            # Stores event international from payload to DB
            add_baggage_international(payload)
        
        # Commit the new message as being read
        consumer.commit_offsets()


app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api('openapi.yaml', base_path='/storage', strict_validation=True, validate_responses=True)

if __name__ == '__main__':
    t1 = Thread(target=process_messages)
    t1.setDaemon(True)
    t1.start()
    app.run(port=8090)