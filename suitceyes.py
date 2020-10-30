from board import SCL,SDA
import busio
from adafruit_pca9685 import PCA9685
import time
import threading

class _PCA9685Data:
    index: int
    isDirty: bool
    frequency: int
    lastTick: float
    channels: list
    isOn: bool
    
    def __init__(self, index):
        self.index = index
        self.isDirty = False
        self.frequency = 0
        self.lastTick = -1
        self.channels = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] # 16 channels
        self.isOn = False

"""Vibration motor driver for the PCA9685 i2c board. Can be used for chained boards."""
class VibrationMotorDriver:    
    def __init__(self, *addresses):
        """Initializes the VibrationMotorDriver instance.
        Args:
            *addresses (int): a variable length of addresses to be passed. (e.g. 0x40, 0x41 etc.)
        """
        # Create the I2C bus interface.
        i2c = busio.I2C(SCL, SDA)
        self._boards = []
        self._controllers = []
        index = 0
        self._is_running = False
        for addr in addresses:            
            pca = PCA9685(i2c, address=addr, reference_clock_speed=27000000)
            pca.frequency = 1600
            self._controllers.append(pca)
            self._boards.append(_PCA9685Data(index))
            index=index+1
            
    def __enter__(self):
        self.start()
        return self
    
    def __exit__(self, type, value, trackback):
        self.stop()
            
    def start(self):
        """Starts the driver."""
        if self._is_running == True:
            return
        
        self._is_running = True
        t = threading.Thread(target=self._Loop)
        t.start()
        
    def stop(self):
        """Stops the driver."""
        self._is_running = False        
        for controller in self._controllers:
            for i in range(16):
                controller.channels[i].duty_cycle = 0
            controller.deinit()
    
    def set_frequency(self, index, frequency):
        """Sets the frequency for the PCA9685 board at the given index.

        Args:
            index (int): The board index.
            frequency (int): The frequency in milliseconds.
        """
        if index < 0 or index >= len(self._controllers):
            raise ValueError("The index must be between 0 & " + (len(self._controllers) -1));
        
        frequency = max(0, frequency)
        
        if frequency == self._boards[index].frequency:
            return
        
        self._boards[index].frequency = frequency
        self._boards[index].isDirty = True
    
    def mute_all(self):
        """Mutes all vibration motors across all chained PCA9685 boards."""
        # mute all
        for board in self._boards:            
            for i in range(len(board.channels)):
                board.channels[i] = 0
            board.isDirty = True
    
    def mute(self, index):
        """Mutes all vibrations motors for a given board.
        Args:
            index (int): The index of the board.
        """
        if index < 0 or index >= len(self._controllers):
            raise ValueError("The index must be between 0 & " + (len(self._controllers) -1));
        
        for board in self._boards:
            if board.index == index:                
                for i in range(len(board.channels)):
                    board.channels[i] = 0
                board.isDirty = True
    
    def set_vibration(self, channel, intensity):
        """Sets the vibration for a given channel at the given intensity.
        
        Channels start counting at 0. Channels at board index 1 range from 16 - 31.
        Channels at board index 2 range from 32 - 47 and so forth.
        
        Args:
            channel (int): The channel that should be changed.
            intensity (float): A normalized value between 0 - 1 where 1 = full intensity.
        """
        maxChannels = (len(self._boards) * 16) -1
        if channel > maxChannels:
            raise ValueError("The argument channel is out of range! The value must be between 0 -" + str(maxChannels))
        
        intensity = max(0, min(1, intensity))        
        channelIndex = channel % 16
        boardIndex = int(channel / 16)
        value = round(0xffff * intensity)
        
        # if new value falls below threshold do not make change
        if abs(value - self._boards[boardIndex].channels[channelIndex]) < 0.001:
            return
        
        self._boards[boardIndex].isDirty = True
        self._boards[boardIndex].channels[channelIndex] = value
        
    def set_vibration_batched(self, values : dict):
        """Sets the vibration for list of values.

        Args:
            values (dict): A dictionary where the key is the channel and the value the intensity.
        """
        for index in values:
            self.set_vibration(index, values[index])

    def _Loop(self):
        while self._is_running:
            currentTime = round(time.time() * 1000); # get time in milliseconds
            
            # update each board individually
            for boardIndex in range(0, len(self._boards)):
                board = self._boards[boardIndex]
                controller = self._controllers[board.index]
                
                # calculate whether we have reached the next phase
                nextPhase = board.lastTick + board.frequency
                isNextPhaseReached = currentTime >= nextPhase                
                requiresUpdate = isNextPhaseReached or (board.isDirty and board.isOn)
                
                if requiresUpdate == False:
                    continue                              
                
                # set the values whenever the board is dirty or it was not on
                if board.isDirty or board.isOn == False:
                    board.isDirty = False
                    board.isOn = True
                    for i in range(16):
                        controller.channels[i].duty_cycle = board.channels[i]
                elif board.isOn == True and board.frequency > 0:
                    board.isOn = False
                    for i in range(16):
                        controller.channels[i].duty_cycle = 0
            
                board.lastTick = currentTime

if __name__ == "__main__":
    # Use with "with statement":
    with VibrationMotorDriver(0x40) as driver:
        driver.set_vibration(7, 1.0)
        time.sleep(5)