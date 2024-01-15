from platform import system
from sys import exit
from .build_config import BuildConfig
from .build_linux import BuildLinux
from .build_macos import BuildMacos
from .build_windows import BuildWindows


def main() -> int:
    """
    Build the package

    :return: Return code
    :rtype: int
    """
    system_ = system()
    build_config = BuildConfig(system_)
    config = build_config.get_config()
    if isinstance(config, int):
        return config
    match system_:
        case "Linux":
            build = BuildLinux(config)
        case "Darwin":
            build = BuildMacos(config)
        case "Windows":
            build = BuildWindows(config)
    return build.run()


if __name__ == "__main__":
    exit(main())
