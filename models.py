import psycopg2
from config import Config
from psycopg2 import OperationalError
from flask import Flask, request, jsonify
from psycopg2.extras import RealDictCursor


app = Flask(__name__)


# def connect_to_db():
#     try:
#         conn = psycopg2.connect(
#             host=Config.DB_PARAMETERS['host'],
#             database=Config.DB_PARAMETERS['database'],
#             user=Config.DB_PARAMETERS['user'],
#             password=Config.DB_PARAMETERS['password'],
#             port=Config.DB_PARAMETERS['port']
#         )
#         if not conn:
#             print('Unable to connect to database')
#         print('Connected to database successfully')
#         return conn
#     except OperationalError as e:
#         print(f"Unable to connect to Database: {e}")


def connect_to_db():
    print("ABOUT TO CONNECT TO DATABASE")

    try:
        if Config.DATABASE_URL:
            conn = psycopg2.connect(Config.DATABASE_URL,connect_timeout=10)
        else:
            conn = psycopg2.connect(
                host=Config.DB_PARAMETERS['host'],
                database=Config.DB_PARAMETERS['database'],
                user=Config.DB_PARAMETERS['user'],
                password=Config.DB_PARAMETERS['password'],
                port=Config.DB_PARAMETERS['port']
            )

        print('Connected to database successfully')
        print("DATABASE CONNECTION SUCCESSFUL")

        return conn

    except OperationalError as e:
        print(f"Unable to connect to Database: {e}")


def create_schedule_table():

    with app.app_context():

        # connect to the database
        conn = connect_to_db()

        if not conn:
            print('Unable to connect to database')
            return

        cursor = conn.cursor()
        try:
            print('executing commands')
            cursor.execute(

                """
                CREATE TABLE IF NOT EXISTS schedule(
                name VARCHAR(50),
                studio_name VARCHAR(50),
                mobile_number VARCHAR(15),
                studio_number VARCHAR(15),
                shift_date DATE,
                shift_start TIME,
                shift_end TIME,
                studio_initials VARCHAR(3))
                """
            )
            conn.commit()
            print('table created successfully')

        except OperationalError as e:
            return f"Unable to complete task due to error:{e}", 400

        finally:
            cursor.close()
            conn.close()


