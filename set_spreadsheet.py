#!/usr/bin/env python3
"""スプレッドシートIDを設定するスクリプト"""

import sys
import os

print("=" * 50)
print("スプレッドシート ID 設定")
print("=" * 50)
print()
print("スプレッドシートのURLから、IDをコピーしてください：")
print("https://docs.google.com/spreadsheets/d/【ここがID】/edit")
print()

if len(sys.argv) > 1:
    spreadsheet_id = sys.argv[1]
else:
    spreadsheet_id = input("スプレッドシート ID を入力: ").strip()

if not spreadsheet_id:
    print("❌ IDが入力されていません")
    sys.exit(1)

# .env ファイルに書き込む
env_content = f"""# Flask設定
SECRET_KEY=your-secret-key-here

# Google認証情報ファイルのパス
GOOGLE_CREDENTIALS_FILE=credentials.json

# スプレッドシートID
SPREADSHEET_ID={spreadsheet_id}

# サーバーポート（デフォルト: 5000）
PORT=5000
"""

with open('.env', 'w', encoding='utf-8') as f:
    f.write(env_content)

print()
print("✅ 設定が完了しました！")
print(f"📊 スプレッドシート ID: {spreadsheet_id}")
print()
print("次のステップ:")
print("1. アプリを再起動してください")
print("   pkill -f 'python app.py' && ./start.sh")
print()

