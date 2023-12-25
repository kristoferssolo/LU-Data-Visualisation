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

BLUE = "#1f77b4"
ORANGE = "#ff7f0e"
BLACK = "#000000"


def read_data(path: Path) -> pd.DataFrame:
    dataframe = pd.read_excel(path, parse_dates=["Datums"], index_col="Datums", date_format="%d.%m.%Y")
    return dataframe


def bar_chart() -> None:
    df_avg = read_data(WIND_SPEED_PATH).mean(axis=1)
    df_max = read_data(WIND_GUSTS_PATH).max(axis=1) - df_avg

    df_combined = pd.concat(
        [df_avg, df_max],
        axis=1,
    )

    df_combined.columns = ["Vidējais", "Maksimālais"]
    df_combined.plot.bar(stacked=True, figsize=(12, 8), color=[ORANGE, BLUE], width=0.6)

    plt.yticks(np.arange(0, df_combined.max().max() + 2.5, 2.5))
    plt.xticks(rotation=45)  # FIX: don't display time

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

    df["Season"] = df.index.month % 12 // 3 + 1
    df["Season"] = df["Season"].map(SEASONS)

    df["Average"] = df.iloc[:, 0:24].mean(axis=1)

    df_melted = pd.melt(df, id_vars=["Season"], value_name="Temperature", var_name="Time")  # FIX: should be average temperature
    df_melted["Season"] = pd.Categorical(df_melted["Season"], categories=SEASONS.values(), ordered=True)

    _, ax = plt.subplots(figsize=(12, 8))

    box_props = dict(facecolor=BLUE)  # box
    median_props = dict(color=ORANGE)  # median line
    whisker_props = dict(color=BLACK)  # whiskers (vertical line beween box and min/max)
    width = 0.4

    df_melted[df_melted["Season"] == "Rudens"].boxplot(
        by="Season",
        ax=ax,
        grid=False,
        showfliers=0.5,
        boxprops=box_props,
        medianprops=median_props,
        whiskerprops=whisker_props,
        patch_artist=True,
        widths=width,
    )

    df_melted[df_melted["Season"] != "Rudens"].boxplot(
        by="Season",
        ax=ax,
        grid=False,
        showfliers=False,
        boxprops=box_props,
        medianprops=median_props,
        whiskerprops=whisker_props,
        patch_artist=True,
        widths=width,
    )

    min_value = np.floor(df_melted["Temperature"].min() / 5) * 5
    max_value = np.ceil(df_melted["Temperature"].max() / 5) * 5
    tick_step = 5

    plt.yticks(np.arange(min_value, max_value, tick_step))
    plt.title("Gaisa temperatūra Rīgā četros gadalaikos")
    plt.suptitle("")
    plt.ylabel("Gaisa temperatūra (Celsija grādos)")
    plt.xlabel("")
    plt.show()


@logger.catch
def main() -> None:
    # bar_chart()
    box_plot()


if __name__ == "__main__":
    main()
