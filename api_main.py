import os
import time
from fastapi import FastAPI
from dotenv import load_dotenv, set_key
from motor_control import MotorControl
from light_sensor import BH1750

ENV_FILE = "door_state.env"

app = FastAPI()

motor = MotorControl()
light = BH1750()


def load_config():
    load_dotenv(ENV_FILE, override=True)
    return {
        "DOOR_LENGTH": int(os.getenv("DOOR_LENGTH", 15)),
        "MIN_LIGHT_LEVEL": int(os.getenv("MIN_LIGHT_LEVEL", 1000)),
        "ROPE_LENGTH": int(os.getenv("ROPE_LENGTH", 15))
    }


def save_config(key, value):
    set_key(ENV_FILE, key, str(value), quote_mode="never")


@app.get("/status")
def get_status():
    """Fetch the current door status."""
    config = load_config()
    light_level = light.read_light()
    door_is_closed = config["ROPE_LENGTH"] >= config["DOOR_LENGTH"]

    return {
        "light_level": light_level,
        "rope_length": config["ROPE_LENGTH"],
        "door_state": "closed" if door_is_closed else "open"
    }


@app.post("/control/open")
def open_door():
    """Manually open the door fully."""
    config = load_config()
    motor.run_for(direction="backward", speed=100, duration=config["DOOR_LENGTH"])
    save_config("ROPE_LENGTH", 0)
    return {"message": "Door opened"}


@app.post("/control/close")
def close_door():
    """Manually close the door fully."""
    config = load_config()
    motor.run_for(direction="forward", speed=100, duration=config["DOOR_LENGTH"])
    save_config("ROPE_LENGTH", config["DOOR_LENGTH"])
    return {"message": "Door closed"}


@app.post("/control/stop")
def stop_door():
    """Stop the motor immediately."""
    motor.stop()
    return {"message": "Motor stopped"}


@app.post("/control/move-up")
def move_up():
    """Move the door up (open) by 1 second interval."""
    config = load_config()
    current_rope_length = config["ROPE_LENGTH"]

    if current_rope_length > 0:
        motor.run_for(direction="backward", speed=100, duration=1)
        new_rope_length = max(0, current_rope_length - 1)  # Reduce by 1 inch
        save_config("ROPE_LENGTH", new_rope_length)
        return {"message": f"Moved up. New rope length: {new_rope_length}"}
    else:
        return {"message": "Door is fully open", "status": "already_open"}


@app.post("/control/move-down")
def move_down():
    """Move the door down (close) by 1 second interval."""
    config = load_config()
    current_rope_length = config["ROPE_LENGTH"]

    if current_rope_length < config["DOOR_LENGTH"]:
        motor.run_for(direction="forward", speed=100, duration=1)
        new_rope_length = min(config["DOOR_LENGTH"], current_rope_length + 1)  # Increase by 1 inch
        save_config("ROPE_LENGTH", new_rope_length)
        return {"message": f"Moved down. New rope length: {new_rope_length}"}
    else:
        return {"message": "Door is fully closed", "status": "already_closed"}


@app.post("/settings/update")
def update_settings(door_length: int, min_light_level: int):
    """Update door length and light level thresholds."""
    save_config("DOOR_LENGTH", door_length)
    save_config("MIN_LIGHT_LEVEL", min_light_level)
    return {"message": "Settings updated", "DOOR_LENGTH": door_length, "MIN_LIGHT_LEVEL": min_light_level}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
