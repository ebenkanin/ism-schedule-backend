
# importing packages flask, request, cursor

from flask import Flask, jsonify, request
import models
from psycopg2.extras import RealDictCursor
from flask_cors import CORS


app = Flask(__name__)

CORS(app)


@app.route("/", methods=['POST'])
def get_schedule():
    conn = models.connect_to_db()

    if not conn:
        return jsonify({'Error': 'Unable to connect to database'})

    cursor = conn.cursor(cursor_factory=RealDictCursor)

    try:
        data = request.get_json()

        date = data['current_date']

        cursor.execute("""
        SELECT name, studio_name, mobile_number,studio_number,shift_date,shift_start,shift_end,studio_initials
        FROM schedule where shift_date = %s
        """, (date,))

        response = cursor.fetchall()

        for row in response:
            row['shift_start'] = row['shift_start'].strftime('%H:%M')
            row['shift_end'] = row['shift_end'].strftime('%H:%M')

        return jsonify(response)

    except Exception as e:
        print(e)
        return jsonify({
            "message": f"Could not complete request due to:{str(e)}"
        }), 500

    finally:
        cursor.close()

        conn.close()


if __name__ == '__main__':
    app.run(debug=True)


