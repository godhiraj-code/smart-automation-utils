import json
import os
from .logger import logger
from .exceptions import ConfigurationError

class Config:
    def __init__(self, config_path=None):
        self.config = self._load_default_config()
        if config_path:
            self._load_user_config(config_path)
        self._load_from_env()

    def _load_default_config(self):
        default_path = os.path.join(os.path.dirname(__file__), "default_config.json")
        try:
            with open(default_path, "r") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load default config: {e}")
            return {}

    def _load_user_config(self, config_path):
        if not os.path.exists(config_path):
            raise ConfigurationError(f"User config file not found: {config_path}")
        
        try:
            with open(config_path, "r") as f:
                user_config = json.load(f)
                self.config.update(user_config)
                logger.info(f"Loaded user configuration from {config_path}")
        except json.JSONDecodeError as e:
            raise ConfigurationError(f"Invalid JSON in config file: {e}")

    def _load_from_env(self):
        # Override with environment variables
        # Prefix: SMART_AUTO_
        for key in self.config.keys():
            env_key = f"SMART_AUTO_{key.upper()}"
            if env_key in os.environ:
                val = os.environ[env_key]
                # Try to convert to the same type as default
                default_val = self.config[key]
                if isinstance(default_val, bool):
                    self.config[key] = val.lower() in ("true", "1", "yes")
                elif isinstance(default_val, int):
                    self.config[key] = int(val)
                else:
                    self.config[key] = val
                logger.debug(f"Overridden {key} from environment variable {env_key}")

    def get(self, key, default=None):
        return self.config.get(key, default)

    def __getattr__(self, name):
        if name in self.config:
            return self.config[name]
        return super().__getattribute__(name)
