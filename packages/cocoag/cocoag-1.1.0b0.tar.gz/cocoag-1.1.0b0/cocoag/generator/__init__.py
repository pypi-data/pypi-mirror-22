import logging.config
from cocoag.configuration.config import config

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        }
    },

    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "simple",
            "stream": "ext://sys.stdout"
        },
        "file_handler": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "DEBUG",
            "formatter": "simple",
            "filename": config.get("project", "logging_output_file"),
            "maxBytes": 10485760,
            "backupCount": 20,
            "encoding": "utf8"
        }

    },
    "root": {
        "level": "DEBUG",
        "handlers": ["console", "file_handler"]
    }
}

logging.config.dictConfig(LOGGING_CONFIG)