#!/usr/bin/env python

from pathlib import Path

import matplotlib.pyplot as plt

import numpy as np
import pandas as pd
from loguru import logger

logger.add(
    Path("logs", "data.log"),
    format="{time} | {level} | {message}",
    level="DEBUG",
    rotation="1 MB",
    compression="zip",
)

BASE_PATH = Path(__file__).parent
WIND_GUSTS_PATH = BASE_PATH.joinpath("data", "vejaAtrumsBrazmas.xlsx")
WIND_SPEED_PATH = BASE_PATH.joinpath("data", "vejaAtrumsFaktiskais.xlsx")
AIR_TEMP_PATH = BASE_PATH.joinpath("data", "gaisaTemperatura2022.xlsx")


def read_data(path: Path) -> pd.DataFrame:
    dataframe = pd.read_excel(path, parse_dates=["Datums"])
    dataframe.set_index("Datums", inplace=True)
    return dataframe


def bar_chart() -> None:
    df_wind_speed = read_data(WIND_SPEED_PATH).mean(axis=1)
    df_wind_gusts = read_data(WIND_GUSTS_PATH).max(axis=1) - df_wind_speed

    df_combined = pd.concat(
        [df_wind_speed, df_wind_gusts],
        axis=1,
    )

    df_combined.columns = ["Vidējais", "Maksimālais"]
    df_combined.plot.bar(stacked=True, figsize=(12, 8), color=["#ff7f0e", "#1f77b4"], width=0.6)

    plt.yticks(np.arange(0, df_combined.max().max() + 2.5, 2.5))
    plt.xticks(rotation=45)

    plt.xlabel("Mērījumu Datums")
    plt.ylabel("Vēja ātrums (m/s)")
    plt.title("Vidējais un maksimālais vēja ātrums 2023. gada augustā")
    plt.show()


# def task2() -> None:
#     # create a bar chart
#     df_air_temp = read_data(AIR_TEMP_PATH)
#     plt.bar(df_air_temp, height=10, width=0.8)
#     plt.show()


@logger.catch
def main() -> None:
    bar_chart()


if __name__ == "__main__":
    main()
