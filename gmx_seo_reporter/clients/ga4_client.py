"""
Google Analytics 4 API Client
GA4からデータを取得するクライアント
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional

import pandas as pd
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
)
from google.oauth2 import service_account


class GmxGa4Client:
    """Google Analytics 4 APIクライアント"""
    
    SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
    
    def __init__(
        self,
        property_id: Optional[str] = None,
        credentials_json: Optional[str] = None
    ):
        """
        初期化
        
        Args:
            property_id: GA4プロパティID
                        Noneの場合は環境変数から取得
            credentials_json: サービスアカウントのJSONキー(文字列)
                            Noneの場合は環境変数から取得
        """
        # プロパティIDを取得
        if property_id is None:
            property_id = os.getenv('GMX_GA4_PROPERTY_ID')
        
        if not property_id:
            raise ValueError(
                "GA4プロパティIDが見つかりません。"
                "GMX_GA4_PROPERTY_ID環境変数を設定してください。"
            )
        
        self.property_id = property_id
        
        # 認証情報を取得
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
        
        # GA4 APIクライアントを構築
        self.client = BetaAnalyticsDataClient(credentials=self.credentials)
    
    def run_report(
        self,
        start_date: datetime,
        end_date: datetime,
        dimensions: List[str],
        metrics: List[str]
    ) -> pd.DataFrame:
        """
        レポートを実行してデータを取得
        
        Args:
            start_date: 開始日
            end_date: 終了日
            dimensions: ディメンションのリスト
            metrics: メトリクスのリスト
            
        Returns:
            pandas.DataFrame: 取得したデータ
        """
        request = RunReportRequest(
            property=f"properties/{self.property_id}",
            date_ranges=[DateRange(
                start_date=start_date.strftime('%Y-%m-%d'),
                end_date=end_date.strftime('%Y-%m-%d')
            )],
            dimensions=[Dimension(name=dim) for dim in dimensions],
            metrics=[Metric(name=metric) for metric in metrics]
        )
        
        response = self.client.run_report(request)
        
        # レスポンスをDataFrameに変換
        if not response.rows:
            # データがない場合は空のDataFrameを返す
            columns = dimensions + metrics
            return pd.DataFrame(columns=columns)
        
        data = []
        
        for row in response.rows:
            item = {}
            
            # ディメンションの値を取得
            for i, dim in enumerate(dimensions):
                item[dim] = row.dimension_values[i].value
            
            # メトリクスの値を取得
            for i, metric in enumerate(metrics):
                value = row.metric_values[i].value
                # 数値に変換
                try:
                    item[metric] = float(value)
                except ValueError:
                    item[metric] = value
            
            data.append(item)
        
        df = pd.DataFrame(data)
        return df
    
    def get_weekly_data(
        self,
        week_offset: int = 0,
        dimensions: List[str] = None,
        metrics: List[str] = None
    ) -> pd.DataFrame:
        """
        週次データを取得
        
        Args:
            week_offset: 週のオフセット (0=今週, 1=先週, 2=先々週)
            dimensions: ディメンションのリスト
            metrics: メトリクスのリスト
            
        Returns:
            pandas.DataFrame: 週次データ
        """
        if dimensions is None:
            dimensions = ['sessionDefaultChannelGroup']
        
        if metrics is None:
            metrics = ['sessions', 'totalUsers', 'screenPageViews']
        
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
        return self.run_report(
            start_date=target_monday,
            end_date=target_sunday,
            dimensions=dimensions,
            metrics=metrics
        )
    
    def get_this_week_data(
        self,
        dimensions: List[str] = None,
        metrics: List[str] = None
    ) -> pd.DataFrame:
        """今週のデータを取得"""
        return self.get_weekly_data(
            week_offset=1,  # 先週(完全な週)
            dimensions=dimensions,
            metrics=metrics
        )
    
    def get_last_week_data(
        self,
        dimensions: List[str] = None,
        metrics: List[str] = None
    ) -> pd.DataFrame:
        """先週のデータを取得"""
        return self.get_weekly_data(
            week_offset=2,  # 先々週
            dimensions=dimensions,
            metrics=metrics
        )
