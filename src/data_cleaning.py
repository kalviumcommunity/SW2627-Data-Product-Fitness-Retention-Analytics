import pandas as pd


def clean_data(data):
    if isinstance(data, pd.DataFrame):
        df = data.copy()
    else:
        df = pd.read_csv(data)

    df["date"] = pd.to_datetime(df["date"])
    df = df.drop_duplicates()

    df["duration"].fillna(0, inplace=True)
    df["calories"].fillna(0, inplace=True)

    return df