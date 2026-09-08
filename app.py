
# importing packages flask, request, cursor

from flask import Flask, jsonify, request
import models
from psycopg2.extras import RealDictCursor


app = Flask(__name__)


@app.route("/", methods=['GET'])
def get_schedule():
    conn = models.connect_to_db()

    if not conn:
        return jsonify({'Error': 'Unable to connect to database'})

    cursor = conn.cursor(cursorfactory=RealDictCursor)

    try:
        data = request.get_json()

        date = data['current_date']

        cursor.execute("""
        SELECT name, studio_name, mobile_number,studio_number,shift_date,shift_start,shift_end
        FROM schedule where shift_date = %s
        """, (date,))

        response = cursor.fetchall()

        return jsonify(response)

    except Exception as e:
        return jsonify({"message": f"Could not complete request due to:{str(e)}"}), 500

    finally:
        cursor.close()

        conn.close()


