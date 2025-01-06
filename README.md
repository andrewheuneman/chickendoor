# Automatic Door Control System (Chicken Coop Door Controller)

## Overview
The **Automatic Door Control System** is a Python-based application designed to automate the opening and closing of a door based on ambient light levels. The system uses a motor driven by the L298N motor controller and integrates a BH1750 light sensor to monitor light intensity. This project is ideal for applications such as chicken coop doors, greenhouse ventilation, or other automation needs requiring controlled door movement.

---

## Features
- **Light-Sensor Integration**: Reads ambient light levels using the BH1750 sensor.
- **Motorized Door Control**: Controls door movement using an L298N motor driver and a motor.
- **Automatic Operation**: Automatically opens or closes the door based on light intensity thresholds.
- **Speed and Direction Control**: Supports precise control of motor speed and direction.
- **Safety Constraints**: Ensures motor operates within pre-configured rope length limits.
- **Error Handling**: Provides meaningful error messages for out-of-bound operations.
- **Graceful Shutdown**: Ensures hardware is safely powered down when the program exits.

---

## System Requirements
- **Python Version**: Python 3.11 or later
- **Dependencies** :
  - `RPi.GPIO` (for GPIO control on Raspberry Pi Zero)
  - `smbus2` (for I2C communication with the BH1750 sensor)
  - Custom modules:
    - `motor_control` (to control the motor via L298N)
    - `light_sensor` (to interface with the BH1750 light sensor)
- **Hardware**:
  - **Motor Controller**: L298N
  - **Light Sensor**: BH1750
  - **Microcontroller**: Raspberry Pi Zero
  - **Motor**: DC motor compatible with the L298N

---

## Motor Control Details
The system uses an **L298N motor controller** to drive the motor. This dual H-Bridge controller allows the motor to run in both forward and backward directions and supports speed control through Pulse Width Modulation (PWM).

### Pin Configuration
| L298N Pin | Raspberry Pi GPIO Pin |
|-----------|------------------------|
| IN1       | GPIO 17               |
| IN2       | GPIO 27               |
| ENA       | GPIO 22               |

### Functionality
- **Forward**: Sets `IN1` to HIGH and `IN2` to LOW.
- **Backward**: Sets `IN1` to LOW and `IN2` to HIGH.
- **Speed Control**: Adjusts the duty cycle of the PWM signal sent to the `ENA` pin.
- **Stop**: Sets both `IN1` and `IN2` to LOW.

### Key Methods
1. **`set_speed(speed)`**: Sets the motor speed as a percentage (0–100%).
2. **`forward()`**: Configures the motor to rotate in the forward direction.
3. **`backward()`**: Configures the motor to rotate in the backward direction.
4. **`stop()`**: Stops the motor.
5. **`run_for(direction, speed, duration)`**: Runs the motor in a specified direction at a given speed for a set duration.
6. **`cleanup()`**: Stops the PWM signal and resets GPIO settings.

---

## Light Sensor Details
The system uses a **BH1750 light sensor** to monitor ambient light levels. This sensor communicates via the I2C protocol and provides precise lux measurements.

### Key Methods
1. **`power_on()`**: Powers on the light sensor module.
2. **`reset()`**: Resets the sensor's data registers.
3. **`read_light()`**: Reads the ambient light level in lux.

### Sensor Configuration
- **Device Address**: `0x23` (default I2C address for BH1750).
- **Operation Mode**: Continuous High-Resolution mode (`0x10`).
- **Lux Calculation**: Converts the sensor's raw data to lux using the formula: 
  
  ```python
  lux = ((data[0] << 8) | data[1]) / 1.2
  ```

### Example Output
```plaintext
Light Level: 450.25 lux
```

---

## Configuration
- **Maximum Rope Length**: Defined as `MAX_ROPE_LENGTH` (default: 16 inches).
- **Minimum Light Level**: Defined as `MIN_LIGHT_LEVEL` (default: 1000 lux).

---

## Usage
1. Connect the L298N motor controller to the Raspberry Pi as per the above pin configuration.
2. Connect the BH1750 light sensor to the Raspberry Pi's I2C pins.
3. Install required Python dependencies:
   ```bash
   pip install RPi.GPIO smbus2
   ```
4. Run the application:
   ```bash
   python automatic_door_control.py
   ```

### Application Behavior
- The system starts by determining the door's initial state based on light levels.
- It continuously monitors light levels and adjusts the door position accordingly.
- Press `Ctrl+C` to exit the program safely.

---

## Error Handling
- **ValueError**: Raised for invalid speed inputs or out-of-bound rope length operations.
- **KeyboardInterrupt**: Safely terminates the application.

---

## Example Output
```plaintext
Initial door is closed
Light Level: 2000 lux
Opening the door...
Light Level: 500 lux
Closing the door...
Error: Cannot move down: Exceeds maximum rope length.
Exiting program...
```

---

## License
This project is released under the MIT License. See the `LICENSE` file for more details.

---

## Contributions
Contributions are welcome! Feel free to submit pull requests or issues.

---

## Contact
For questions or support, contact the repository owner or open an issue on GitHub.



```shell
sudo apt update && sudo apt upgrade -y
sudo apt install bluetooth bluez bluez-tools rfkill

sudo systemctl start bluetooth
sudo systemctl enable bluetooth
rfkill unblock bluetooth


```