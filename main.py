#!/usr/bin/env python

from pathlib import Path

import matplotlib.pyplot as plt
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


# def visualize() -> None:
#     df_wind_speed = read_data(WIND_SPEED_PATH)
#     df_wind_gusts = read_data(WIND_GUSTS_PATH)
#     index = range(len(df_wind_speed))
#     bar_width = 0.35
#
#     for column, (mean_speed, max_speed) in enumerate(zip(df_wind_speed.columns, df_wind_gusts.columns)):
#         plt.bar(index, df_wind_speed[column], width=bar_width, label=f"Vidējais vēja ātrums {mean_speed}", color="blue")
#         plt.bar(index, df_wind_gusts[column], width=bar_width, label=f"Vēja ātrums brāzmās {mean_speed}", color="orange")
#
#     plt.figure(figsize=(12, 6))
#     plt.xlabel("Mērījumu Datums")
#     plt.ylabel("Vēja ātrums (m/s)")
#     plt.title("Vidējais un maksimālais vēja ātrums 2023. gada augustā")
#     plt.legend()
#     plt.show()


def task2() -> None:
    # create a bar chart
    df_air_temp = read_data(AIR_TEMP_PATH)
    plt.bar(df_air_temp, height=10, width=0.8)
    plt.show()


@logger.catch
def main() -> None:
    # visualize()
    task2()


if __name__ == "__main__":
    main()
