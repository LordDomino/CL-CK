CONFIG_PRINT_WARNINGS: bool = True
CONFIG_PRINT_DEBUGS: bool = True

def printwarning(message: str) -> None:
    if CONFIG_PRINT_WARNINGS:
        print(f"Warning: {message}")


def printdebug(message: object) -> None:
    if CONFIG_PRINT_DEBUGS:
        print(f"Debug: {message}")