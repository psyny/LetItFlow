import os
import json

from backend.libs.psn.filemanager.filemanager import FileManager

class AppConfig:
    _instance = None
    _config = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AppConfig, cls).__new__(cls)
            cls._instance.initialize()
        return cls._instance
    
    def initialize(self):
        self.load_config()

    def load_config(self):
        """Load configuration from appconfig.json and environment variables."""
        # Load environment variables
        self._config = dict(os.environ)

        # Load appconfig.json
        app_config = FileManager.loadJsonFile("appconfig.json", [])
        if app_config:
            # Override environment variables with appconfig.json values
            self._config.update(app_config)

    def get(self, key: str):
        """Get the configuration value by key."""
        return self._config.get(key, None)

    def set(self, key: str, value):
        """Set a configuration value by key."""
        self._config[key] = value

    def get_all(self):
        """Return all configuration key-value pairs."""
        return self._config