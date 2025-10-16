#!/bin/bash

echo "======================================"
echo "TODO リストアプリ - セットアップスクリプト"
echo "======================================"
echo ""

# Python バージョン確認
echo "Python バージョンを確認中..."
python3 --version

# 仮想環境の作成
echo ""
echo "仮想環境を作成中..."
python3 -m venv venv

# 仮想環境の有効化
echo "仮想環境を有効化中..."
source venv/bin/activate

# パッケージのインストール
echo ""
echo "必要なパッケージをインストール中..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "======================================"
echo "セットアップ完了！"
echo "======================================"
echo ""
echo "次のステップ:"
echo "1. Google Cloud Console でサービスアカウントを作成"
echo "2. credentials.json をプロジェクトルートに配置"
echo "3. Google スプレッドシートを作成してサービスアカウントと共有"
echo "4. アプリケーションを起動: python app.py"
echo ""
echo "詳細は README.md を参照してください。"
echo ""

