import logging
import sys

from src.config import Config

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    config = Config("config.yaml")

