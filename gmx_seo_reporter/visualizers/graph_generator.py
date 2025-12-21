"""
Graph Generator
グラフを生成するモジュール
"""

import os
from datetime import datetime
from typing import Dict, List, Optional

import matplotlib
matplotlib.use('Agg')  # GUIなし環境用
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# 日本語フォント設定
plt.rcParams['font.sans-serif'] = ['Hiragino Sans', 'Yu Gothic', 'Meirio', 'Takao', 'IPAexGothic', 'IPAPGothic', 'Noto Sans CJK JP']
plt.rcParams['axes.unicode_minus'] = False


class GmxReportVisualizer:
    """レポート用グラフ生成クラス"""
    
    def __init__(self, config: Dict = None):
        """
        初期化
        
        Args:
            config: ビジュアライゼーション設定
        """
        self.config = config or {}
        
        # スタイル設定
        style = self.config.get('graph_style', 'seaborn')
        if style == 'seaborn':
            sns.set_style("whitegrid")
        
        # カラースキーム
        self.colors = self.config.get('color_scheme', {
            'primary': '#2E86AB',
            'secondary': '#A23B72',
            'success': '#06A77D',
            'warning': '#F18F01',
            'danger': '#C73E1D'
        })
        
        # 図のサイズとDPI
        self.figure_size = self.config.get('figure_size', [12, 6])
        self.dpi = self.config.get('dpi', 100)
    
    def create_clicks_trend_graph(
        self,
        summary_stats: Dict,
        output_path: str
    ) -> str:
        """
        クリック数トレンドグラフを作成
        
        Args:
            summary_stats: サマリー統計
            output_path: 出力パス
            
        Returns:
            str: 保存したファイルパス
        """
        fig, ax = plt.subplots(figsize=self.figure_size, dpi=self.dpi)
        
        # データ準備
        weeks = ['先々週', '先週']
        clicks = [
            summary_stats['clicks']['last_week'],
            summary_stats['clicks']['this_week']
        ]
        
        # 棒グラフ
        bars = ax.bar(weeks, clicks, color=self.colors['primary'], alpha=0.7)
        
        # 値をバーの上に表示
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2.,
                height,
                f'{int(height):,}',
                ha='center',
                va='bottom',
                fontsize=12,
                fontweight='bold'
            )
        
        # 変化率を表示
        change_pct = summary_stats['clicks']['change_pct']
        color = self.colors['success'] if change_pct > 0 else self.colors['danger']
        ax.text(
            0.5, 0.95,
            f'前週比: {change_pct:+.1f}%',
            transform=ax.transAxes,
            ha='center',
            va='top',
            fontsize=14,
            fontweight='bold',
            color=color,
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8)
        )
        
        ax.set_ylabel('クリック数', fontsize=12)
        ax.set_title('検索クリック数の推移', fontsize=14, fontweight='bold', pad=20)
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=self.dpi, bbox_inches='tight')
        plt.close()
        
        return output_path
    
    def create_ctr_comparison_graph(
        self,
        summary_stats: Dict,
        output_path: str
    ) -> str:
        """
        CTR比較グラフを作成
        
        Args:
            summary_stats: サマリー統計
            output_path: 出力パス
            
        Returns:
            str: 保存したファイルパス
        """
        fig, ax = plt.subplots(figsize=self.figure_size, dpi=self.dpi)
        
        # データ準備
        weeks = ['先々週', '先週']
        ctr = [
            summary_stats['ctr']['last_week'] * 100,  # パーセント表示
            summary_stats['ctr']['this_week'] * 100
        ]
        
        # 棒グラフ
        bars = ax.bar(weeks, ctr, color=self.colors['secondary'], alpha=0.7)
        
        # 値をバーの上に表示
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2.,
                height,
                f'{height:.2f}%',
                ha='center',
                va='bottom',
                fontsize=12,
                fontweight='bold'
            )
        
        # 変化率を表示
        change_pct = summary_stats['ctr']['change_pct']
        color = self.colors['success'] if change_pct > 0 else self.colors['danger']
        ax.text(
            0.5, 0.95,
            f'前週比: {change_pct:+.1f}%',
            transform=ax.transAxes,
            ha='center',
            va='top',
            fontsize=14,
            fontweight='bold',
            color=color,
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8)
        )
        
        ax.set_ylabel('CTR (%)', fontsize=12)
        ax.set_title('クリック率(CTR)の推移', fontsize=14, fontweight='bold', pad=20)
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=self.dpi, bbox_inches='tight')
        plt.close()
        
        return output_path
    
    def create_channel_sessions_graph(
        self,
        ga4_analysis: Dict,
        output_path: str
    ) -> str:
        """
        チャネル別セッション数グラフを作成
        
        Args:
            ga4_analysis: GA4分析結果
            output_path: 出力パス
            
        Returns:
            str: 保存したファイルパス
        """
        fig, ax = plt.subplots(figsize=self.figure_size, dpi=self.dpi)
        
        wow_df = ga4_analysis['wow_comparison']
        
        # データ準備
        channels = wow_df['sessionDefaultChannelGroup'].tolist()
        this_week = wow_df['sessions_this_week'].tolist()
        last_week = wow_df['sessions_last_week'].tolist()
        
        # バーの位置
        x = range(len(channels))
        width = 0.35
        
        # 棒グラフ
        bars1 = ax.bar(
            [i - width/2 for i in x],
            last_week,
            width,
            label='先々週',
            color=self.colors['primary'],
            alpha=0.6
        )
        bars2 = ax.bar(
            [i + width/2 for i in x],
            this_week,
            width,
            label='先週',
            color=self.colors['success'],
            alpha=0.8
        )
        
        ax.set_xlabel('チャネル', fontsize=12)
        ax.set_ylabel('セッション数', fontsize=12)
        ax.set_title('チャネル別セッション数', fontsize=14, fontweight='bold', pad=20)
        ax.set_xticks(x)
        ax.set_xticklabels(channels, rotation=45, ha='right')
        ax.legend()
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=self.dpi, bbox_inches='tight')
        plt.close()
        
        return output_path
    
    def create_top_queries_graph(
        self,
        top_queries: pd.DataFrame,
        output_path: str,
        n: int = 10
    ) -> str:
        """
        トップクエリグラフを作成
        
        Args:
            top_queries: トップクエリデータ
            output_path: 出力パス
            n: 表示する件数
            
        Returns:
            str: 保存したファイルパス
        """
        fig, ax = plt.subplots(figsize=self.figure_size, dpi=self.dpi)
        
        # 上位N件を取得
        data = top_queries.head(n).copy()
        data = data.sort_values('clicks', ascending=True)  # 昇順でプロット
        
        # 横棒グラフ
        bars = ax.barh(
            range(len(data)),
            data['clicks'],
            color=self.colors['primary'],
            alpha=0.7
        )
        
        # クエリ名を設定
        ax.set_yticks(range(len(data)))
        ax.set_yticklabels(data['query'], fontsize=10)
        
        # 値をバーの右に表示
        for i, (idx, row) in enumerate(data.iterrows()):
            ax.text(
                row['clicks'],
                i,
                f" {int(row['clicks']):,}",
                va='center',
                fontsize=10
            )
        
        ax.set_xlabel('クリック数', fontsize=12)
        ax.set_title(f'トップ{n}検索クエリ', fontsize=14, fontweight='bold', pad=20)
        ax.grid(axis='x', alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=self.dpi, bbox_inches='tight')
        plt.close()
        
        return output_path
