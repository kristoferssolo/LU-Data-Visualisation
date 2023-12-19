#!/usr/bin/env python

from pathlib import Path

from loguru import logger

logger.add(
    Path("logs", "data.log"),
    format="{time} | {level} | {message}",
    level="DEBUG",
    rotation="1 MB",
    compression="zip",
)


@logger.catch
def main() -> None:
    pass


if __name__ == "__main__":
    main()
