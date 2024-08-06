from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import os
import time
import csv

# InfluxDBの接続情報
url = "http://localhost:8086"
token = "CrjF9bKU1WvlY3ror9Tf16h-Eb6Y6jw6cNpTJmOxIJCEXdfdMqByD6cV3i9H2jHAsCOYpBlYt4Vttu9IjAUb9A=="
org = "PLANET-Q"
bucket = "NSE2024"

# CSVをInfluxDBに書き込む関数
def import_csv_to_influxdb(csv_file):
    try:
        with open(csv_file, mode='r') as file:
            reader = csv.reader(file)
            header = next(reader)  # 最初の行をヘッダーとして読み込む

            client = InfluxDBClient(url=url, token=token, org=org)
            write_api = client.write_api(write_options=SYNCHRONOUS)

            for row in reader:
                timestamp = row[0]
                phase = int(row[1])
                missiontime = int(row[2])
                flighttime = float(row[3])
                lat = float(row[4])
                lon = float(row[5])
                alt = float(row[6])
                pressure = float(row[7])
                temperature = float(row[8])
                voltage = float(row[9])

                point = Point("measurement_name") \
                    .time(timestamp) \
                    .field("phase", phase) \
                    .field("missiontime", missiontime) \
                    .field("flighttime", flighttime) \
                    .field("lat", lat) \
                    .field("lon", lon) \
                    .field("alt", alt) \
                    .field("pressure", pressure) \
                    .field("temperature", temperature) \
                    .field("voltage", voltage)

                write_api.write(bucket=bucket, org=org, record=point)

            write_api.close()
            print(f"Successfully imported data from {csv_file}")

    except Exception as e:
        print(f"Failed to import data from {csv_file}: {e}")

# CSVファイルが置かれているディレクトリ
csv_directory = 'C:\\Users\\jun15\\Documents\\Planet-Q\\電装\\地上局\\rig'

# インポートする特定のCSVファイルのリスト
csv_files_to_import = [
    'sendata.csv'
    # 他のファイル名を必要に応じて追加
]

# ファイルの最終更新時刻を保持する辞書
file_mod_times = {filename: None for filename in csv_files_to_import}

# ファイルの変更を監視してインポートする
while True:
    for filename in csv_files_to_import:
        csv_file_path = os.path.join(csv_directory, filename)
        if os.path.exists(csv_file_path):
            # ファイルの最終更新時刻を取得
            mod_time = os.path.getmtime(csv_file_path)
            # ファイルの更新時刻が前回の更新時刻と異なる場合
            if file_mod_times[filename] is None or file_mod_times[filename] != mod_time:
                file_mod_times[filename] = mod_time
                import_csv_to_influxdb(csv_file_path)  # 新しいデータをインポートする
        else:
            print(f"File {filename} does not exist.")

    time.sleep(0.5)
