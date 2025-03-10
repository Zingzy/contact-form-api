import tomli
import os
import re
from typing import Dict, Any
from pathlib import Path


class Config:
    def __init__(self):
        config_path = Path("config.toml")
        if not config_path.exists():
            raise FileNotFoundError("config.toml not found")

        with open(config_path, "rb") as f:
            self._config = tomli.load(f)

        # Replace environment variables in webhook URI
        webhook_uri = self._config["webhook"]["uri"]
        if webhook_uri.startswith("${") and webhook_uri.endswith("}"):
            env_var = webhook_uri[2:-1]
            self._config["webhook"]["uri"] = os.environ.get(env_var)

    @property
    def server(self) -> Dict[str, Any]:
        return self._config["server"]

    @property
    def ratelimit(self) -> Dict[str, Any]:
        return self._config["ratelimit"]

    @property
    def webhook_uri(self) -> str:
        return self._config["webhook"]["uri"]

    @property
    def email_regex(self) -> re.Pattern:
        return re.compile(self._config["validation"]["email_regex"])

    @property
    def logging(self) -> Dict[str, Any]:
        return self._config["logging"]


# Create a singleton instance
config = Config()
