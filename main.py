import logging
import sys
import copy

from src.config import Config
from src.sender import SendFiles

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    config = Config("config.yaml")
    config2 = copy.copy(config)
    send = SendFiles(
        # config.send_proto,
        # config.remote_host,
        # config.remote_port,
        # config.remote_path,
        # config.local_path
        proto = "http",
        remote_host = "172.21.187.156",
        remote_port = "8080",
        remote_path = "/",
        local_path = "/home/tester/test/tmp_client/testfile.txt"
    )