from sqlalchemy import create_engine
from time import time
import pandas as pd
import numpy as np
import argparse
import requests
import os


def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-01.parquet"

    # Reading data

    parquet_name = 'yellow_tripdata_2021-01.parquet'

    response = requests.get(url, verify=False)  # Disable SSL verification
    with open(parquet_name, 'wb') as f:
        f.write(response.content)

    # Check if the file is not empty
    if os.path.getsize(parquet_name) > 0:
        print("File downloaded successfully.")
    else:
        print("Download failed or file is empty.")

    df = pd.read_parquet(parquet_name, engine='pyarrow')

    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    print(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    # Create connection to postgres
    engine = create_engine(
        f'postgresql://{user}:{password}@{host}:{port}/{db}')

    # Inserting data
    df_splits = np.array_split(df, 10)
    for df_split in df_splits:
        t_start = time()
        df_split.to_sql(name=table_name, con=engine,
                        if_exists='append', index=False)
        t_end = time()

        print(f'inserted another chunk, took {t_end - t_start} seconds')


if __name__ == '__main__':

    # user, password, host, port, database name, table name, url of the parquet
    parser = argparse.ArgumentParser(
        description='Ingest parquet data to postgrese')
    parser.add_argument('--user', help='user name for postgres')
    parser.add_argument('--password', help='password for postgres')
    parser.add_argument('--host', help='host for postgres')
    parser.add_argument('--port', help='port for postgres')
    parser.add_argument('--db', help='database name for postgres')
    parser.add_argument(
        '--table_name', help='table name where the data will be ingested')

    args = parser.parse_args()


main(args)
