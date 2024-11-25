from pythonosc import dispatcher
from pythonosc import osc_server
from db_writer import DBWriter  # DBWriterクラスをインポート

# グローバル変数で一時的にデータを保存
temporary_data = {'alpha': None, 'beta': None, 'theta': None}

# データベースへの保存関数を使用
def save_to_db(alpha, beta, theta):
    global db_writer
    db_writer.save_data(alpha, beta, theta)

def print_handler(address, *args):
    global temporary_data

    if address == "/muse/elements/alpha_absolute":
        temporary_data['alpha'] = args[0]
    elif address == "/muse/elements/beta_absolute":
        temporary_data['beta'] = args[0]
    elif address == "/muse/elements/theta_absolute":
        temporary_data['theta'] = args[0]

    # 三つのデータがすべて揃ったらデータベースに書き込む
    if all(value is not None for value in temporary_data.values()):
        save_to_db(
            alpha=temporary_data['alpha'],
            beta=temporary_data['beta'],
            theta=temporary_data['theta']
        )
        # 一時的データをリセット
        temporary_data = {'alpha': None, 'beta': None, 'theta': None}
        
    print(f"Received message from {address}: {args}")

if __name__ == "__main__":
    global db_writer
    ip = "0.0.0.0"  # 受信するIPアドレス（すべて）
    port = 5000     # 受信するポート番号（Mind Monitorで設定したポート番号）

    db_writer = DBWriter('brainwaves_11_21_meeting.db')  # クラスのインスタンス化

    disp = dispatcher.Dispatcher()
    disp.map("/muse/elements/alpha_absolute", print_handler)
    disp.map("/muse/elements/beta_absolute", print_handler)
    disp.map("/muse/elements/theta_absolute", print_handler)

    server = osc_server.ThreadingOSCUDPServer((ip, port), disp)
    print(f"Serving on {server.server_address}")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Data written to DB.")
