FROM python:3.11-slim
WORKDIR /app

# 依存を先に入れてキャッシュ活用
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリ本体
COPY . .

# ログを即時フラッシュ
ENV PYTHONUNBUFFERED=1

# Render が割り当てるPORTを使って起動
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:${PORT}", "--timeout", "120"]
