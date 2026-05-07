"""
Configuration Reader Module

Loads and manages test configuration from YAML files.
Supports environment variable overrides for headless mode.
"""

import os
import yaml


def load_config() -> dict:
    """
    Load test configuration from YAML file.

    Reads config/config.yaml and applies environment variable overrides.
    Environment Variables:
        HEADLESS: Set to "true" or "false" to override config.yaml setting

    Returns:
        dict: Configuration dictionary with test settings
    """
    with open("configs/config.yaml") as f:
        config = yaml.safe_load(f)

    # Override headless mode if set via environment variable
    if "HEADLESS" in os.environ:
        config["headless"] = os.environ["HEADLESS"].lower() == "true"

    return config


config = load_config()