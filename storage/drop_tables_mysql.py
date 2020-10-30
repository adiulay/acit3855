import mysql.connector

db_conn = mysql.connector.connect(
    host='ec2-52-24-255-57.us-west-2.compute.amazonaws.com',
    user='adiulay', 
    password='P@ssw0rd',
    database='events', 
    port=3306
)

db_cursor = db_conn.cursor()

db_cursor.execute(
    '''
    DROP TABLE IF EXISTS domestic_baggage
    '''
)

db_cursor.execute(
    '''
    DROP TABLE IF EXISTS international_baggage
    '''
)

db_conn.commit()
db_conn.close()


