import sqlite3
from datetime import datetime

class DBWriter:
    def __init__(self, db_path):
        self.db_path = db_path
        self._initialize_db()

    def _initialize_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS brainwaves (
            timestamp TEXT,
            alpha REAL,
            beta REAL,
            theta REAL
        )
        ''')
        conn.commit()
        conn.close()

    def save_data(self, alpha, beta, theta):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute('''
        INSERT INTO brainwaves (timestamp, alpha, beta, theta) 
        VALUES (?, ?, ?, ?)
        ''', (timestamp, alpha, beta, theta))
        conn.commit()
        conn.close()
