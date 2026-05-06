import yaml

def load_config():
    with open("configs/config.yaml") as f:
        return yaml.safe_load(f)
    config["headless"] = os.getenv("HEADLESS", "true").lower() == "true"

config = load_config()