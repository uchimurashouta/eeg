import sqlite3
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def get_all_energy_data(db_name, table_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # 全てのアルファ波とベータ波のエネルギーデータを取得
    cursor.execute(f"SELECT alpha, beta FROM {table_name}")
    rows = cursor.fetchall()
    
    # データをそれぞれ1次元のリストに変換
    alpha_energy_data = [row[0] for row in rows]
    beta_energy_data = [row[1] for row in rows]
    
    conn.close()
    return np.array(alpha_energy_data), np.array(beta_energy_data)

def main():
    # データベースから全てのアルファ波とベータ波のエネルギーデータを取得
    db_name = 'brainwaves_11_21_meeting.db'  # 実際のデータベース名を指定
    table_name = 'brainwaves'  # 実際のテーブル名を指定
    alpha_energy_data, beta_energy_data = get_all_energy_data(db_name, table_name)
    
    # アルファ波の平均値を計算
    mean_alpha_energy = np.mean(alpha_energy_data)
    
    # エネルギーデータをプロット
    plt.figure(figsize=(12, 8))
    
    # アルファ波のプロット
    plt.plot(alpha_energy_data, label='Alpha Energy', color='b')
    plt.axhline(y=mean_alpha_energy, color='c', linestyle='--', label='Mean Alpha Energy')
    
    # ベータ波のプロット
    plt.plot(beta_energy_data, label='Beta Energy', color='r')
    
    plt.title('Alpha and Beta Energy (Raw Data)')
    plt.xlabel('Sample')
    plt.ylabel('Energy')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()
