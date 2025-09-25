
from loguru import logger

def custom_lint_task(code):
    """Run custom linting on code."""
    logger.info("Linting code: {}", code)
    return f"Linted: {code}"

if __name__ == "__main__":
    print(custom_lint_task("print('Hello')"))