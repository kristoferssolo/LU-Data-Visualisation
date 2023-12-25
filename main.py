#!/usr/bin/env python

import platform
import subprocess
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from loguru import logger
from matplotlib.backends.backend_pdf import PdfPages


logger.add(
    Path("logs", "data.log"),
    format="{time} | {level} | {message}",
    level="INFO",
    rotation="1 MB",
    compression="zip",
)

BASE_PATH = Path(__file__).parent
WIND_GUSTS_PATH = BASE_PATH.joinpath("data", "vejaAtrumsBrazmas.xlsx")
WIND_SPEED_PATH = BASE_PATH.joinpath("data", "vejaAtrumsFaktiskais.xlsx")
AIR_TEMP_PATH = BASE_PATH.joinpath("data", "gaisaTemperatura2022.xlsx")
PDF_PATH = BASE_PATH.joinpath("plots.pdf")

BLUE = "#1f77b4"
ORANGE = "#ff7f0e"
BLACK = "#000000"


@logger.catch
def read_data(path: Path) -> pd.DataFrame:
    dataframe = pd.read_excel(path, parse_dates=["Datums"], index_col="Datums", date_format="%d.%m.%Y")
    logger.info(f"Read data from {path}")
    return dataframe


@logger.catch
def create_bar_chart() -> plt.Figure:
    df_avg: pd.Series = read_data(WIND_SPEED_PATH).mean(axis=1)
    df_max: pd.Series = read_data(WIND_GUSTS_PATH).max(axis=1) - df_avg

    df_combined: pd.DataFrame = pd.concat(
        [df_avg, df_max],
        axis=1,
    )

    fig, ax = plt.subplots(figsize=(12, 8))

    df_combined.columns = ["Vidējais", "Maksimālais"]
    df_combined.plot.bar(
        stacked=True,
        figsize=(12, 8),
        color=[ORANGE, BLUE],
        width=0.6,
        ax=ax,
    )

    date_format = df_combined.index.strftime("%d.%m.%Y")
    ax.set_xticks(np.arange(len(date_format)))
    ax.set_xticklabels(date_format, rotation=45)
    ax.set_yticks(np.arange(0, df_combined.max().max() + 2.5, 2.5))

    ax.set_title("Vidējais un maksimālais vēja ātrums 2023. gada augustā")
    ax.set_xlabel("Mērījumu Datums")
    ax.set_ylabel("Vēja ātrums (m/s)")

    logger.info("Created bar chart")

    return fig


SEASONS: dict[int, str] = {
    1: "Ziema",
    2: "Pavasaris",
    3: "Vasara",
    4: "Rudens",
}


@logger.catch
def create_box_plot() -> plt.Figure:
    df: pd.DataFrame = read_data(AIR_TEMP_PATH)

    df["Season"] = df.index.month % 12 // 3 + 1
    df["Season"] = df["Season"].map(SEASONS)

    df["Average"] = df.iloc[:, 0:24].mean(axis=1)

    seasonal_data: list[pd.Series] = [df[df["Season"] == season]["Average"] for season in SEASONS.values()]

    fig, ax = plt.subplots(figsize=(12, 8))

    ax.boxplot(
        seasonal_data,
        labels=SEASONS.values(),
        showfliers=True,
        boxprops=dict(facecolor=BLUE),  # box
        medianprops=dict(color=ORANGE),  # median line
        whiskerprops=dict(color=BLACK),  # whiskers (vertical line between box and min/max)
        patch_artist=True,
        widths=0.4,
    )

    min_value: float = np.floor(df["Average"].min() / 5) * 5
    max_value: float = np.ceil(df["Average"].max() / 5) * 5
    tick_step: int = 5

    ax.set_yticks(np.arange(min_value, max_value, tick_step))
    ax.set_title("Gaisa temperatūra Rīgā četros gadalaikos")
    ax.set_ylabel("Gaisa temperatūra (Celsija grādos)")
    ax.set_xlabel("")

    logger.info("Created box plot")

    return fig


@logger.catch
def open_pdf(pdf_path: Path) -> None:
    logger.info(f"Opening {pdf_path}")

    system = platform.system().lower()
    if system == "linux":
        subprocess.run(["xdg-open", pdf_path], check=True)
    elif system == "windows":
        subprocess.run(["start", "", pdf_path], check=True)
    elif system == "darwin":  # macOS
        subprocess.run(["open", pdf_path], check=True)
    else:
        logger.warning(f"Unsupported platform: {system}. Please open the PDF manually.")


@logger.catch
def main() -> None:
    with PdfPages(PDF_PATH) as pdf:
        fig1 = create_bar_chart()
        pdf.savefig(fig1)
        plt.close(fig1)

        fig2 = create_box_plot()
        pdf.savefig(fig2)
        plt.close(fig2)

    try:
        open_pdf(PDF_PATH)
    except Exception as e:
        logger.error(e)
        logger.warning("Something went wrong while opening the PDF. Please open it manually.")


if __name__ == "__main__":
    main()
