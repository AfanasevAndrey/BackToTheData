
class FTPSenderException(Exception):
    pass

#TODO 
class FTPSender:
    def __init__(self, port: str, local_path: str, remote_path: str) -> None:
        self.port = port
        self.local_path = local_path
        self.remote_path = remote_path

    def send(self):
        # Отправка по FTP
        print("Sending via FTP")