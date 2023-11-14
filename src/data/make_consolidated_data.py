import os
import polars as pl
from pathlib import Path

def combine_csvs(raw_data_path, output_file):
    # Create a list to hold dataframes
    dfs = []

    # Iterate over each file in the raw data directory
    for filename in os.listdir(raw_data_path):
        if filename.endswith('.csv'):
            filepath = os.path.join(raw_data_path, filename)
            df = pl.read_csv(filepath)
            dfs.append(df)

    # Concatenate all dataframes
    combined_df = pl.concat(dfs, how='vertical_relaxed')

    # Save the combined dataframe to a CSV
    combined_df.write_csv(output_file)

if __name__ == '__main__':
    raw_data_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                os.pardir,
                os.pardir,
                'data',
                'raw'
                )
            )
    output_file = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                os.pardir,
                os.pardir,
                'data',
                'interim',
                'consolidated_data.csv'
                )
            )
    combine_csvs(raw_data_path, output_file)