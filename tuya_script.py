import tinytuya

# Device credentials
DEVICE_ID = "50621376c4dd57129cda"
LOCAL_KEY = "w1RJuuxG=Oif4]Ov"
IP_ADDRESS = "192.168.178.30"

# Device object
device = tinytuya.Device(DEVICE_ID, IP_ADDRESS, LOCAL_KEY, version=3.3)

def on():
    device.set_status(True)

def off():
    device.set_status(False)


