"""
Модуль в котором реализован класс, который принимает параметры: протокол, удаленный хост, удаленный порт, путь удалённый, путь локальный.
На основании протокола выбирается класс для отправки.
"""
from typing import Optional
import logging

import src.constants
from src.senders.sender_http import HTTPSender

class SendFilesException(Exception):
    pass


class SendFiles:
    """
    Класс, который принимает параметры: протокол, удаленный хост, удаленный порт, путь удалённый, путь локальный.
    На основании протокола выбирается класс для отправки.
    """
    def __init__(self, proto: str, remote_host:str, remote_port: str, remote_path: str, local_path: str) -> None:
        """
        Объект класса SendFiles, предназначен для отправки бекапа на сервер. На основании протокола выбирается класс для отправки.
        Принимает параметры:
            proto       - строка, принимающая значение протокола;
            remote_host - строка, принимающая значение домена или IP-адреса;
            remote_port - строка, принимающая значение номера порта;
            remote_path - строка, содержащая удаленный путь для сохранения бекапа;
            local_path  - строка, содержащая локальный путь для сохранения бекапа

        """
        self.proto = proto
        self.remote_host = remote_host
        self.remote_port = remote_port
        self.remote_path = remote_path
        self.local_path = local_path
        
        default_ports = src.constants.PORT_RANGE    # Заменить на DEFAULT_PORTS

        # На основании протокола выбираем класс для отправки
        if proto == "http":
            # Используем класс HTTPSender
            http_sender = HTTPSender(
                self.remote_host, 
                self.remote_port, 
                self.remote_path, 
                default_ports)
            http_sender.send(self.local_path)
        # elif proto == "ftp":
        #     # Используем класс FTPSender
        #     ftp_sender = FTPSender(port, local_path, remote_path)
        #     ftp_sender.send()
        else:
            logging.error(f"Unsupported protocol {proto} in URL")
            raise SendFilesException(
                f"Unsupported protocol {proto} in URL"
            )
        
    




