import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import os


class SheetsManager:
    """Google Sheetsを使ったTODO管理クラス"""
    
    def __init__(self):
        """Google Sheets APIの初期化"""
        # 認証情報の設定
        scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        
        # 認証情報を環境変数から取得（Render用）
        google_creds = os.environ.get('GOOGLE_CREDENTIALS')
        if google_creds:
            # 環境変数から直接認証情報を取得
            import json
            creds_info = json.loads(google_creds)
            creds = Credentials.from_service_account_info(creds_info, scopes=scopes)
        else:
            # ローカル用：認証情報ファイルから取得
            creds_file = os.environ.get('GOOGLE_CREDENTIALS_FILE', 'credentials.json')
            creds = Credentials.from_service_account_file(creds_file, scopes=scopes)
        
        try:
            self.client = gspread.authorize(creds)
            
            # スプレッドシートを開く（IDまたは名前で指定）
            spreadsheet_id = os.environ.get('SPREADSHEET_ID')
            if spreadsheet_id:
                print(f"🔍 スプレッドシート ID で開こうとしています: {spreadsheet_id}")
                self.sheet = self.client.open_by_key(spreadsheet_id).sheet1
                print(f"✅ スプレッドシートを開きました: {self.sheet.title}")
            else:
                # スプレッドシート名で開く
                spreadsheet_name = os.environ.get('SPREADSHEET_NAME', 'TODO リスト')
                print(f"🔍 スプレッドシート名で開こうとしています: {spreadsheet_name}")
                try:
                    self.sheet = self.client.open(spreadsheet_name).sheet1
                    print(f"✅ スプレッドシートを開きました: {self.sheet.title}")
                except gspread.SpreadsheetNotFound:
                    print(f"❌ スプレッドシート '{spreadsheet_name}' が見つかりません")
                    raise Exception(f"スプレッドシート '{spreadsheet_name}' が見つかりません。SPREADSHEET_ID を設定するか、スプレッドシートが存在することを確認してください。")
            
            # ヘッダー行の確認と作成
            self._initialize_sheet()
            
        except Exception as e:
            raise Exception(f'Google Sheets APIの初期化に失敗しました: {str(e)}')
    
    def _initialize_sheet(self):
        """シートのヘッダー行を初期化"""
        try:
            # 最初の行を取得
            first_row = self.sheet.row_values(1)
            
            # ヘッダーが存在しない場合は作成
            if not first_row or first_row[0] != 'ID':
                headers = ['ID', 'タイトル', '内容', '期日', '作成日時', '更新日時']
                self.sheet.insert_row(headers, 1)
        except Exception as e:
            raise Exception(f'シートの初期化に失敗しました: {str(e)}')
    
    def get_all_todos(self):
        """全てのTODOを取得"""
        try:
            # 全データを取得（ヘッダー行を除く）
            all_records = self.sheet.get_all_records()
            
            # データを整形
            todos = []
            for record in all_records:
                todos.append({
                    'id': record.get('ID', ''),
                    'title': record.get('タイトル', ''),
                    'content': record.get('内容', ''),
                    'due_date': record.get('期日', ''),
                    'created_at': record.get('作成日時', ''),
                    'updated_at': record.get('更新日時', '')
                })
            
            return todos
        except Exception as e:
            raise Exception(f'TODOの取得に失敗しました: {str(e)}')
    
    def get_todo_by_id(self, todo_id):
        """指定されたIDのTODOを取得"""
        try:
            all_todos = self.get_all_todos()
            for todo in all_todos:
                if str(todo['id']) == str(todo_id):
                    return todo
            return None
        except Exception as e:
            raise Exception(f'TODOの取得に失敗しました: {str(e)}')
    
    def add_todo(self, title, content, due_date):
        """新しいTODOを追加"""
        try:
            # 新しいIDを生成（既存の最大ID + 1）
            all_todos = self.get_all_todos()
            new_id = max([int(todo['id']) for todo in all_todos if todo['id']], default=0) + 1
            
            # 現在時刻
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # 新しい行を追加
            new_row = [new_id, title, content, due_date, now, now]
            self.sheet.append_row(new_row)
            
            return new_id
        except Exception as e:
            raise Exception(f'TODOの追加に失敗しました: {str(e)}')
    
    def update_todo(self, todo_id, title, content, due_date):
        """TODOを更新"""
        try:
            # 該当するIDの行を探す
            all_records = self.sheet.get_all_records()
            row_index = None
            
            for idx, record in enumerate(all_records, start=2):  # ヘッダー行があるので2から開始
                if str(record.get('ID', '')) == str(todo_id):
                    row_index = idx
                    break
            
            if row_index is None:
                raise Exception(f'ID {todo_id} のTODOが見つかりません')
            
            # 更新時刻
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # 行を更新
            self.sheet.update(f'B{row_index}:F{row_index}', [[title, content, due_date, 
                                                              self.sheet.cell(row_index, 5).value, now]])
            
            return True
        except Exception as e:
            raise Exception(f'TODOの更新に失敗しました: {str(e)}')
    
    def delete_todo(self, todo_id):
        """TODOを削除"""
        try:
            # 該当するIDの行を探す
            all_records = self.sheet.get_all_records()
            row_index = None
            
            for idx, record in enumerate(all_records, start=2):  # ヘッダー行があるので2から開始
                if str(record.get('ID', '')) == str(todo_id):
                    row_index = idx
                    break
            
            if row_index is None:
                raise Exception(f'ID {todo_id} のTODOが見つかりません')
            
            # 行を削除
            self.sheet.delete_rows(row_index)
            
            return True
        except Exception as e:
            raise Exception(f'TODOの削除に失敗しました: {str(e)}')

