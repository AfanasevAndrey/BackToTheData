"""
Модуль в котором реализован класс для отпраки файлов по http.
"""
import logging
ме

import requests

class HTTPSenderException(Exception):
    pass

class HTTPSender:
    """Класс, который принимает параметры: порт, url, путь локальный, путь удалённый и отправляет данные по HTTP."""
    def __init__(self, host:str, remote_port:str, default_ports:str, remote_path:str) -> None:
        self.host = host
        self.remote_port = remote_port
        self.default_ports = default_ports
        self.remote_path = remote_path

    def send(self, local_path):
        # Отправка по HTTP
        print("Sending via HTTP")

        with open(local_path, 'rb') as file:
            for port in self.default_ports:
                url = f"{self.host}:{port}/{self.remote_path}"
                file = {'file': (local_path, file)}
                try:   
                    r = requests.post(url, files=file)
                    print(r.text)
                    print(f"Send {file} to {url} - Status code: {r.status_code}")
                    print(f"Raise for status: {r.raise_for_status()}")
                except requests.exceptions.RequestException as e:
                    logging.error(f"Failed to send {file} to {url}: {e}")
                    raise requests.exceptions.RequestException(
                        f"Failed to send {file} to {url}: {e}"
                    )
                except ConnectionError:
                    logging.error(f"Connection refused")
                    raise ConnectionError(
                        f"Connection refused"
                    )
                except Exception as e:
                    logging.error(f"Unexpected error: {e}")
                    raise HTTPSenderException(
                        f"Unexpected error: {e}"
                    )