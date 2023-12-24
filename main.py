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
    dataframe = pd.read_excel(path, date_parser="Datums", index_col="Datums")
    return dataframe


def get_season(month: int) -> str | None:
    if month in [12, 1, 2]:
        return "Ziema"
    elif month in [3, 4, 5]:
        return "Pavasaris"
    elif month in [6, 7, 8]:
        return "Vasara"
    elif month in [9, 10, 11]:
        return "Rudens"
    else:
        return None


def bar_chart() -> None:
    df_avg = read_data(WIND_SPEED_PATH).mean(axis=1)
    df_max = read_data(WIND_GUSTS_PATH).max(axis=1) - df_avg

    df_combined = pd.concat(
        [df_avg, df_max],
        axis=1,
    )

    df_combined.columns = ["Vidējais", "Maksimālais"]
    df_combined.plot.bar(stacked=True, figsize=(12, 8), color=["#ff7f0e", "#1f77b4"], width=0.6)

    plt.yticks(np.arange(0, df_combined.max().max() + 2.5, 2.5))
    plt.xticks(rotation=45)

    plt.title("Vidējais un maksimālais vēja ātrums 2023. gada augustā")
    plt.xlabel("Mērījumu Datums")
    plt.ylabel("Vēja ātrums (m/s)")
    plt.show()


SEASONS = {
    1: "Ziema",
    2: "Pavasaris",
    3: "Vasara",
    4: "Rudens",
}


def box_plot() -> None:
    df = read_data(AIR_TEMP_PATH)
    df.index = pd.to_datetime(df.index, format="%d.%m.%Y")

    df["Season"] = df.index.month % 12 // 3 + 1
    df["Season"] = df["Season"].map(SEASONS)

    plt.title("Gaisa temperatūra Rīgā četros gadalaikos")
    plt.ylabel("Gaisa temperatūra (Celsija grādos)")
    # plt.show()


@logger.catch
def main() -> None:
    # bar_chart()
    box_plot()


if __name__ == "__main__":
    main()
