import io
import os
import requests
import pandas as pd
from google.cloud import storage
import pyarrow as pa

from pyarrow.parquet import ParquetFile
import pyarrow.parquet as pq

"""
Pre-reqs: 
1. `pip install pandas pyarrow google-cloud-storage`
2. Set GOOGLE_APPLICATION_CREDENTIALS to your project/service-account key
3. Set GCP_GCS_BUCKET as your bucket or change default value of BUCKET
"""

# services = ['fhv','green','yellow']
#init_url = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/'
init_url = 'https://d37ci6vzurychx.cloudfront.net/trip-data'

# switch out the bucketname
BUCKET = os.environ.get("GCP_GCS_BUCKET", "lucapug-taxi-data-us")


table_schema_fhv = pa.schema(
    [
        ('dispatching_base_num',pa.string()),
        ('pickup_datetime',pa.timestamp('s')),
        ('dropOff_datetime',pa.timestamp('s')),
        ('PUlocationID',pa.int64()),
        ('DOlocationID',pa.int64()),
        ('SR_Flag',pa.int64()),
    ]
)


def upload_to_gcs(bucket, object_name, local_file):
    """
    Ref: https://cloud.google.com/storage/docs/uploading-objects#storage-upload-object-python
    """
    # # WORKAROUND to prevent timeout for files > 6 MB on 800 kbps upload speed.
    # # (Ref: https://github.com/googleapis/python-storage/issues/74)
    # storage.blob._MAX_MULTIPART_SIZE = 5 * 1024 * 1024  # 5 MB
    # storage.blob._DEFAULT_CHUNKSIZE = 5 * 1024 * 1024  # 5 MB

    client = storage.Client()
    bucket = client.bucket(bucket)
    blob = bucket.blob(object_name)
    blob.upload_from_filename(local_file)


def web_to_gcs(year, service):
    for i in range(12):
        
        # sets the month part of the file_name string
        month = '0'+str(i+1)
        month = month[-2:]
        
        # parquet file name
        file_name = f"{service}_tripdata_{year}-{month}.parquet"

        # dowload parquet file from TLC website
        request_url = f"{init_url}/{file_name}"
        r = requests.get(request_url, allow_redirects=True)
        open(file_name, 'wb').write(r.content)
        print(f"Local: {file_name}")
        
        # # Impose schema to parquet via pandas read_parquet
        # #df = pd.read_parquet(file_name, engine = 'pyarrow', schema=table_schema_fhv)        
        # df = pd.read_parquet(file_name, engine = 'pyarrow')        
        # df.to_parquet(file_name, engine='pyarrow', schema = table_schema_fhv)
        # #df.to_parquet(file_name, engine='pyarrow')        
        # print(f"Local with schema imposed: {file_name}") 

        # Read metadata 
        #print(pq.read_metadata(file_name))
        
        # Read file, read the table from file and check schema
        file = pq.ParquetFile(file_name)
        table = file.read()
        #print(table.schema )       

        # Convert to pandas and check data 
        df = table.to_pandas()
        #print(df.info())

        # Impose schema to parquet
        df.to_parquet(file_name, engine='pyarrow', schema = table_schema_fhv)    
        print(f"Local with schema imposed: {file_name}") 
                               
        # upload it to gcs 
        upload_to_gcs(BUCKET, f"{service}/{file_name}", file_name)
        print(f"GCS uploaded: {service}/{file_name}")

web_to_gcs('2019', 'fhv')