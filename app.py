from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
import os
from dotenv import load_dotenv
from sheets_manager import SheetsManager

# 環境変数を読み込み
load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-here')

# Google Sheets Manager初期化
try:
    sheets_manager = SheetsManager()
    print("✅ Google Sheets Manager の初期化に成功しました")
except Exception as e:
    print(f"❌ Google Sheets Manager の初期化に失敗しました: {str(e)}")
    sheets_manager = None


@app.route('/')
def index():
    """TODOリスト一覧を表示"""
    if sheets_manager is None:
        flash('Google Sheets の接続に失敗しています。設定を確認してください。', 'error')
        return render_template('index.html', todos=[])
    
    try:
        todos = sheets_manager.get_all_todos()
        return render_template('index.html', todos=todos)
    except Exception as e:
        flash(f'エラーが発生しました: {str(e)}', 'error')
        return render_template('index.html', todos=[])


@app.route('/add', methods=['GET', 'POST'])
def add_todo():
    """新しいTODOを追加"""
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        due_date = request.form.get('due_date')
        
        if not title:
            flash('タイトルは必須です', 'error')
            return render_template('add.html')
        
        try:
            sheets_manager.add_todo(title, content, due_date)
            flash('TODOを追加しました', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'エラーが発生しました: {str(e)}', 'error')
            return render_template('add.html')
    
    return render_template('add.html')


@app.route('/edit/<int:todo_id>', methods=['GET', 'POST'])
def edit_todo(todo_id):
    """TODOを編集"""
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        due_date = request.form.get('due_date')
        
        if not title:
            flash('タイトルは必須です', 'error')
            return redirect(url_for('edit_todo', todo_id=todo_id))
        
        try:
            sheets_manager.update_todo(todo_id, title, content, due_date)
            flash('TODOを更新しました', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'エラーが発生しました: {str(e)}', 'error')
            return redirect(url_for('edit_todo', todo_id=todo_id))
    
    try:
        todo = sheets_manager.get_todo_by_id(todo_id)
        if not todo:
            flash('TODOが見つかりません', 'error')
            return redirect(url_for('index'))
        return render_template('edit.html', todo=todo)
    except Exception as e:
        flash(f'エラーが発生しました: {str(e)}', 'error')
        return redirect(url_for('index'))


@app.route('/delete/<int:todo_id>')
def delete_todo(todo_id):
    """TODOを削除"""
    try:
        sheets_manager.delete_todo(todo_id)
        flash('TODOを削除しました', 'success')
    except Exception as e:
        flash(f'エラーが発生しました: {str(e)}', 'error')
    return redirect(url_for('index'))


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

