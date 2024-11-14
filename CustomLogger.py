import logging

class CustomLogger:
    def __init__(self,barra=None,contenedor=None):
        self.logger = logging.getLogger("yt-dlp")  # Usamos el nombre estándar de yt-dlp
        self.logger.setLevel(logging.DEBUG)  # Puedes ajustar el nivel de log según sea necesario
        ch = logging.StreamHandler()  # Define dónde mostrar los logs (en la consola)
        ch.setLevel(logging.DEBUG)  # Establece el nivel de los logs a mostrar
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')  # Formato de los logs
        ch.setFormatter(formatter)
        self.logger.addHandler(ch) 
        self.descargado = False
        self.barraDescarga = barra
        self.contenedor = contenedor
        self.messages = []  # Lista para almacenar los mensajes

    def debug(self, msg):
        if "has already been downloaded" in msg:
            self.messages.append(msg)
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def critical(self, msg):
        self.logger.critical(msg)

    def exception(self, msg):
        self.logger.exception(msg)


