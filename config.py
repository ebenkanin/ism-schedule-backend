from dotenv import load_dotenv
import os


load_dotenv('.env')


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    DB_PARAMETERS ={
        'host': os.getenv('HOSTNAME'),
        'database': os.getenv('DB_DATABASE'),
        'user': os.getenv('DB_USERNAME'),
        'password': os.getenv('DB_PASSWORD'),
        'port': os.getenv('PORT')
    }


DEBUG = True