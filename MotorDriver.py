import json
from VestDeviceBase import VestDevice

class MotorDriver(VestDevice):
    """
    Decorator of the VestDevice class. Adds conversion of pin layout
    when setting pin values.
    """
    def __init__(self, vest_device):
        self._vest_device = vest_device
        with open('config.json') as json_file:
            print("loading config file")
            data = json.load(json_file)
            self._config = data["Layout"]
            self._shouldConvert = data["OverridePinLayout"]

    def set_pin(self, index, intensity):
        idx = self._get_pin(index)
        self._vest_device.set_pin(idx, intensity)
    
    def set_frequency(self, frequency):
        self._vest_device.set_frequency(frequency)
    
    def mute(self):
        self._vest_device.mute()

    def set_pins_batched(self, values = dict):
        for key in values:
            self.set_pin(key, values[key])
    
    def _get_pin(self, pin):
        if self._shouldConvert == False:
            return pin
        idx = str(pin)
        if idx in self._config:
            return self._config[idx]

        return pin