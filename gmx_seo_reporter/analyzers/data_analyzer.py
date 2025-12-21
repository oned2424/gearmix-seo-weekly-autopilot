"""
Data Analyzer
データ分析と前週比較(WoW)を行うモジュール
"""

from typing import Dict, List, Tuple

import pandas as pd


class GmxDataAnalyzer:
    """データ分析クラス"""
    
    @staticmethod
    def calculate_wow_comparison(
        this_week_df: pd.DataFrame,
        last_week_df: pd.DataFrame,
        key_column: str,
        metric_columns: List[str]
    ) -> pd.DataFrame:
        """
        Week over Week (WoW) 比較を計算
        
        Args:
            this_week_df: 今週のデータ
            last_week_df: 先週のデータ
            key_column: キーとなるカラム名 (例: 'query')
            metric_columns: 比較するメトリクスのカラム名リスト
            
        Returns:
            pandas.DataFrame: WoW比較結果
        """
        # 今週と先週のデータをマージ
        merged = this_week_df.merge(
            last_week_df,
            on=key_column,
            how='outer',
            suffixes=('_this_week', '_last_week')
        )
        
        # 各メトリクスについて差分と変化率を計算
        for metric in metric_columns:
            this_col = f'{metric}_this_week'
            last_col = f'{metric}_last_week'
            delta_col = f'{metric}_delta'
            change_col = f'{metric}_change_pct'
            
            # 欠損値を0で埋める
            merged[this_col] = merged[this_col].fillna(0)
            merged[last_col] = merged[last_col].fillna(0)
            
            # 差分を計算
            merged[delta_col] = merged[this_col] - merged[last_col]
            
            # 変化率を計算 (%)
            merged[change_col] = merged.apply(
                lambda row: (
                    ((row[this_col] - row[last_col]) / row[last_col] * 100)
                    if row[last_col] != 0
                    else (100 if row[this_col] > 0 else 0)
                ),
                axis=1
            )
        
        return merged
    
    @staticmethod
    def get_top_performers(
        df: pd.DataFrame,
        metric_column: str,
        n: int = 20
    ) -> pd.DataFrame:
        """
        トップパフォーマーを取得
        
        Args:
            df: データフレーム
            metric_column: ソートに使用するメトリクスカラム
            n: 取得する件数
            
        Returns:
            pandas.DataFrame: トップN件のデータ
        """
        return df.nlargest(n, metric_column)
    
    @staticmethod
    def get_biggest_movers(
        wow_df: pd.DataFrame,
        metric: str,
        n: int = 10,
        direction: str = 'both'
    ) -> Dict[str, pd.DataFrame]:
        """
        最も変化が大きかった項目を取得
        
        Args:
            wow_df: WoW比較データ
            metric: 対象メトリクス
            n: 取得する件数
            direction: 'up' (改善), 'down' (悪化), 'both' (両方)
            
        Returns:
            Dict: {'improved': DataFrame, 'declined': DataFrame}
        """
        delta_col = f'{metric}_delta'
        
        result = {}
        
        if direction in ['up', 'both']:
            # 最も改善した項目
            improved = wow_df.nlargest(n, delta_col)
            result['improved'] = improved
        
        if direction in ['down', 'both']:
            # 最も悪化した項目
            declined = wow_df.nsmallest(n, delta_col)
            result['declined'] = declined
        
        return result
    
    @staticmethod
    def calculate_summary_stats(
        this_week_df: pd.DataFrame,
        last_week_df: pd.DataFrame,
        metric_columns: List[str]
    ) -> Dict[str, Dict[str, float]]:
        """
        サマリー統計を計算
        
        Args:
            this_week_df: 今週のデータ
            last_week_df: 先週のデータ
            metric_columns: メトリクスカラムのリスト
            
        Returns:
            Dict: サマリー統計
        """
        summary = {}
        
        for metric in metric_columns:
            this_total = this_week_df[metric].sum()
            last_total = last_week_df[metric].sum()
            delta = this_total - last_total
            change_pct = (delta / last_total * 100) if last_total != 0 else 0
            
            summary[metric] = {
                'this_week': this_total,
                'last_week': last_total,
                'delta': delta,
                'change_pct': change_pct
            }
        
        return summary
    
    @staticmethod
    def analyze_gsc_data(
        this_week_df: pd.DataFrame,
        last_week_df: pd.DataFrame
    ) -> Dict:
        """
        GSCデータを分析
        
        Args:
            this_week_df: 今週のGSCデータ
            last_week_df: 先週のGSCデータ
            
        Returns:
            Dict: 分析結果
        """
        # WoW比較
        wow_comparison = GmxDataAnalyzer.calculate_wow_comparison(
            this_week_df,
            last_week_df,
            key_column='query',
            metric_columns=['clicks', 'impressions', 'ctr', 'position']
        )
        
        # サマリー統計
        summary_stats = GmxDataAnalyzer.calculate_summary_stats(
            this_week_df,
            last_week_df,
            metric_columns=['clicks', 'impressions', 'ctr', 'position']
        )
        
        # トップクエリ
        top_queries = GmxDataAnalyzer.get_top_performers(
            this_week_df,
            metric_column='clicks',
            n=20
        )
        
        # 最も変化が大きかったクエリ
        biggest_movers_clicks = GmxDataAnalyzer.get_biggest_movers(
            wow_comparison,
            metric='clicks',
            n=10
        )
        
        return {
            'wow_comparison': wow_comparison,
            'summary_stats': summary_stats,
            'top_queries': top_queries,
            'biggest_movers': biggest_movers_clicks
        }
    
    @staticmethod
    def analyze_ga4_data(
        this_week_df: pd.DataFrame,
        last_week_df: pd.DataFrame
    ) -> Dict:
        """
        GA4データを分析
        
        Args:
            this_week_df: 今週のGA4データ
            last_week_df: 先週のGA4データ
            
        Returns:
            Dict: 分析結果
        """
        # WoW比較
        wow_comparison = GmxDataAnalyzer.calculate_wow_comparison(
            this_week_df,
            last_week_df,
            key_column='sessionDefaultChannelGroup',
            metric_columns=['sessions', 'totalUsers', 'screenPageViews']
        )
        
        # サマリー統計
        summary_stats = GmxDataAnalyzer.calculate_summary_stats(
            this_week_df,
            last_week_df,
            metric_columns=['sessions', 'totalUsers', 'screenPageViews']
        )
        
        return {
            'wow_comparison': wow_comparison,
            'summary_stats': summary_stats
        }
