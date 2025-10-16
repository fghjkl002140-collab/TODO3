# TODO リストアプリ

Google スプレッドシートをデータベースとして使用した、シンプルで使いやすい TODO リストアプリケーションです。

## 機能

- ✅ TODOの登録（タイトル、内容、期日）
- ✏️ TODOの編集
- 🗑️ TODOの削除
- 📋 TODOリストの一覧表示
- 📊 Google スプレッドシートでのデータ管理

## 必要なもの

- Python 3.8以上
- Google Cloud Platform アカウント
- Google スプレッドシート

## セットアップ手順

### 1. Google Cloud Platform の設定

1. [Google Cloud Console](https://console.cloud.google.com/) にアクセス
2. 新しいプロジェクトを作成
3. Google Sheets API と Google Drive API を有効化
4. サービスアカウントを作成
5. サービスアカウントのキー（JSON）をダウンロード
6. ダウンロードしたJSONファイルを `credentials.json` としてプロジェクトルートに配置

### 2. Google スプレッドシートの準備

1. Google スプレッドシートで新しいシートを作成
2. シート名を「TODO リスト」にする（または環境変数で指定）
3. サービスアカウントのメールアドレスとシートを共有（編集権限）
   - サービスアカウントのメールアドレスは `credentials.json` の `client_email` フィールドで確認できます

### 3. パッケージのインストール

```bash
pip install -r requirements.txt
```

### 4. 環境変数の設定（オプション）

`.env` ファイルを作成して以下を設定できます：

```bash
# 必須ではないが推奨
SECRET_KEY=your-secret-key-here

# Google認証情報ファイルのパス（デフォルト: credentials.json）
GOOGLE_CREDENTIALS_FILE=credentials.json

# スプレッドシートID（推奨）またはスプレッドシート名
SPREADSHEET_ID=your-spreadsheet-id
# または
SPREADSHEET_NAME=TODO リスト

# サーバーポート（デフォルト: 5000）
PORT=5000
```

**スプレッドシートIDの確認方法:**
Google スプレッドシートのURLから確認できます：
```
https://docs.google.com/spreadsheets/d/【ここがスプレッドシートID】/edit
```

### 5. アプリケーションの起動

```bash
python app.py
```

ブラウザで `http://localhost:5000` にアクセスしてください。

## 本番環境へのデプロイ

### Heroku へのデプロイ

1. Heroku CLI をインストール
2. Heroku アプリを作成

```bash
heroku create your-app-name
```

3. 環境変数を設定

```bash
heroku config:set SECRET_KEY=your-secret-key
heroku config:set SPREADSHEET_ID=your-spreadsheet-id
```

4. `credentials.json` の内容を環境変数として設定

```bash
heroku config:set GOOGLE_CREDENTIALS="$(cat credentials.json)"
```

その後、`sheets_manager.py` で環境変数から読み込むように修正が必要です。

5. `Procfile` を作成

```
web: python app.py
```

6. デプロイ

```bash
git add .
git commit -m "Initial commit"
git push heroku main
```

### その他のクラウドサービス

- **Google Cloud Run**: Dockerコンテナとしてデプロイ可能
- **AWS EC2**: 仮想サーバーで直接実行
- **Render**: 簡単にデプロイ可能

## ディレクトリ構造

```
TODOリスト/
├── app.py                  # メインアプリケーション
├── sheets_manager.py       # Google Sheets連携
├── requirements.txt        # 依存パッケージ
├── credentials.json        # Google認証情報（要作成）
├── .env                    # 環境変数（オプション）
├── templates/              # HTMLテンプレート
│   ├── base.html
│   ├── index.html
│   ├── add.html
│   └── edit.html
└── static/                 # 静的ファイル
    └── css/
        └── style.css
```

## トラブルシューティング

### Google Sheets API のエラー

- `credentials.json` が正しい場所にあるか確認
- サービスアカウントとスプレッドシートが共有されているか確認
- Google Sheets API と Google Drive API が有効になっているか確認

### スプレッドシートが見つからない

- `SPREADSHEET_ID` または `SPREADSHEET_NAME` が正しく設定されているか確認
- スプレッドシートがサービスアカウントと共有されているか確認

### ポートエラー

- 他のアプリケーションが同じポートを使用していないか確認
- 環境変数 `PORT` で別のポートを指定

## ライセンス

MIT License

## 作成者

TODO リストアプリ開発チーム

