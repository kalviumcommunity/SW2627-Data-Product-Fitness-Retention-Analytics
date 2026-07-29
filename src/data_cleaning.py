import pandas as pd


feature/fix-imports-and-validation
def clean_data(file):
    """Clean workout data.

    Accepts either a file path / file-like object (CSV) or an already-loaded
    DataFrame. Returns a cleaned DataFrame.
    """
    if isinstance(file, pd.DataFrame):
        df = file.copy()
    else:
        df = pd.read_csv(file)
=======
def clean_data(data):
    if isinstance(data, pd.DataFrame):
        df = data.copy()
    else:
        df = pd.read_csv(data)
 main

    df["date"] = pd.to_datetime(df["date"])
    df = df.drop_duplicates()

    df["duration"] = df["duration"].fillna(0)
    df["calories"] = df["calories"].fillna(0)

    return df