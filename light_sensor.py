import smbus2
import time


class BH1750:
    # Define constants
    DEVICE_ADDRESS = 0x23  # Default I2C address for BH1750
    POWER_ON = 0x01  # Power on the module
    RESET = 0x07  # Reset data register
    CONTINUOUS_H_RES_MODE = 0x10  # Continuous High-Resolution mode

    def __init__(self, bus=1):
        self.bus = smbus2.SMBus(bus)

    def power_on(self):
        self.bus.write_byte(self.DEVICE_ADDRESS, self.POWER_ON)

    def reset(self):
        self.bus.write_byte(self.DEVICE_ADDRESS, self.RESET)

    def read_light(self):
        # Request a measurement
        self.bus.write_byte(self.DEVICE_ADDRESS, self.CONTINUOUS_H_RES_MODE)
        time.sleep(0.2)  # Wait for measurement to complete

        # Read data (2 bytes)
        data = self.bus.read_i2c_block_data(self.DEVICE_ADDRESS, self.CONTINUOUS_H_RES_MODE, 2)
        # Convert to lux (MSB << 8 | LSB) / 1.2
        lux = ((data[0] << 8) | data[1]) / 1.2
        return lux


if __name__ == "__main__":
    sensor = BH1750()
    sensor.power_on()
    sensor.reset()

    try:
        while True:
            light_level = sensor.read_light()
            print(f"Light Level: {light_level:.2f} lux")
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nExiting program.")
