import yaml
import os

config_path = os.path.join(os.path.dirname(__file__), "config.yaml")


class Config:

    def __init__(self, config_path):
        self.config_path = config_path
        with open(config_path, "r", encoding="utf-8") as file:
            self.config = yaml.load(file, Loader=yaml.FullLoader)

    def __str__(self):
        return str(self.config)

    def load(self, config_path):
        self.config_path = config_path
        with open(config_path, "r", encoding="utf-8") as file:
            self.config = yaml.load(file, Loader=yaml.FullLoader)

    def save(self):
        with open(self.config_path, "w") as file:
            yaml.dump(self.config, file)


main_config = Config(config_path)

__all__ = ["main_config"]
