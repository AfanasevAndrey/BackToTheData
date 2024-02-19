"""
Модуль в котором реализован класс для отпраки бекапа по http.
"""
import logging

import requests

class HTTPSenderException(Exception):
    pass

class HTTPSender:
    """Класс, который принимает параметры: удаленный хост, удаленный порт, удалённый путь, дефольный порт."""
    def __init__(self, remote_host:str, remote_port:str, remote_path:str, default_ports:str) -> None:
        self.remote_host = remote_host
        self.remote_port = remote_port
        self.remote_path = remote_path
        self.default_ports = default_ports

    def send(self, local_path:str) -> None:
        """Метод класса HTTPSender принимает локальный путь до файла и выполняет отправку по HTTP."""
        print(">>> Sending via HTTP")

        if self.remote_port in self.default_ports:
            url = f"http://{self.remote_host}{self.remote_path}"                        # нужно обработать первый "/", тк он есть в пути
        else:
            url = f"http://{self.remote_host}:{self.remote_port}{self.remote_path}"     # нужно обработать первый "/", тк он есть в пути
        file = {'file': open(local_path, 'rb')}
        try:
            r = requests.post(url, files=file)
            print(f"Send {file} to {url} - Status code: {r.status_code}")
            print(r.text)
            print(f"Raise for status: {r.raise_for_status()}")
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to send {file} to {url}: {e}")
        except ConnectionError:
            logging.error(f"Connection refused")
        except Exception as e:
            logging.error(f"Unexpected error: {e}")