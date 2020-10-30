from MqttMessageService import MqttMessageService
from VibrationPatternPlayer import VibrationPatternPlayer
from VestDeviceBase import DummyVestDevice
from HaptogramService import HaptogramService
from I2CVibrationDevice import I2CVestDevice
import json

class TactileBoardListener:
    def __init__(self, message_bus, haptogram_service):
        self.hs = haptogram_service
        message_bus.add_listener("suitceyes/tactile-board/play", self._handle_message)
    
    def _handle_message(self, data):
        payload = json.loads(data.payload)
        self.hs.enqueue(payload)
        return

if __name__ == "__main__":
    with I2CVestDevice(0x40) as vest_device, MqttMessageService() as mb:
        vpp = VibrationPatternPlayer(vest_device)
        hs = HaptogramService(vpp, 2.0, 0.1)
        hs.start()
        listener = TactileBoardListener(mb, hs)

        while True:
            pass
    
        hs.stop()