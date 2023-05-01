import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# 認証情報を設定する
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

# JSON ファイルへのパスを取得する
dir_path = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(dir_path, '..', 'client_secret_720300467731-3jeisrjue0np4tm8oa69ajvnjm3hnrl1.apps.googleusercontent.com.json')

# 認証情報を取得する
credentials = ServiceAccountCredentials.from_json_keyfile_name(json_path, scope)
client = gspread.authorize(credentials)

# スプレッドシートを取得する
sheet = client.open('スプレッドシート名').worksheet('5月')

# 目次を設定する
sheet.update_cell(1, 1, '日付')
sheet.update_cell(1, 2, 'チェック項目１')
sheet.update_cell(1, 3, 'チェック項目２')
sheet.update_cell(1, 4, 'チェック項目３')

# 日付を生成する
date = datetime.datetime(2023, 5, 1)

# スプレッドシートに日付を書き込む
for i in range(31):
    sheet.update_cell(i+2, 1, date.strftime('%-m/%-d'))
    date += datetime.timedelta(days=1)
