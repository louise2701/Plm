import MySQLdb

def create_database(db_name, db_user, db_password, db_host='localhost'):
    try:
        db = MySQLdb.connect(host=db_host, user=db_user, passwd=db_password)
        cursor = db.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name};")
        print(f"Database '{db_name}' created or already exists.")
        db.close()
    except MySQLdb.Error as e:
        print(f"Error connecting to MySQL: {e}")

# parameters
db_user = 'root'
db_password = 'root'
db_name = 'plm_mgo'

create_database(db_name, db_user, db_password)