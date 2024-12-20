from flask import Flask, render_template, redirect, url_for
import time
import adafruit_dht
import board
from tuya_script import on, off
from dht11_script import is_it_hot

app = Flask(__name__)

# Set up the DHT sensor
DHT_PIN = board.D4  # Use the D4 pin
dht_sensor = adafruit_dht.DHT11(pin=DHT_PIN)

# Initialize an error log
error_log = []

temperature_status = "Initializing..."

def log_error(message):
    """Logs errors to the error log."""
    global error_log
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    error_log.append(f"[{timestamp}] {message}")
    print(f"Error logged: {message}")  # Print to console for debugging

def get_temperature():
    """Reads the temperature from the DHT sensor."""
    try:
        temperature = dht_sensor.temperature
        return temperature
    except RuntimeError as error:
        log_error(f"RuntimeError: {error.args}")
        return None
    except Exception as error:
        log_error(f"Exception: {error.args}")
        return None

@app.route('/')
def index():
    # Read the temperature
    temperature = get_temperature()
    if temperature is not None:
        temperature_status = f"{temperature}°C"
    else:
        temperature_status = "Sensor Error"

    return render_template('index.html', temperature_status=temperature_status)

@app.route('/turn_on')
def turn_on():
    try:
        on()
    except Exception as error:
        log_error(f"Error in turn_on: {error}")
    return redirect(url_for('index'))

@app.route('/turn_off')
def turn_off():
    try:
        off()
    except Exception as error:
        log_error(f"Error in turn_off: {error}")
    return redirect(url_for('index'))

@app.route('/check_temperature')
def check_temperature():
    """Refresh temperature and redirect to home."""
    global temperature_status
    temperature = get_temperature()
    if temperature is not None:
        temperature_status = f"{temperature}°C"
    else:
        temperature_status = "Sensor Error"
        log_error("Failed to retrieve temperature")
    return redirect(url_for('index'))

@app.route('/error_log')
def show_error_log():
    """Displays the error log."""
    return render_template('error_log.html', error_log=error_log)

def start_flask_app():
    """Starts the Flask app."""
    app.run(host='192.168.178.74', port=5000)
