import time
import adafruit_dht
import board

# Set up DHT11
DHT_PIN = board.D4

# Initialize DHT11
dht_sensor = adafruit_dht.DHT11(pin=DHT_PIN)

def is_it_hot():
    try:
        # Attempt read of temp and humid
        humidity = dht_sensor.humidity
        temperature = dht_sensor.temperature

        if humidity is not None and temperature is not None:
            if temperature >= 22.0:
                return True  # Hot
            elif temperature <= 19.0:
                return False  # Cold
            else:
                print(f"Temperature is okay. {temperature}°C")
        else:
            print("Error reading sensor data.")
            return None  # Return None if reading fails

    except RuntimeError as error:
        print(f"RuntimeError: {error.args}")
        return None
    except Exception as error:
        print(f"Exception: {error.args}")
        return None

if __name__ == "__main__":
    try:
        while True:
            hot_or_cold_status = is_it_hot()
            print(hot_or_cold_status)  # Print status
            time.sleep(2)  # Delay between readings

    except KeyboardInterrupt:
        print("Program terminated by user.")
