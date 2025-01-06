import time
import os
from dotenv import load_dotenv, set_key
from motor_control import MotorControl
from light_sensor import BH1750

ENV_FILE = "door_state.env"


def load_config():
    """Loads configuration variables from .env file."""
    load_dotenv(ENV_FILE, override=True)
    door_length = int(os.getenv("DOOR_LENGTH", 15))
    min_light_level = int(os.getenv("MIN_LIGHT_LEVEL", 1000))
    rope_length = int(os.getenv("ROPE_LENGTH", 15))
    print(f"Loaded config: DOOR_LENGTH={door_length}, MIN_LIGHT_LEVEL={min_light_level}, ROPE_LENGTH={rope_length}")
    return {
        "DOOR_LENGTH": door_length,  # Dynamic length of door travel
        "MIN_LIGHT_LEVEL": min_light_level,  # Light threshold
        "ROPE_LENGTH": rope_length  # Saved state of door (closed by default)
    }


def save_rope_length(rope_length):
    """Writes the updated rope length to .env file."""
    set_key(ENV_FILE, "ROPE_LENGTH", str(rope_length), quote_mode="never")


def calculate_duration(inches):
    """Calculates the time duration required to move the motor a given distance."""
    return inches * (10 / 9)  # 10 seconds for 9 inches at full speed


def adjust_rope_length(motor, target_rope_length, current_rope_length):
    """
    Moves the door to the target rope length, ensuring it stays within valid limits.

    :param motor: MotorControl instance
    :param target_rope_length: Desired rope length (0 for fully open, DOOR_LENGTH for fully closed)
    :param current_rope_length: Current rope length
    :return: Updated rope length
    """
    if target_rope_length < 0 or target_rope_length > load_config()["DOOR_LENGTH"]:
        raise ValueError("Invalid target rope length: Out of bounds.")

    inches_to_move = abs(current_rope_length - target_rope_length)
    duration = calculate_duration(inches_to_move)

    if current_rope_length > target_rope_length:  # Moving up (open door)
        print(f"Opening door by {inches_to_move} inches...")
        motor.run_for(direction="backward", speed=100, duration=duration)
    else:  # Moving down (close door)
        print(f"Closing door by {inches_to_move} inches...")
        motor.run_for(direction="forward", speed=100, duration=duration)

    save_rope_length(target_rope_length)
    return target_rope_length


def main():
    # Initialize motor and sensor
    motor = MotorControl()
    light = BH1750()

    try:
        while True:
            # Reload config each iteration to allow live updates
            config = load_config()
            DOOR_LENGTH = config["DOOR_LENGTH"]
            MIN_LIGHT_LEVEL = config["MIN_LIGHT_LEVEL"]
            rope_length = config["ROPE_LENGTH"]

            light_level = light.read_light()
            door_is_closed = rope_length >= DOOR_LENGTH

            print(f"Light Level: {light_level:.2f} lux")
            print(f"Rope Length: {rope_length} inches")
            print("Door is open" if not door_is_closed else "Door is closed")

            if door_is_closed and light_level > MIN_LIGHT_LEVEL:
                # Open the door fully
                rope_length = adjust_rope_length(motor, target_rope_length=0, current_rope_length=rope_length)
                print(f"Rope Length after opening: {rope_length} inches")
            elif not door_is_closed and light_level < MIN_LIGHT_LEVEL:
                # Close the door fully
                rope_length = adjust_rope_length(motor, target_rope_length=DOOR_LENGTH, current_rope_length=rope_length)
                print(f"Rope Length after closing: {rope_length} inches")
            else:
                print("No action needed.")

            print("\n")

            time.sleep(1)  # Check every second

    except KeyboardInterrupt:
        print("Exiting program...")

    except ValueError as e:
        print(f"Error: {e}")

    finally:
        motor.cleanup()


if __name__ == "__main__":
    main()
