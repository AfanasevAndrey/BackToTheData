"""
Модуль в котором реализован класс вычитывания конфигурации из *.yaml
Чтобы вычитать конфигурацию - нужно создать объект класса Config, конфигурация
будет сохранена в его полях.
"""
from typing import Optional
import logging

import yaml

import constants

class ConfigException(Exception):
    pass


class Config:
    """
    Класс для вычитывания конфигурации из *.yaml, конфигурация хранится в полях
    объекта класса.
    """
    def __init__(self, path: str) -> None:
        """
        Объект класса Config, предназначен для вычитывания и сохранения
        конфигурации из *.yaml файла. Конфигурация хранится в полях объекта.
        Принимает параметры:
            path - строка, содержащая путь к конфигурации *.yaml
        """
        logging.info(f"Trying get config from {path}")
        full_config: dict = {}
        # Вычитываем конфигурацию из переданного файла
        try:
            with open(path) as f:
                full_config = yaml.safe_load(f)
        # Обрабатываем возможные ошибки
        except FileNotFoundError:
            logging.error(f"File {path} does not exist")
            raise FileNotFoundError(
                f"File {path} does not exist"
            )
        except PermissionError:
            logging.error(f"Permission Denied Error: Access is denied to {path}")
            raise PermissionError(
                f"Permission Denied Error: Access is denied to {path}"
            )
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            raise ConfigException(
                f"Unexpected error: {e}"
            )
        logging.info(f"Successfull get config from {path}")
        # Устанавливаем полученные значения в поля класса
        self.url = full_config.get("URL", None)
        self.local_path = full_config.get("LocalPath", None)
        logging.debug(
            f"Resulting configuration: (\n"+
            f"URL: {self.url}\n"+
            f"Sending protocol: {self.send_proto}\n"+
            f"Remote host: {self.remote_host}\n"+
            f"Remote port: {self.remote_port}\n"+
            f"Remote path: {self.remote_path}\n"+
            f"Local path to save Backup: {self.local_path})")
    # Cвойства класса
    @property
    def url(self):
        """
        Ссылка для отправки бэкапа на удаленный хост.
        """
        return self._url
    
    @url.setter
    def url(self, url: Optional[str]):
        if url is not None and url != "":
            self._url = url
            self._parse_url()
        else:
            self._url = None
            self.send_proto = None
            self.remote_host = None
            self.remote_port = None
            self.remote_path = None

    @property
    def send_proto(self):
        """
        Протокол для отправки бэкапа на удаленный хост.
        """
        return self._send_proto

    @send_proto.setter
    def send_proto(self, proto: Optional[str]):
        if proto is not None:
            #Валидируем протокол
            self._validate_send_proto(proto)
        self._send_proto = proto
    
    @property
    def remote_host(self):
        """
        Удаленный хост, куда будет отправлен бэкап.
        """
        return self._remote_host
    
    @remote_host.setter
    def remote_host(self, host: Optional[str]):
        self._remote_host = host
    
    @property
    def remote_port(self):
        """
        Порт удаленного хоста, куда будет отправлен бэкап
        """
        return self._remote_port
    
    @remote_port.setter
    def remote_port(self, port: Optional[str]):
        # Если указан порт, то проверяем его корректность и принимаем
        if port is not None:
            self._validate_port(port)
            self._remote_port = port
        elif self.send_proto is not None:
            # Если порт не указан, то берем дефолтный для протокола
            self._remote_port = self._get_default_port()
        else:
            self._remote_port = None

    @property
    def remote_path(self):
        """
        Путь отправки бэкапа на удаленном хосте
        """
        return self._remote_path
    
    @remote_path.setter
    def remote_path(self, path: Optional[str]):
        if path is not None:
            self._remote_path = path
        elif self.url is None:
            self._remote_path = None 
        else:
            self._remote_path = "/"
    
    #TODO Свойства локального размещения бэкапа
    @property
    def local_path(self):
        """
        Путь для сохранения бэкапа на локальном хосте
        """
        return self._local_path

    @local_path.setter
    def local_path(self, path: Optional[str]):
        if path is not None:
            self._local_path = path
        else:
            logging.error("Local path to save doesnt exist in config file")
            raise ConfigException(
                "Local path to save doesnt exist in config file"
            )
        
    # Методы класса
    def _validate_port(self, port: str) -> None:
        """
        Проверяет корректность порта, если порт не корректен, то выдает ошибку
        Принимает параметры:
            port - порт на удаленном хосте
        """
        try:
            int_port = int(port)
        except ValueError:
            logging.error("Invalid port in URL")
            raise ValueError(
                "Invalid port in URL"
            )
        if int_port not in constants.PORT_RANGE:
            logging.error("Invalid port in URL")
            raise ConfigException(
                "Invalid port in URL"
            )
        
    def _get_default_port(self) -> str:
        """
        Метод для определения дефолтного порта исходя из протокола
        """
        return constants.SEND_PROTOCOLS[self.send_proto]
    
    def _validate_send_proto(self, proto: str):
        """
        Проверяет корректность протокола, если протокол не подерживается, то
        выдает ошибку.
        Принимает параметры:
            proto - протокол отправки
        """
        if proto not in constants.SEND_PROTOCOLS:
            logging.error(f"Unsupported protocol {proto} in URL")
            raise ConfigException(
                f"Unsupported protocol {proto} in URL"
            )
    
    def _parse_url(self):
        """
        Парсим переданный URL чтобы получить из нее параметры для отправки
        бэкапа
        """
        # Определяем протокол и порт
        splitted_doublepoint = self.url.split(":")
        # Если после разбиения вышло 3 элемента в списке, значит порт указан,
        # если 2, значит порт не указан

        # В ссылке есть и протокол и указанный порт
        if len(splitted_doublepoint) == 3:
            self.send_proto = splitted_doublepoint[0]
            self.remote_host = splitted_doublepoint[1].removeprefix("//")
            port_with_path = splitted_doublepoint[-1].split('/')
            # Пути в ссылке может и не быть, проверяем это
            if len(port_with_path) > 1:
                self.remote_port = port_with_path[0]
                self.remote_path = splitted_doublepoint[-1].removeprefix(
                    self.remote_port)
            else:
                self.remote_port = port_with_path[0]
                self.remote_path = None

        # В ссылке есть указанный протокол, но нет порта
        elif len(splitted_doublepoint) == 2:
            
            self.send_proto = splitted_doublepoint[0]
            self.remote_port = None
            host_with_path = splitted_doublepoint[1].removeprefix("//").split("/")
            # Проверяем есть ли путь
            if len(host_with_path) > 1:
                self.remote_host = host_with_path[0]
                self.remote_path = splitted_doublepoint[1].removeprefix(
                    f"//{self.remote_host}")
            else:
                self.remote_host = host_with_path[0]
                self.remote_path = None
        
        # Ссылка некорректного вида
        else:
            logging.error(f"Incorrect URL: {self.url}")
            raise ConfigException(
                f"Incorrect URL: {self.url}"
            )
        