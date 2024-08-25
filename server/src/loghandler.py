import logging
import os

class LogHandler:
    def __init__(self, name, filename, directory='logs', file_formatter=None, cli_formatter=None, level=logging.DEBUG):
        filename = os.path.join(directory, filename)
        os.makedirs(directory, exist_ok=True)

        if not file_formatter:
            file_formatter = logging.Formatter(
                '[%(name)s] %(asctime)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )

        if not cli_formatter:
            try:
                import colorlog

                cli_formatter = colorlog.ColoredFormatter(
                '%(log_color)s[%(name)s] %(asctime)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S',
                log_colors={
                    'DEBUG': 'cyan',
                    'INFO': 'green',
                    'WARNING': 'yellow',
                    'ERROR': 'red',
                    'CRITICAL': 'red,bg_white',
                }
            )
            except ImportError:
                cli_formatter = file_formatter

        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(cli_formatter)
        self.logger.addHandler(stream_handler)

        file_handler = logging.FileHandler(filename)
        file_handler.setFormatter(file_formatter)
        file_handler.setLevel(level)
        self.logger.addHandler(file_handler)

    def get_logger(self):
        return self.logger