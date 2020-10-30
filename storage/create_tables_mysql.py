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
    CREATE TABLE IF NOT EXISTS domestic_baggage(
        id INT NOT NULL AUTO_INCREMENT,
        baggage_id VARCHAR(100) NOT NULL,
        weight_kg INT NOT NULL,
        destination_province VARCHAR(250) NOT NULL,
        postal_code VARCHAR(7) NOT NULL,
        timestamp VARCHAR(100) NOT NULL,
        date_created VARCHAR(100) NOT NULL,
        CONSTRAINT domestic_baggage_PK PRIMARY KEY (id)
    )
    '''
)

db_cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS international_baggage(
        id INT NOT NULL AUTO_INCREMENT,
        baggage_id VARCHAR(100) NOT NULL,
        weight_kg INT NOT NULL,
        destination VARCHAR(250) NOT NULL,
        timestamp VARCHAR(100) NOT NULL,
        date_created VARCHAR(100) NOT NULL,
        CONSTRAINT international_baggage_PK PRIMARY KEY (id)
    )
    '''
)

db_conn.commit()
db_conn.close()


