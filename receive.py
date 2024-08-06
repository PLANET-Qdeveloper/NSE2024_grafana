import serial
import time
import csv
import os

# シリアルポートの設定
ser = serial.Serial('COM11', 115200)  # COMポートは受信機とつながってるやつの番号をThonnyなりデバイスマネージャーなりで確認してね

# 保存先のCSVファイルを指定
data_csv_file_path = 'C:\\Users\\jun15\\Documents\\Planet-Q\\電装\\地上局\\NSE2024_grafana\\datar2.csv'  # 適宜変更
tempdata_csv_file_path = 'C:\\Users\\jun15\\Documents\\Planet-Q\\電装\\地上局\\NSE2024_grafana\\tempdata.csv'  # 適宜変更

while True:
    try:
        if ser.in_waiting:
            # シリアルポートからデータを読み取る
            data = ser.readline().strip().decode('utf-8')

            # timestampをISO 8601形式で取得
            timestamp = time.strftime("%Y-%m-%dT%H:%M:%S+09:00")

            # データ内のカンマを避けるために、データをリストに変換
            split_data = data.split(',')
            split_data.insert(0, timestamp)

            # data.csvファイルにデータを追加
            with open(data_csv_file_path, mode='a', newline='') as file:
                writer = csv.writer(file, quoting=csv.QUOTE_MINIMAL)
                writer.writerow(split_data)

            # tempdata.csvの2行目以降を削除
            if os.path.exists(tempdata_csv_file_path):
                with open(tempdata_csv_file_path, 'r', newline='') as file:
                    reader = list(csv.reader(file))
                if len(reader) > 1:
                    reader = [reader[0]]  # ヘッダー行を残す
                with open(tempdata_csv_file_path, 'w', newline='') as file:
                    writer = csv.writer(file, quoting=csv.QUOTE_MINIMAL)
                    writer.writerows(reader)
            
            # tempdata.csvファイルにデータを追加
            with open(tempdata_csv_file_path, mode='a', newline='') as file:
                writer = csv.writer(file, quoting=csv.QUOTE_MINIMAL)
                writer.writerow(split_data)
            
            print(f"データを追加しました: {timestamp}, {data}")

    except KeyboardInterrupt:
        print("処理を中断しました。")
        break
    except Exception as e:
        print(f"エラーが発生しました: {e}")
