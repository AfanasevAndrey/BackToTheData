import logging
import sys
import copy

from src.config import Config

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    config = Config("config.yaml")
    config2 = copy.copy(config)



