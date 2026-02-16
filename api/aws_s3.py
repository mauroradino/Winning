import boto3
import pandas as pd
from dotenv import load_dotenv
import os
import io

load_dotenv()

aws_ak = os.getenv("AWS_ACCESS_KEY_ID") 
aws_secret = os.getenv("AWS_SECRET_ACCESS_KEY") 
bucket_name = os.getenv("BUCKET_NAME")
region = os.getenv("AWS_REGION")

if not aws_ak or not aws_secret:
    print("Faltan las variables de entorno de AWS")

s3 = boto3.client(
    's3',
    aws_access_key_id=aws_ak,
    aws_secret_access_key=aws_secret,
    region_name=region 
)

def read_aws_csv(path):
    try:
        obj = s3.get_object(Bucket=bucket_name, Key=path.lower())
        df = pd.read_csv(io.BytesIO(obj['Body'].read()))
        return df.where(pd.notnull(df), None)
    except Exception as e:
        print(f"Error al leer {path}: {e}")
        return None
    

def upload_file(df, s3_path):
    csv_buffer = io.StringIO()
    df_clean = df.where(pd.notnull(df), None)
    df_clean.to_csv(csv_buffer, index=False, encoding="utf-8-sig")
    
    try:
        s3.put_object(
            Bucket=bucket_name, 
            Key=s3_path, 
            Body=csv_buffer.getvalue()
        )
        print(f"✅ Subido exitosamente a S3: {s3_path}")
    except Exception as e:
        print(f"❌ Error al subir a S3: {e}")