import logging
import os


class FileLoggerSingleton:
    _instance = None

    def __new__(cls, run_id, logs_folder):
        if cls._instance is None:
            cls._instance = super(FileLoggerSingleton, cls).__new__(cls)
            cls._instance.run_id = run_id
            cls._instance.logs_folder = logs_folder
            if not os.path.exists(logs_folder):
                os.makedirs(logs_folder)
        return cls._instance

    def log(self, log_type: str, message: str, level=logging.INFO):
        logger = logging.getLogger(log_type)
        if not logger.handlers:
            logger.setLevel(logging.DEBUG)
            file_handler = logging.FileHandler(
                os.path.join(self.logs_folder, f"{self.run_id}_{log_type}.log")
            )
            formatter = logging.Formatter("%(message)s")
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        logger.log(level, message)
