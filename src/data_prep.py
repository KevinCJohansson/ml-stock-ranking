import numpy as np
import pandas as pd

FEATURES = [
    "PE ratio",
    "PB ratio",
    "priceToSalesRatio",
    "ROE",
    "debtEquityRatio",
    "currentRatio",
    "Net Profit Margin",
    "Gross Margin",
    "Free Cash Flow margin",
    "Revenue Growth",
    "EPS Growth",
    "Dividend Yield",
    "interestCoverage",
    "Market Cap"
]

def load_year(year, data_dir="../Data"):
    """Läser in ett års fil och ger avkastningskolumnen ett gemensamt namn."""
    df = pd.read_csv(f"{data_dir}/{year}_Financial_Data.csv")
    df = df.rename(columns={
        "Unnamed: 0": "Ticker",
        f"{year + 1} PRICE VAR [%]": "next_year_return",
    }).copy()
    df["year"] = year
    return df

def prepare_year(df):
    """Rensar ett års data och skapar målvariabeln."""
    df = df.copy()

    # Ta bort bolag som saknar mer än hälften av alla värden
    df = df[df[FEATURES].isna().mean(axis=1) <= 0.5]

    # Ta bort orimliga avkastningar (under -100 % är omöjligt)
    df = df[df["next_year_return"] >= -100]

    # Målvariabel: 1 om avkastningen är över årets median
    median = df["next_year_return"].median()
    df["above_median"] = (df["next_year_return"] > median).astype(int)

    # P/E = 0 betyder förlust
    df["has_loss"] = (df["Net Income"] < 0).astype(int)
    df.loc[df["PE ratio"] == 0, "PE ratio"] = np.nan

    # Börsvärdet varierar enormt, så vi använder logaritmen
    df["Market Cap"] = np.log1p(df["Market Cap"].clip(lower=0))

    columns = ["Ticker", "year", "Sector"] + FEATURES + ["has_loss",
               "next_year_return", "above_median"]
    return df[columns]

def build_dataset(years, data_dir="../Data"):
    """Läser in och rensar flera år och slår ihop dem till ett dataset."""
    frames = [prepare_year(load_year(y, data_dir)) for y in years]
    return pd.concat(frames, ignore_index=True)