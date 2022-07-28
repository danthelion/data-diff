import pandas as pd


def csv_to_parquet(csv_file, parquet_file):
    df = pd.read_csv(csv_file)
    df.to_parquet(parquet_file)


if __name__ == "__main__":
    csv_to_parquet("ratings.csv", "ratings.parquet")
