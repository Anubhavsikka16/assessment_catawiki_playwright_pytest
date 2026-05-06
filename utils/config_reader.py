import yaml
import os


def load_config():

    with open("configs/config.yaml") as f:
        config = yaml.safe_load(f)

    # Check if HEADLESS was passed from terminal
    if "HEADLESS" in os.environ:

        config["headless"] = (
            os.environ["HEADLESS"].lower() == "true"
        )

    return config


config = load_config()