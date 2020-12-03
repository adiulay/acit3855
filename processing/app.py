import connexion
from connexion import NoContent
import json
import requests
from apscheduler.schedulers.background import BackgroundScheduler

from datetime import datetime

from flask_cors import CORS, cross_origin

import yaml
import logging
import logging.config
import os

import mysql.connector

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
    
# # loading yaml config
# with open('./app_conf.yml', 'r') as f:
#     app_config = yaml.safe_load(f.read())
    
    
# # loading logs config
# with open('log_conf.yml', 'r') as f:
#     log_config = yaml.safe_load(f.read())
#     logging.config.dictConfig(log_config)
    
logger = logging.getLogger('basicLogger')

logger.info("App Conf File: {}".format(app_conf_file))
logger.info("Log Conf File: {}".format(log_conf_file))


def get_stats():
    """ get_stats GET request based on openapi.yaml """
    
    logger.info('GET request stats has been initiated')
    
    try:
        with open(app_config['datastore']['filename'], 'r') as f:
            data_stats_read = f.read()
            
            # converted to object
            data_stats = json.loads(data_stats_read)
            
            show_stats = {
                "num_domestic_baggages": data_stats["num_domestic_baggages"],
                "num_international_baggages": data_stats["num_international_baggages"],
                "total_baggages": data_stats["total_baggages"],
                "last_updated": data_stats["last_updated"]
            }
            
            logger.debug('Get stats with num_domestic_baggages: {}, num_international_baggages: {}, total_baggages: {}'.format(
                show_stats['num_domestic_baggages'],
                show_stats['num_international_baggages'],
                show_stats['total_baggages']
            ))
            
            logger.info('GET request stats has been completed')
            
            return show_stats, 200
            
    except FileNotFoundError:
        error_message = 'Statistics do not exist with status code 404'
        logger.error(error_message)
        
        return {"message": error_message}, 404
        


def populate_stats():
    """ Periodically update stats """
    
    # logger.info('Periodic processing for stats has been initiated')
    
    stats_info = ''
    
    time_now = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    
    try:
        with open(app_config['datastore']['filename'], 'r') as f:
            data_read = f.read()
            stats_info = json.loads(data_read)
            
    except FileNotFoundError:
        with open(app_config['datastore']['filename'], 'w') as f:
            json_template = {
                "num_domestic_baggages": 0,
                "num_international_baggages": 0,
                "total_baggages": 0,
                "last_updated": time_now
            }
            f.write(json.dumps(json_template, indent=4))
        
        with open(app_config['datastore']['filename'], 'r') as f:
            data_read = f.read()
            
            stats_info = json.loads(data_read)
    
    current_time = {
        "timestamp" : stats_info['last_updated']
    }
            
    get_domestic_baggages = requests.get('{}/baggage/domestic'.format(app_config['eventstore']['url']), params=current_time)
    
    get_international_baggages = requests.get('{}/baggage/international'.format(app_config['eventstore']['url']), params=current_time)

    if stats_info['last_updated'] <= time_now:
        if isinstance(get_domestic_baggages.json(), list):
            logger.info('{} events received from domestic baggages GET request with status code {}'.format(
                        len(get_domestic_baggages.json()),
                        get_domestic_baggages.status_code))
            stats_info["num_domestic_baggages"] = stats_info["num_domestic_baggages"] + len(get_domestic_baggages.json())
        else:
            logger.error('PROBLEM, THE OUTPUT IS NOT A LIST SEE HERE')
            logger.error('DOMESTIC: {}'.format(get_domestic_baggages.json()))
        
        if isinstance(get_international_baggages.json(), list):
            stats_info["num_international_baggages"] = stats_info["num_international_baggages"] + len(get_international_baggages.json())
            logger.info('{} events received from international baggages GET request with status code {}'.format(
                        len(get_international_baggages.json()),
                        get_international_baggages.status_code))
        else:
            logger.error('PROBLEM, THE OUTPUT IS NOT A LIST SEE HERE')
            logger.error('INTERNATIONAL: {}'.format(get_international_baggages.json()))


    # Updating data.json file
    stats_info["total_baggages"] = stats_info["num_domestic_baggages"] + stats_info["num_international_baggages"]
    stats_info["last_updated"] = time_now
    
    with open(app_config['datastore']['filename'], 'w') as f:
        f.write(json.dumps(stats_info, indent=4))
        
    # logger.debug("Data store updated with num_domestic_baggages: {}, num_international_baggages: {}, total_baggages: {}".format(
    #     stats_info["num_domestic_baggages"],
    #     stats_info["num_international_baggages"],
    #     stats_info["total_baggages"]
    # ))
    db_conn = mysql.connector.connect(
        host='ec2-52-24-255-57.us-west-2.compute.amazonaws.com',
        user='adiulay', 
        password='P@ssw0rd',
        database='events', 
        port=3306
    )
    
    db_cursor = db_conn.cursor()

    query_domestic = "SELECT COUNT(*) FROM events.domestic_baggage"
    query_international = "SELECT COUNT(*) FROM events.international_baggage"
    
    db_cursor.execute(query_domestic)
    logger.info('BAGGAGE NUMBER')
    logger.info(db_cursor.fetchall()[0][0])
    db_cursor.execute(query_international)
    logger.debug('INTERNATIONAL', db_cursor.fetchall()[0][0])
    
    db_conn.close()
    
    
def init_scheduler():
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(populate_stats,
                  'interval',
                  seconds=app_config['scheduler']['period_sec'])
    sched.start()
    

app = connexion.FlaskApp(__name__, specification_dir='')
CORS(app.app)
app.app.config['CORS_HEADERS'] = 'Content-Type'
app.add_api('openapi.yaml', base_path='/processing', strict_validation=True, validate_responses=True)

if __name__ == '__main__':
    # starting standalone server
    # get_stats()
    # populate_stats()
    init_scheduler()
    app.run(port=8100, use_reloader=False)