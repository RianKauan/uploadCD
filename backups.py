import os
import csv
import datetime
from google.cloud import storage


storage_client = storage.Client()


def write_log(log_data):
    file_exists = os.path.isfile(os.getenv("LOG_FILE"))
    with open(os.getenv("LOG_FILE"), mode="a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["date_time","file_path", "status"])
        writer.writerow(log_data)


def upload_to_bucket(blob_name, file_path):
    try:
        bucket = storage_client.get_bucket(os.getenv("BUCKET_NAME"))
        blob = bucket.blob(blob_name)
        blob.upload_from_filename(file_path)
        print(f"Arquivo {blob_name} enviado com sucesso!")
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        write_log([timestamp,blob_name,"Sucesso", ""])
        return True
    
    except Exception as e:
        timestamp = datetime.datetime.now().strftime("Y-%m-%d %H:%M:%S")
        write_log([timestamp, blob_name, "Erro", str(e)])
        print(f"Erro ao enviar {blob_name}: {e}")
        return False


def upload_multiple_files():
    with os.scandir(os.getenv("PATH_BACKUPS")) as entries:
        files = [entry.name for entry in entries if entry.is_file()]

    for file in files:
        file_path = os.path.join(os.getenv("PATH_BACKUPS"), file)
        if os.path.isfile(file_path):
            blob_name = f"arquivos/{file}"
            upload_to_bucket(blob_name,file_path)

upload_multiple_files()
