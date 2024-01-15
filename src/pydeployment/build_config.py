from argparse import ArgumentError, Namespace
from os import environ
from os.path import basename, exists
from sys import argv
from typing import Any, Dict
from dotenv import dotenv_values
from .arg_parser import ArgParser
from .logger import logger


class BuildConfig:
    """
    Class to parse build configuration arguments

    :param system: Name of system OS (Linux, Darwin, or Windows)
    :type system: str
    """
    def __init__(self, system: str) -> None:
        """
        Constructor
        """
        self.logger = logger
        self.system = system

    def _is_set(self, key: str, dict_: Dict[str, Any]) -> bool:
        """
        Check if a key `key` in the dictionary `dict_` exists and is not empty

        :param key: Key to check
        :type key: str
        :param dict_: Dictionary in which to check the key
        :type dict_: Dict[str, Any]
        :return: True if a value in the dictionary exists and is not empty
        :rtype: bool
        """
        return not (key not in dict_.keys() or not dict_[key])

    def _get_config_from_env(self) -> Dict[str, Any]:
        """
        Get configuration from the environment file, either .env in the current
        working directory or the path specified in the `ENV_FILE` environment
        variable

        :return: Variables from environment file
        :rtype: Dict[str, Any]
        """
        if self._is_set("ENV_FILE", environ):
            env_file = environ["ENV_FILE"]
        else:
            env_file = ".env"
        config = dotenv_values(env_file)
        # Coerce target to a single-item list
        if self._is_set("TARGET", config):
            config["TARGET"] = [config["TARGET"]]
        return config

    def _get_config_from_argv(self) -> Dict[str, Any]:
        """
        Get configuration from command line arguments. Any parameters beyond
        the `--` marker are for PyInstaller to handle and are mapped to
        the `PYI_ARGS` key

        :return: Variables from command line
        :rtype: Dict[str, Any]
        """
        parser = ArgParser(self.system)
        args = argv[1:]
        try:
            index = args.index("--")
        except ValueError:
            index = len(args)
        if index < len(args) - 1:
            pyi_args = " ".join(args[index + 1:])
        else:
            pyi_args = ""
        config = vars(parser.parse_args(args[:index]))
        config["PYI_ARGS"] = pyi_args
        return config

    def _validate_target(self, config: Dict[str, Any]) -> int:
        """
        Validate the target files of the configuration

        :param config: Configuration dictionary
        :type config: Dict[str, Any]
        :return: Return code
        :rtype: int
        """
        try:
            if not self._is_set("TARGET", config):
                raise ArgumentError(None, "Target not set")
            targets = config["TARGET"]
            for target in targets:
                if not exists(target):
                    raise ArgumentError(None, f"Target '{target}' not found")
        except ArgumentError as e:
            self.logger.error(e)
            return 1
        return 0

    def _handle_target(self, config: Dict[str, Any]) -> int:
        """
        Handle the target file by making the first argument the target and the
        rest as PyInstaller arguments

        :param config: Configuration dictionary
        :type config: Dict[str, Any]
        :return: Return code
        :rtype: int
        """
        targets = config["TARGET"]
        config["TARGET"] = targets[0]
        args = " ".join(targets[1:])
        if args:
            config["PYI_ARGS"] = " ".join([args, config["PYI_ARGS"]])
        return 0

    def _handle_defaults(self, config: Dict[str, Any]) -> int:
        """
        Assign default values to config parameters based on the spec file

        :param config: Configuration dictionary
        :type config: Dict[str, Any]
        :return: Return code
        :rtype: int
        """
        target = config["TARGET"]
        if target.endswith(".spec"):
            config["MODE"] = "SPEC"
            filename = basename(target.removesuffix(".spec"))
        else:
            config["MODE"] = "PY"
            filename = basename(target.removesuffix(".py"))
        defaults = {
            "FILENAME": filename,
            "ID": f"id.not.found.{filename}",
            "OUTDIR": "dist"
        }
        for k, v in defaults.items():
            if not self._is_set(k, config):
                config[k] = v
        # Special cases for application name and publisher
        defaults = {
            "APPNAME": "FILENAME",
            "PUBLISHER": "AUTHOR"
        }
        for k, v in defaults.items():
            if not self._is_set(k, config):
                config[k] = config[v]
        return 0

    def get_config(self, skip_validation: bool=False) -> Namespace | int:
        """
        Get the build configuration from various sources in order of increasing
        precedence:

        1. The environment file
        2. Command line arguments

        :param system: Name of system OS (Linux, Darwin, or Windows)
        :type system: str
        :param skip_validation: Skip file validation
        :type skip_validation: bool
        :return: Build configuration or return code
        :rtype: argparse.Namespace | int
        """
        # Get configuration from environment file
        env = self._get_config_from_env()
        # Get configuration from command line arguments
        args = self._get_config_from_argv()
        # Override values in env that are not empty in args
        config = env | {
            k: v for k, v in args.items() if k not in env.keys() or v
        }
        # Validate target files
        if not skip_validation:
            result = self._validate_target(config)
            if result:
                return result
        # Handle target file
        self._handle_target(config)
        # Handle defaults
        self._handle_defaults(config)
        return Namespace(**config)
