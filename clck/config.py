CONFIG_PRINT_WARNINGS: bool = False
CONFIG_PRINT_DEBUGS: bool = False

def print_warning(message: str) -> None:
    if CONFIG_PRINT_WARNINGS:
        print(f"Warning: {message}")


def print_debug(message: object) -> None:
    if CONFIG_PRINT_DEBUGS:
        print(f"Debug: {message}")