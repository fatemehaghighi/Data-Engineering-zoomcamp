
import pandas as pd
from sqlalchemy import create_engine
import click
import requests
import pyarrow.parquet as pq
from io import BytesIO



dtype_taxi_zone = {
    'LocationID': 'int64',
    'Borough': 'string',
    'Zone': 'string',
    'service_zone': 'string'
}


@click.command()
@click.option('--pg-user', default='root', help='PostgreSQL user')
@click.option('--pg-pass', default='root', help='PostgreSQL password')
@click.option('--pg-host', default='localhost', help='PostgreSQL host')
@click.option('--pg-port', default=5432, type=int, help='PostgreSQL port')
@click.option('--pg-db', default='ny_taxi', help='PostgreSQL database name')
@click.option('--target-table', default='green_tripdata', help='Target table name')
@click.option('--year', default=2025, type=int, help='Year of the data')
@click.option('--month', default=11, type=int, help='Month of the data')
@click.option('--chunksize', default=100000, type=int, help='Chunk size for ingestion')


def run(pg_user, pg_pass, pg_host, pg_port, pg_db,target_table ,year, month, chunksize ):
    prefix_trip_data = 'https://d37ci6vzurychx.cloudfront.net/trip-data'
    url_trip_data=f'{prefix_trip_data}/green_tripdata_{year}-{month:02d}.parquet'
    url_taxi_zone='https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv'
    
    response = requests.get(url_trip_data)
    parquet_file = pq.ParquetFile(BytesIO(response.content))

    engine = create_engine(f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')
    first_green_tripdata = True
    first_taxi_zone = True
    
    for batch in parquet_file.iter_batches(batch_size=chunksize):
        if first_green_tripdata:
            df_chunk = batch.to_pandas()
            df_chunk.head(0).to_sql(name=target_table,con=engine,if_exists='replace')
            first_green_tripdata = False
        df_chunk.to_sql(name=target_table,con=engine,if_exists="append")
        
    df_taxi_zone=pd.read_csv(url_taxi_zone,dtype=dtype_taxi_zone)
    if first_taxi_zone:
        df_taxi_zone.head(0).to_sql(name='taxi_zone',con=engine,if_exists='replace')
        first_taxi_zone=False
    
    df_taxi_zone.to_sql(name='taxi_zone',con=engine,if_exists="append")
    

if __name__== '__main__':
    run()