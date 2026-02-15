import boto3
import pandas as pd
from dotenv import load_dotenv
import os
import io

load_dotenv()

# Cambia estos nombres para que coincidan EXACTAMENTE con lo que pusiste en Vercel
aws_ak = os.getenv("AWS_ACCESS_KEY_ID") # Agregado _ID
aws_secret = os.getenv("AWS_SECRET_ACCESS_KEY") # Nombre estándar
bucket_name = os.getenv("BUCKET_NAME")

if not aws_ak or not aws_secret:
    print("Faltan las variables de entorno de AWS")

# Es mejor inicializar el cliente dentro de una función o asegurar que tenga los datos
s3 = boto3.client(
    's3',
    aws_access_key_id=aws_ak,
    aws_secret_access_key=aws_secret,
    region_name='us-east-2' # Cambia a la región que se ve en tu captura (Ohio)
)

def read_aws_csv(path):
    try:
        # Usamos la variable local bucket_name
        obj = s3.get_object(Bucket=bucket_name, Key=path)
        df = pd.read_csv(io.BytesIO(obj['Body'].read()))
        # Limpieza de NaNs para evitar el error de JSON que tenías en FastAPI
        return df.where(pd.notnull(df), None)
    except Exception as e:
        print(f"Error al leer {path}: {e}")
        return None
    

def upload_file(df, s3_path):
    csv_buffer = io.StringIO()
    # Limpieza antes de subir para que el CSV sea consistente
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