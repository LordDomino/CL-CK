CONFIG_PRINT_WARNINGS: bool = False

def printwarning(message: str) -> None:
    if CONFIG_PRINT_WARNINGS:
        print(f"Warning: {message}")