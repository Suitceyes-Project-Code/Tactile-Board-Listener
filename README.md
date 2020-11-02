# Tactile Board Listener
This repository contains code for the Python scripts that are responsible for listening for messages that arrive from the Tactile Board<sup>[1](#ft_1)</sup> application through the MQTT message bus.

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

## Citing
If you use this code in your research, you must cite:

<a name=ft_1><sup>1</sup></a> Arthur Theil, Lea Buchweitz, James Gay, Eva Lindell, Li Guo, Nils-Krister Persson, and Oliver Korn. 2020. Tactile Board: A Multimodal Augmentative and Alternative Communication Device for Individuals with Deafblindness. In 19th International Conference on Mobile and Ubiquitous Multimedia (MUM 2020), November 22–25, 2020, Essen, Germany. ACM, New York, NY, USA, 6 pages. https://doi.org/10.1145/3428361.3428465
