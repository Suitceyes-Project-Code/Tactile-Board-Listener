from abc import ABC, abstractmethod

class VestDevice(ABC):
    
    @abstractmethod
    def set_pin(self, index, intensity):
        pass

    @abstractmethod
    def set_pins_batched(self, values = dict):
        pass
    
    @abstractmethod
    def set_frequency(self, frequency):
        pass
    
    @abstractmethod
    def mute(self):
        pass
    
class DummyVestDevice(VestDevice):
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, tb):
        return True

    def set_pin(self, index, intensity):
        if intensity > 0:
            print("Motor at " + str(index) + " vibrating with intensity of " + str(intensity * 100) + "%")
        #pass
    
    def set_frequency(self, frequency):
        pass
    
    def mute(self):
        pass

    def set_pins_batched(self, values = dict):
        for key in values:
            self.set_pin(key, values[key])