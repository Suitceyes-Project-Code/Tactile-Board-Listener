# Tactile Board Listener
This repository contains code for the Python scripts that are responsible for listening for messages that arrive from the Tactile Board application through the MQTT message bus.

## Requirements
- For USB: PyCmdMessenger (https://pypi.org/project/PyCmdMessenger/)
- For BLE: bluepy (https://pypi.org/project/bluepy/)
- For I2C: adafruit-pca9685 (https://github.com/adafruit/Adafruit_Python_PCA9685)
- Paho MQTT Client: paho-mqtt (https://pypi.org/project/paho-mqtt/)

## Setup
Install the above named python packages via pip. To execute, simply run the command from the root directory:
```
python Main.py
```

If you have your own MQTT message broker, change the required credentials in the provided config.json file.

By default the program runs with an I2C interface. If you are using a device connected through USB change line 20 in Main.py to:
```python
with UsbVestDevice("YOUR_COM_PORT") as vest_device, MqttMessageService() as mb:
```
Use the respective COM port (e.g. "COM3").

## Authors
- James Gay (james.gay@hs-offenburg.de)