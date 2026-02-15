import boto3
import pandas as pd
from dotenv import load_dotenv
import os
import io

load_dotenv()

aws_ak = os.getenv("AWS_ACCESS_KEY")
aws_secret = os.getenv("AWS_SECRET_KEY")

if not aws_ak and not aws_secret:
    print("Faltan las variables de entorno")

s3 = boto3.client(
    's3',
    aws_access_key_id= aws_ak,
    aws_secret_access_key=aws_secret,
    region_name='us-east-1'
)


def read_aws_csv(path):
    obj = s3.get_object(Bucket=os.getenv("BUCKET_NAME"), Key=path)
    if obj:
        df = pd.read_csv(io.BytesIO(obj['Body'].read()))
        return df
    else:
        return f"Archivo {path} no existente"


def upload_file(df, s3_path):
    s3 = boto3.client(
        's3',
        aws_access_key_id=aws_ak,
        aws_secret_access_key=aws_secret,
        region_name='us-east-1'
    )
    
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False, encoding="utf-8-sig")
    
    try:
        s3.put_object(
            Bucket=os.getenv("BUCKET_NAME"), 
            Key=s3_path, 
            Body=csv_buffer.getvalue()
        )
        print(f"Subido exitosamente a S3: {s3_path}")
    except Exception as e:
        print(f"Error al subir a S3: {e}")