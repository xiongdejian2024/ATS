import logging
import toml
from pathlib import Path

logger = logging.getLogger("jidutest_io.conf_parser")


class IoConfigParser(object):

    def __init__(self, conf_path: Path or str) -> None:
        self.__conf_info = toml.load(conf_path)
        logger.info(self.__conf_info)

    @property
    def io_config(self):
        return self.__conf_info

    @property
    def io_info(self):
        return self.io_config.get("tool", {}).get("pytest", {}).get("ini_options", {}).get("io")

    @property
    def io_dev_info(self):
        return self.io_config.get("tool", {}).get("pytest", {}).get("ini_options", {}).get("io", {}).get("dev")

    @property
    def io_signal_info(self):
        return self.io_config.get("tool", {}).get("pytest", {}).get("ini_options", {}).get("io", {}).get("signal")
