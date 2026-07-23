import pandas as pd

def clean_data(file_path):
    df = pd.read_csv(file_path)

    # Convert date
    df["date"] = pd.to_datetime(df["date"])

    # Remove duplicates
    df = df.drop_duplicates()

    # Fill missing values
    df["duration"].fillna(0, inplace=True)
    df["calories"].fillna(0, inplace=True)

    return df