#!/usr/bin/env python

from pathlib import Path

from data.visualize import visualize

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
    visualize()


if __name__ == "__main__":
    main()
