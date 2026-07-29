import pandas as pd


def clean_data(file):
    """Clean workout data.

    Accepts either a file path / file-like object (CSV) or an already-loaded
    DataFrame. Returns a cleaned DataFrame.
    """
    if isinstance(file, pd.DataFrame):
        df = file.copy()
    else:
        df = pd.read_csv(file)

    df["date"] = pd.to_datetime(df["date"])
    df = df.drop_duplicates()

    df["duration"] = df["duration"].fillna(0)
    df["calories"] = df["calories"].fillna(0)

    return df