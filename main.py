#!/usr/bin/env python

"""
Author: Kristiāns Francis Cagulis, kc22015
Date: 25.12.2023.
Github: https://github.com/kristoferssolo/LU-Data-Visualisation
Dependencies: matplotlib, numpy, pandas, loguru, openpyxl

This script generates two plots from Excel files and saves them to a PDF file.
Excel files can be stored in the same directory as this script or in a subdirectory called "data".
"""


import platform
import subprocess
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from loguru import logger
from matplotlib.backends.backend_pdf import PdfPages


BASE_PATH = Path(__file__).parent
WIND_GUSTS_FILENAME = "vejaAtrumsBrazmas.xlsx"
WIND_SPEED_FILENAME = "vejaAtrumsFaktiskais.xlsx"
AIR_TEMP_FILENAME = "gaisaTemperatura2022.xlsx"
PDF_FILENAME = "plots.pdf"

BLUE = "#1f77b4"
ORANGE = "#ff7f0e"
BLACK = "#000000"

# Setup logger
logger.add(
    BASE_PATH.joinpath("logs", "data.log"),
    format="{time} | {level} | {message}",
    level="INFO",
    rotation="1 MB",
    compression="zip",
)


def read_data(filename: str) -> pd.DataFrame:
    """
    Read data from Excel file and return a pandas DataFrame.

    Raises:
    FileNotFoundError: if the specified file is not found.
    """
    possible_paths = [
        BASE_PATH.joinpath(filename),
        BASE_PATH.joinpath("data", filename),
    ]

    for path in possible_paths:
        if path.exists():
            dataframe = pd.read_excel(path, parse_dates=["Datums"], index_col="Datums", date_format="%d.%m.%Y")
            logger.info(f"Read data from {path}")
            return dataframe

    raise FileNotFoundError(f"Could not find {filename}")


def create_bar_chart() -> plt.Figure:
    """Create a bar chart with average and maximum wind speed."""

    df_avg: pd.Series = read_data(WIND_SPEED_FILENAME).mean(axis=1)
    df_max: pd.Series = read_data(WIND_GUSTS_FILENAME).max(axis=1) - df_avg

    df_combined: pd.DataFrame = pd.concat(
        [df_avg, df_max],
        axis=1,
    )

    fig, ax = plt.subplots(figsize=(12, 8))

    df_combined.columns = ["Vidējais", "Maksimālais"]  # Rename columns

    df_combined.plot.bar(
        stacked=True,
        figsize=(12, 8),
        color=[ORANGE, BLUE],
        width=0.6,
        ax=ax,
    )

    # Format x-axis
    date_format = df_combined.index.strftime("%d.%m.%Y")
    ax.set_xticks(np.arange(len(date_format)))
    ax.set_xticklabels(date_format, rotation=45)
    ax.set_xlabel("Mērījumu Datums")

    # Format y-axis
    ax.set_yticks(np.arange(0, df_combined.max().max() + 2.5, 2.5))
    ax.set_ylabel("Vēja ātrums (m/s)")

    ax.set_title("Vidējais un maksimālais vēja ātrums 2023. gada augustā")

    logger.info("Created bar chart")

    return fig


SEASONS: dict[int, str] = {
    1: "Ziema",
    2: "Pavasaris",
    3: "Vasara",
    4: "Rudens",
}


def create_box_plot() -> plt.Figure:
    """Create a box plot showing the distribution of air temperature across seasons."""

    df: pd.DataFrame = read_data(AIR_TEMP_FILENAME)

    # Assign season to each row
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

    # Format x-axis
    ax.set_xlabel("")

    # Format y-axis
    min_value: float = np.floor(df["Average"].min() / 5) * 5
    max_value: float = np.ceil(df["Average"].max() / 5) * 5
    tick_step: int = 5
    ax.set_yticks(np.arange(min_value, max_value, tick_step))
    ax.set_ylabel("Gaisa temperatūra (Celsija grādos)")

    ax.set_title("Gaisa temperatūra Rīgā četros gadalaikos")

    logger.info("Created box plot")

    return fig


def open_pdf(filename: str) -> None:
    """
    Open a PDF file using the default system viewer.

    Raises:
    FileNotFoundError: if the specified file is not found.
    """

    pdf_path = BASE_PATH.joinpath(filename)
    if not pdf_path.exists():
        raise FileNotFoundError(f"Could not find {pdf_path}")

    logger.info(f"Opening {filename}")

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
    """Main function to generate and save plots to a PDF file, then open the PDF."""

    # Generate and save plots to a PDF file
    with PdfPages(PDF_FILENAME) as pdf:
        fig1 = create_bar_chart()
        pdf.savefig(fig1)
        plt.close(fig1)

        fig2 = create_box_plot()
        pdf.savefig(fig2)
        plt.close(fig2)

    try:
        open_pdf(PDF_FILENAME)
    except Exception as e:
        logger.error(e)
        logger.warning("Something went wrong while opening the PDF. Please open it manually.")


if __name__ == "__main__":
    main()
