import sqlite3
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def get_first_timestamp(db_name, table_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # 最初のタイムスタンプを取得
    cursor.execute(f"SELECT MIN(timestamp) FROM {table_name}")
    first_timestamp = cursor.fetchone()[0]
    
    conn.close()
    return first_timestamp

def get_eeg_data(db_name, table_name, start_time, end_time):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # 特定の時間範囲のアルファ波とベータ波データを取得
    cursor.execute(f"SELECT alpha, beta FROM {table_name} WHERE timestamp BETWEEN '{start_time}' AND '{end_time}'")
    rows = cursor.fetchall()
    
    # データをそれぞれ1次元のリストに変換
    alpha_wave_data = [row[0] for row in rows]
    beta_wave_data = [row[1] for row in rows]
    
    conn.close()
    return np.array(alpha_wave_data), np.array(beta_wave_data)

def main():
    # データベースから最初のタイムスタンプを取得
    db_name = 'brainwaves_11_21_meeting.db'  # 実際のデータベース名を指定
    table_name = 'brainwaves'  # 実際のテーブル名を指定
    first_timestamp = get_first_timestamp(db_name, table_name)
    
    # 開始時刻をdatetimeオブジェクトに変換
    start_time_dt = datetime.strptime(first_timestamp, '%Y-%m-%d %H:%M:%S')
    
    # 30秒後の終了時刻を計算
    end_time_dt = start_time_dt + timedelta(seconds=30)
    
    # 終了時刻を文字列に変換
    end_time = end_time_dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # 開始時刻を文字列として保持
    start_time = start_time_dt.strftime('%Y-%m-%d %H:%M:%S')
    
    alpha_wave_data, beta_wave_data = get_eeg_data(db_name, table_name, start_time, end_time)
    
    # 生データをプロット
    plt.figure(figsize=(12, 8))
    
    # アルファ波のプロット
    plt.plot(alpha_wave_data, label='Alpha Wave', color='b')
    
    # ベータ波のプロット
    plt.plot(beta_wave_data, label='Beta Wave', color='r')
    
    plt.title('Alpha and Beta Waves (First 30 Seconds of Raw Data)')
    plt.xlabel('Sample')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()
