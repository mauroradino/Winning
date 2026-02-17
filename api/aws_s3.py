import boto3
import pandas as pd
from dotenv import load_dotenv
import os
import io
import unicodedata
load_dotenv()

aws_ak = os.getenv("AWS_ACCESS_KEY_ID") 
aws_secret = os.getenv("AWS_SECRET_ACCESS_KEY") 
bucket_name = os.getenv("BUCKET_NAME")
region = os.getenv("AWS_REGION")

def normalize(text):
    if pd.isna(text) or text is None:
        return ""
    text_str = str(text)
    text_nfkd = unicodedata.normalize("NFD", text_str)
    without_accents = "".join(c for c in text_nfkd if unicodedata.category(c) != "Mn")
    return without_accents.lower().strip()

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

def execute_s3_transfer(player_name, season, from_club, to_club, transfer_amount):
    path_origin_squad = f"datasets/{from_club}/{season}/{from_club}_{season}_players.csv"
    path_dest_squad = f"datasets/{to_club}/{season}/{to_club}_{season}_players.csv"
    path_origin_transfers = f"datasets/{from_club}/{season}/{from_club}_{season}_bajas.csv"
    path_dest_transfers = f"datasets/{to_club}/{season}/{to_club}_{season}_altas.csv"
    path_origin_vals = f"datasets/{from_club}/{season}/{from_club}_{season}_valuations.csv"
    path_dest_vals = f"datasets/{to_club}/{season}/{to_club}_{season}_valuations.csv"

    df_origin = read_aws_csv(path_origin_squad)
    df_dest = read_aws_csv(path_dest_squad)
    df_trans_origin = read_aws_csv(path_origin_transfers)
    df_trans_dest = read_aws_csv(path_dest_transfers)
    df_vals_origin = read_aws_csv(path_origin_vals)
    df_vals_dest = read_aws_csv(path_dest_vals)

    if df_origin is None or df_dest is None:
        return "❌ Error: No se encontraron los planteles base en S3."

    nombre_buscado = normalize(player_name.lower())
    col_name_squad = next((c for c in df_origin.columns if c.lower().strip() in ['nombre y apellido', 'player_name', 'nombre']), None)
    
    if not col_name_squad:
        return "❌ Error: No se encontró columna de nombre en el plantel."

    mask_squad = df_origin[col_name_squad].str.lower().apply(normalize) == nombre_buscado
    player_row = df_origin[mask_squad]
    
    if player_row.empty:
        return f"⚠️ Jugador '{player_name}' no encontrado en {from_club}."

    p_id = player_row.iloc[0].get('player_id') or player_row.iloc[0].get('id')
    
    df_vals_origin_upd = df_vals_origin
    df_vals_dest_upd = df_vals_dest

    if df_vals_origin is not None and p_id is not None:
        mask_vals = df_vals_origin['player_id'].astype(str).str.replace('.0', '', regex=False) == str(p_id).replace('.0', '')
        player_vals_rows = df_vals_origin[mask_vals].copy()
        
        if not player_vals_rows.empty:
            df_vals_origin_upd = df_vals_origin[~mask_vals]
            player_vals_rows['club'] = to_club.strip().title()
            
            if df_vals_dest is not None:
                df_vals_dest_upd = pd.concat([df_vals_dest, player_vals_rows], ignore_index=True)
            else:
                df_vals_dest_upd = player_vals_rows

    df_origin_updated = df_origin[~mask_squad]
    player_row_updated = player_row.copy()
    player_row_updated['club'] = to_club.strip().title()
    df_dest_updated = pd.concat([df_dest, player_row_updated], ignore_index=True)

    new_transfer = pd.DataFrame([{
        "player_id": p_id,
        "player_name": player_name.strip().title(),
        "from_club": from_club.strip().title(),
        "to_club": to_club.strip().title(),
        "amount": transfer_amount,
        "transfer_date": pd.Timestamp.now().strftime('%Y-%m-%d')
    }])

    df_bajas_upd = pd.concat([df_trans_origin, new_transfer], ignore_index=True) if df_trans_origin is not None else new_transfer
    df_altas_upd = pd.concat([df_trans_dest, new_transfer], ignore_index=True) if df_trans_dest is not None else new_transfer

    try:
        upload_file(df_origin_updated, path_origin_squad)
        upload_file(df_dest_updated, path_dest_squad)
        upload_file(df_bajas_upd, path_origin_transfers)
        upload_file(df_altas_upd, path_dest_transfers)
        
        if df_vals_origin_upd is not None:
            upload_file(df_vals_origin_upd, path_origin_vals)
        if df_vals_dest_upd is not None:
            upload_file(df_vals_dest_upd, path_dest_vals)
            
        return f"✅ EXITOSO: {player_name} transferido a {to_club}."
    except Exception as e:
        return f"❌ Error en persistencia: {e}"