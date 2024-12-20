import threading
from web_ui import start_flask_app
from dht11_script import is_it_hot, dht_sensor
from tuya_script import on, off
import time

def react_to_temperature(is_hot):
    temperature = get_temperature()
    if is_hot:
        print(f"It's hot! {temperature}°C")
        off()
    elif is_hot is not None:
        print(f"It's cold. {temperature}°C")
        on()

def get_temperature():
    """Reads the temperature from the DHT sensor."""
    try:
        temperature = dht_sensor.temperature
        return temperature
    except RuntimeError as error:
        print(f"RuntimeError: {error.args}")
        return None
    except Exception as error:
        print(f"Exception: {error.args}")
        return None

# Start the Flask app in a separate thread
flask_thread = threading.Thread(target=start_flask_app, daemon=True)
flask_thread.start()

# Main logic loop
try:
    while True:
        temperature_status = is_it_hot()  # Check if it's hot
        react_to_temperature(temperature_status)  # React to temperature
        time.sleep(60)  # Delay between checks
except KeyboardInterrupt:
    print("Program terminated.")