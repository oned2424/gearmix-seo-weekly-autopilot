"""
Google Search Console API Client
Search Consoleからデータを取得するクライアント
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional

import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build


class GmxGscClient:
    """Google Search Console APIクライアント"""
    
    SCOPES = ['https://www.googleapis.com/auth/webmasters.readonly']
    
    def __init__(self, credentials_json: Optional[str] = None):
        """
        初期化
        
        Args:
            credentials_json: サービスアカウントのJSONキー(文字列)
                            Noneの場合は環境変数から取得
        """
        if credentials_json is None:
            credentials_json = os.getenv('GMX_SERVICE_ACCOUNT_CREDENTIALS')
            
        if not credentials_json:
            raise ValueError(
                "認証情報が見つかりません。"
                "GMX_SERVICE_ACCOUNT_CREDENTIALS環境変数を設定してください。"
            )
        
        # JSON文字列をパース
        credentials_info = json.loads(credentials_json)
        
        # 認証情報を作成
        self.credentials = service_account.Credentials.from_service_account_info(
            credentials_info,
            scopes=self.SCOPES
        )
        
        # Search Console APIサービスを構築
        self.service = build('searchconsole', 'v1', credentials=self.credentials)
    
    def get_search_analytics(
        self,
        site_url: str,
        start_date: datetime,
        end_date: datetime,
        dimensions: List[str] = None,
        row_limit: int = 1000
    ) -> pd.DataFrame:
        """
        Search Analyticsデータを取得
        
        Args:
            site_url: サイトURL (例: 'https://gearmix.co.jp/')
            start_date: 開始日
            end_date: 終了日
            dimensions: ディメンション (デフォルト: ['query'])
            row_limit: 取得行数の上限
            
        Returns:
            pandas.DataFrame: 取得したデータ
        """
        if dimensions is None:
            dimensions = ['query']
        
        request = {
            'startDate': start_date.strftime('%Y-%m-%d'),
            'endDate': end_date.strftime('%Y-%m-%d'),
            'dimensions': dimensions,
            'rowLimit': row_limit,
            'startRow': 0
        }
        
        response = self.service.searchanalytics().query(
            siteUrl=site_url,
            body=request
        ).execute()
        
        # レスポンスをDataFrameに変換
        if 'rows' not in response:
            # データがない場合は空のDataFrameを返す
            columns = dimensions + ['clicks', 'impressions', 'ctr', 'position']
            return pd.DataFrame(columns=columns)
        
        rows = response['rows']
        data = []
        
        for row in rows:
            item = {}
            
            # ディメンションの値を取得
            for i, dim in enumerate(dimensions):
                item[dim] = row['keys'][i]
            
            # メトリクスの値を取得
            item['clicks'] = row['clicks']
            item['impressions'] = row['impressions']
            item['ctr'] = row['ctr']
            item['position'] = row['position']
            
            data.append(item)
        
        df = pd.DataFrame(data)
        return df
    
    def get_weekly_data(
        self,
        site_url: str,
        week_offset: int = 0,
        dimensions: List[str] = None,
        row_limit: int = 1000
    ) -> pd.DataFrame:
        """
        週次データを取得
        
        Args:
            site_url: サイトURL
            week_offset: 週のオフセット (0=今週, 1=先週, 2=先々週)
            dimensions: ディメンション
            row_limit: 取得行数の上限
            
        Returns:
            pandas.DataFrame: 週次データ
        """
        # 今日の日付
        today = datetime.now()
        
        # 週の開始日(月曜日)を計算
        days_since_monday = today.weekday()
        this_monday = today - timedelta(days=days_since_monday)
        
        # 指定された週のオフセットを適用
        target_monday = this_monday - timedelta(weeks=week_offset)
        
        # 週の終了日(日曜日)
        target_sunday = target_monday + timedelta(days=6)
        
        # データを取得
        return self.get_search_analytics(
            site_url=site_url,
            start_date=target_monday,
            end_date=target_sunday,
            dimensions=dimensions,
            row_limit=row_limit
        )
    
    def get_this_week_data(
        self,
        site_url: str,
        dimensions: List[str] = None,
        row_limit: int = 1000
    ) -> pd.DataFrame:
        """今週のデータを取得"""
        return self.get_weekly_data(
            site_url=site_url,
            week_offset=1,  # 先週(完全な週)
            dimensions=dimensions,
            row_limit=row_limit
        )
    
    def get_last_week_data(
        self,
        site_url: str,
        dimensions: List[str] = None,
        row_limit: int = 1000
    ) -> pd.DataFrame:
        """先週のデータを取得"""
        return self.get_weekly_data(
            site_url=site_url,
            week_offset=2,  # 先々週
            dimensions=dimensions,
            row_limit=row_limit
        )
