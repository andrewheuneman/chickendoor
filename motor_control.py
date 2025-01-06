import RPi.GPIO as GPIO
import time

class MotorControl:
    def __init__(self, in1 = 17, in2 = 27, ena= 22, pwm_frequency=100):
        """
        Initialize the motor control.

        :param in1: GPIO pin connected to IN1 on L298N
        :param in2: GPIO pin connected to IN2 on L298N
        :param ena: GPIO pin connected to ENA on L298N
        :param pwm_frequency: Frequency for PWM (default: 100 Hz)

        # Pin definitions
        IN1 = 17  # GPIO pin connected to IN1 on L298N
        IN2 = 27  # GPIO pin connected to IN2 on L298N
        ENA = 22  # GPIO pin connected to ENA on L298N
        """
        self.IN1 = in1
        self.IN2 = in2
        self.ENA = ena

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.IN1, GPIO.OUT)
        GPIO.setup(self.IN2, GPIO.OUT)
        GPIO.setup(self.ENA, GPIO.OUT)

        self.pwm = GPIO.PWM(self.ENA, pwm_frequency)
        self.pwm.start(0)  # Start PWM with 0% duty cycle

    def set_speed(self, speed):
        """Sets the motor speed (0 to 100%)."""
        if 0 <= speed <= 100:
            self.pwm.ChangeDutyCycle(speed)
        else:
            raise ValueError("Speed must be between 0 and 100.")

    def forward(self):
        """Sets the motor to rotate forward."""
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)

    def backward(self):
        """Sets the motor to rotate backward."""
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.HIGH)

    def stop(self):
        """Stops the motor."""
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.LOW)

    def run_for(self, direction, speed, duration):
        """
        Runs the motor in a specified direction and speed for a certain duration.

        :param direction: "forward" or "backward"
        :param speed: Speed percentage (0 to 100)
        :param duration: Duration to run the motor (in seconds)
        """
        if direction == "forward":
            self.forward()
        elif direction == "backward":
            self.backward()
        else:
            raise ValueError("Direction must be 'forward' or 'backward'.")

        self.set_speed(speed)
        time.sleep(duration)
        self.stop()

    def cleanup(self):
        """Stops PWM and cleans up GPIO settings."""
        if self.pwm is not None:
            try:
                self.pwm.stop()
            except Exception as e:
                print(f"Warning: Failed to stop PWM: {e}")
            self.pwm = None  # Set PWM to None to avoid multiple stops
        GPIO.cleanup()

    def __del__(self):
        """Destructor to ensure cleanup is called when the object is deleted."""
        try:
            self.cleanup()
        except Exception as e:
            print(f"Warning: Cleanup in __del__ failed: {e}")
# Example usage
if __name__ == "__main__":
    motor = None
    try:
        motor = MotorControl()

        print("Running motor forward at 50% speed for 5 seconds...")
        motor.run_for(direction="forward", speed=100, duration=10)
        time.sleep(10)
        print("Running motor backward at 75% speed for 3 seconds...")
        motor.run_for(direction="backward", speed=100, duration=10)

    except KeyboardInterrupt:
        print("Exiting program...")

    finally:
        motor = None
