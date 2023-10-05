from flask import Flask, request, abort
import logging
import os
import time

import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

# Check and create if logs directory doesn't exist
if not os.path.exists('logs'):
    os.makedirs('logs')

# Define logging configuration
logging.basicConfig(filename='logs/app.log', 
                    format='%(asctime)s - test_api - %(levelname)s - %(message)s', 
                    level=logging.INFO)

sentry_sdk.init(
    dsn="https://c6d27896735ad104ac268539033bfb73@o4505994371596288.ingest.sentry.io/4505999352594432",
    integrations=[
        FlaskIntegration(),
    ],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0
)



app = Flask(__name__)

@app.route('/charge', methods=['POST'])
def charge():
    # Simulate successful credit card charge
    if request.json.get('order') == '1234':
        logging.info("INFO: Charged order 1234 successfully")
        return {"status": "Order 1234 charged successfully"}
    # Simulate failed credit card charge
    elif request.json.get('order') == '4567':
        logging.error("ERROR: Credit card charge failed for order 4567")
        return {"status": "Order 4567 charge failed"}, 400
    else:
        abort(400, 'Invalid order')

@app.route('/slow-query', methods=['GET'])
def slow_query():
    # Simulate a database wait time
    time.sleep(3)  # waits for 3 seconds
    # Fake a successful database query
    if request.args.get('table') == 'customers':
        logging.info("INFO: Query on customers table took 500ms")
        return {"status": "Query on customers table took 500ms"}
    # Fake a slow database query
    else:
        logging.warning("WARN: Slow database query took 3000ms")
        return {"status": "Slow database query took 3000ms"}

@app.route('/invalid-login', methods=['POST'])
def invalid_login():
    username = request.json.get('username')
    password = request.json.get('password')
    # Log successful login attempt
    if username == 'admin' and password == 'password':
        logging.info(f"INFO: User {username} logged in successfully")
        return {"status": f"User {username} logged in successfully"}
    # Log unauthorized login attempt
    else:
        logging.error(f"ERROR: Unauthorized login attempt from 192.168.1.1 with invalid credentials for user {username}")
        return {"status": f"Unauthorized login attempt from 192.168.1.1 for user {username}"}, 401

@app.route('/cause-load', methods=['GET'])
def cause_load():
    # Log normal CPU load
    if request.args.get('load') < '80':
        logging.info("INFO: CPU usage on server xyz at 50%")
        return {"status": "CPU usage on server xyz at 50%"}
    # Log high CPU load
    else:
        logging.error("ERROR: CPU usage on server xyz spiked to 99%")
        return {"status": "CPU usage on server xyz spiked to 99%"}, 429

@app.route('/')
def index():
    # Trigger a successful operation
    if request.args.get('operation') == 'success':
        logging.info("INFO: Operation completed successfully")
        return {"status": "Operation completed successfully"}
    # Trigger an unhandled exception
    else:
        logging.error("ERROR: Unhandled IndexError: list index out of range")
        return {"status": "Unhandled exception"}, 500

@app.route('/debug-sentry')
def trigger_error():
    denominator = 0
if denominator != 0:
    division_by_zero = 1 / denominator
else:
    division_by_zero = None

if __name__ == "__main__":
    app.run(debug=True)

