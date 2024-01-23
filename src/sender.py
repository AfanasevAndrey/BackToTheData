"""
Модуль в котором реализован класс, который принимает параметры: протокол, порт, путь локальный, путь удалённый, 
на основании протокола выбирается класс для отправки.
"""
from typing import Optional
import logging

import src.constants
from src.config import Config
from src.senders.sender_http import HTTPSender

class SendFilesException(Exception):
    pass


class SendFiles:
    """
    Класс, который принимает параметры: протокол, порт, путь локальный, путь удалённый, на основании протокола выбирается класс для отправки.
    """
    def __init__(self, proto: str, port: str, local_path: str, remote_path: str) -> None:
        """
        Объект класса SendFiles, предназначен для отправки бекапа на сервер. На основании протокола выбирается класс для отправки.
        Принимает параметры:
            proto       - строка, принимающая значение протокола 
            port        - строка, принимающая значение номера порта
            local_path  - строка, содержащая локальный путь для сохранения бекапа
            remote_path - строка, содержащая удаленный путь для сохранения бекапа
        """
        self.proto = proto
        self.port = port
        self.local_path = local_path
        self.remote_path = remote_path
        
        config = Config()
        host = config.remote_host
        remote_port = config.remote_port
        remote_path = config.remote_path
        default_ports = src.constants.PORT_RANGE    # Заменить на DEFAULT_PORTS

        # На основании протокола выбираем класс для отправки
        if proto == "http":
            # Используем класс HTTPSender
            http_sender = HTTPSender(host, remote_port, remote_path, default_ports)
            http_sender.send(local_path)
        # elif proto == "ftp":
        #     # Используем класс FTPSender
        #     ftp_sender = FTPSender(port, local_path, remote_path)
        #     ftp_sender.send()
        else:
            logging.error(f"Unsupported protocol {proto} in URL")
            raise SendFilesException(
                f"Unsupported protocol {proto} in URL"
            )
        
    




