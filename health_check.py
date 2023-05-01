# URLを配列で定義し、それぞれのURLに対してリクエストを送り、レスポンスを受け取ることで、ヘルスチェックを行う。
# 結果はGmailで通知する。
import requests                      # URLにリクエストを送信してレスポンスを送信する。
import smtplib                       # メールを送信する。
import os                            # 環境変数を取得する。
from dotenv import load_dotenv       # .envファイルから環境変数を読み込む。
from email.mime.text import MIMEText # メールの内容を作成する。
from email.utils import formatdate   # メールの日付を作成する。

# .envファイルから環境変数を読み込む
load_dotenv()

# Gmailのアドレスとパスワードを環境変数から取得
address  = os.getenv('GMAIL_USER')
password = os.getenv('GMAIL_PASSWORD')

# メール送信用の関数
def send_mail(body):
    # メールの内容を作成
    msg = MIMEText(body)
    msg['Subject'] = 'ヘルスチェック結果'
    msg['From'] = address
    msg['To']   = address
    msg['Date'] = formatdate()

    # Gmailに接続
    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.ehlo()
    smtp.starttls()
    # Gmailにログイン
    smtp.login(address, password)
    # メールの送信
    smtp.send_message(msg)
    smtp.close()

# ヘルスチェック用の関数
def health_check(url):
    try:
        # URLにリクエストを送信
        response = requests.get(url)
        # レスポンスのステータスコードを取得
        status_code = response.status_code
        # ステータスコードが200の場合はOK、それ以外はNGと判定
        if status_code == 200:
            return 'OK'
        else:
            return 'ステータスコードが200ではありません。'
    except requests.exceptions.RequestException:
        # リクエスト自体が失敗した場合はNGと判定
        return 'リクエストが失敗しました。'

# メイン処理
if __name__ == '__main__':
    # ヘルスチェックを行うURLを配列で定義
    urls = [
        {'url': 'https://www.pachinkovista.com/pfactory/model_top.php', 'name': 'パチンコビスタ'},
        {'url': 'https://www.operal.jp/login/index/', 'name': '券売機'},
        {'url': 'https://www.fscorp.jp/', 'name': 'エフエス'},
        {'url': 'https://www.j-net-gs.com/gsession/common/cmn001.do', 'name': 'グループセッション'},
        {'url': 'https://www.kenbaiki-pro.jp/', 'name': '券売機プロ'},
    ]

    # ヘルスチェックの結果を格納する配列を定義
    health_check_results = []

    # ヘルスチェックを行うURLの数だけループ
    for url in urls:
        # ヘルスチェックを行う
        health_check_result = health_check(url['url'])
        # ヘルスチェックの結果を配列に格納
        health_check_results.append(f"{url['name']}：{health_check_result}")

    # ヘルスチェックの結果を表示
    print('\n'.join(health_check_results))

    # ヘルスチェックの結果をメールで送信
    send_mail('\n'.join(health_check_results))
