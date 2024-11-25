import sqlite3
import numpy as np
import matplotlib.pyplot as plt

def get_all_eeg_data(db_name, table_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # 全てのアルファ波とベータ波データを取得
    cursor.execute(f"SELECT alpha, beta FROM {table_name}")
    rows = cursor.fetchall()
    
    # データをそれぞれ1次元のリストに変換
    alpha_wave_data = [row[0] for row in rows]
    beta_wave_data = [row[1] for row in rows]
    
    conn.close()
    return np.array(alpha_wave_data), np.array(beta_wave_data)

def main():
    # データベースから全てのアルファ波とベータ波データを取得
    db_name = 'brainwaves_11_21_meeting.db'  # 実際のデータベース名を指定
    table_name = 'brainwaves'  # 実際のテーブル名を指定
    alpha_wave_data, beta_wave_data = get_all_eeg_data(db_name, table_name)
    
    # サンプル数とサンプリングレートの設定
    fs = 1  # サンプリング周波数
    samples_per_minute = fs * 60  # 1分ごとのサンプル数
    
    # データを1分ごとに分割
    num_minutes = len(alpha_wave_data) // samples_per_minute
    alpha_box_data = [alpha_wave_data[i*samples_per_minute:(i+1)*samples_per_minute] for i in range(num_minutes)]
    beta_box_data = [beta_wave_data[i*samples_per_minute:(i+1)*samples_per_minute] for i in range(num_minutes)]
    
    # 箱ひげ図をプロット
    plt.figure(figsize=(12, 8))

    # アルファ波の箱ひげ図
    plt.subplot(2, 1, 1)
    plt.boxplot(alpha_box_data)
    plt.title('Alpha Wave Box Plot (1 minute intervals)')
    plt.xlabel('Minute')
    plt.ylabel('Alpha Wave Amplitude')

    # ベータ波の箱ひげ図
    plt.subplot(2, 1, 2)
    plt.boxplot(beta_box_data)
    plt.title('Beta Wave Box Plot (1 minute intervals)')
    plt.xlabel('Minute')
    plt.ylabel('Beta Wave Amplitude')
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
