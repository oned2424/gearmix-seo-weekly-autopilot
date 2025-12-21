"""
Summary Generator
Executive Summaryを自動生成するモジュール
"""

from typing import Dict, List


class GmxSummaryGenerator:
    """サマリー生成クラス"""
    
    @staticmethod
    def generate_executive_summary(
        gsc_analysis: Dict,
        ga4_analysis: Dict
    ) -> str:
        """
        Executive Summaryを生成
        
        Args:
            gsc_analysis: GSC分析結果
            ga4_analysis: GA4分析結果
            
        Returns:
            str: Executive Summary(日本語)
        """
        summary_parts = []
        
        # タイトル
        summary_parts.append("# 📊 週次SEOレポート - エグゼクティブサマリー\n")
        
        # GSCサマリー
        gsc_summary = GmxSummaryGenerator._generate_gsc_summary(gsc_analysis)
        summary_parts.append(gsc_summary)
        
        # GA4サマリー
        ga4_summary = GmxSummaryGenerator._generate_ga4_summary(ga4_analysis)
        summary_parts.append(ga4_summary)
        
        # 改善アクション
        actions = GmxSummaryGenerator._generate_action_items(gsc_analysis, ga4_analysis)
        summary_parts.append(actions)
        
        return "\n\n".join(summary_parts)
    
    @staticmethod
    def _generate_gsc_summary(gsc_analysis: Dict) -> str:
        """GSCサマリーを生成"""
        stats = gsc_analysis['summary_stats']
        
        parts = ["## 🔍 検索パフォーマンス(Google Search Console)\n"]
        
        # クリック数
        clicks_data = stats['clicks']
        clicks_trend = "増加" if clicks_data['change_pct'] > 0 else "減少"
        clicks_emoji = "📈" if clicks_data['change_pct'] > 0 else "📉"
        
        parts.append(
            f"{clicks_emoji} **検索クリック数**: {int(clicks_data['this_week']):,}回 "
            f"(前週比 {clicks_data['change_pct']:+.1f}%)"
        )
        
        if abs(clicks_data['change_pct']) > 10:
            parts.append(
                f"   - 先週と比較して{abs(clicks_data['change_pct']):.1f}%の{clicks_trend}を記録しました。"
            )
        
        # 表示回数
        impressions_data = stats['impressions']
        impressions_trend = "増加" if impressions_data['change_pct'] > 0 else "減少"
        impressions_emoji = "👀" if impressions_data['change_pct'] > 0 else "👁️"
        
        parts.append(
            f"{impressions_emoji} **表示回数**: {int(impressions_data['this_week']):,}回 "
            f"(前週比 {impressions_data['change_pct']:+.1f}%)"
        )
        
        # CTR
        ctr_data = stats['ctr']
        ctr_trend = "改善" if ctr_data['change_pct'] > 0 else "悪化"
        ctr_emoji = "✅" if ctr_data['change_pct'] > 0 else "⚠️"
        
        parts.append(
            f"{ctr_emoji} **クリック率(CTR)**: {ctr_data['this_week']*100:.2f}% "
            f"(前週比 {ctr_data['change_pct']:+.1f}%)"
        )
        
        # 平均掲載順位
        position_data = stats['position']
        # 順位は低い方が良いので、変化率の解釈を逆にする
        position_trend = "改善" if position_data['change_pct'] < 0 else "悪化"
        position_emoji = "⬆️" if position_data['change_pct'] < 0 else "⬇️"
        
        parts.append(
            f"{position_emoji} **平均掲載順位**: {position_data['this_week']:.1f}位 "
            f"(前週比 {position_data['change_pct']:+.1f}%)"
        )
        
        # トップクエリ
        top_query = gsc_analysis['top_queries'].iloc[0]
        parts.append(
            f"\n💡 **最もパフォーマンスの高いクエリ**: 「{top_query['query']}」"
            f"({int(top_query['clicks'])}クリック)"
        )
        
        # 最も改善したクエリ
        if len(gsc_analysis['biggest_movers']['improved']) > 0:
            improved_query = gsc_analysis['biggest_movers']['improved'].iloc[0]
            parts.append(
                f"🚀 **最も成長したクエリ**: 「{improved_query['query']}」"
                f"({int(improved_query['clicks_delta']):+d}クリック)"
            )
        
        # 最も悪化したクエリ
        if len(gsc_analysis['biggest_movers']['declined']) > 0:
            declined_query = gsc_analysis['biggest_movers']['declined'].iloc[0]
            parts.append(
                f"⚠️ **最も減少したクエリ**: 「{declined_query['query']}」"
                f"({int(declined_query['clicks_delta']):+d}クリック)"
            )
        
        return "\n".join(parts)
    
    @staticmethod
    def _generate_ga4_summary(ga4_analysis: Dict) -> str:
        """GA4サマリーを生成"""
        stats = ga4_analysis['summary_stats']
        
        parts = ["## 📈 トラフィック分析(Google Analytics 4)\n"]
        
        # セッション数
        sessions_data = stats['sessions']
        sessions_trend = "増加" if sessions_data['change_pct'] > 0 else "減少"
        sessions_emoji = "📊" if sessions_data['change_pct'] > 0 else "📉"
        
        parts.append(
            f"{sessions_emoji} **総セッション数**: {int(sessions_data['this_week']):,} "
            f"(前週比 {sessions_data['change_pct']:+.1f}%)"
        )
        
        # ユーザー数
        users_data = stats['totalUsers']
        users_emoji = "👥" if users_data['change_pct'] > 0 else "👤"
        
        parts.append(
            f"{users_emoji} **総ユーザー数**: {int(users_data['this_week']):,} "
            f"(前週比 {users_data['change_pct']:+.1f}%)"
        )
        
        # ページビュー数
        pageviews_data = stats['screenPageViews']
        pageviews_emoji = "📄" if pageviews_data['change_pct'] > 0 else "📃"
        
        parts.append(
            f"{pageviews_emoji} **ページビュー数**: {int(pageviews_data['this_week']):,} "
            f"(前週比 {pageviews_data['change_pct']:+.1f}%)"
        )
        
        # チャネル別分析
        wow_df = ga4_analysis['wow_comparison']
        organic_row = wow_df[wow_df['sessionDefaultChannelGroup'] == 'Organic Search']
        
        if len(organic_row) > 0:
            organic_sessions = int(organic_row.iloc[0]['sessions_this_week'])
            organic_change = organic_row.iloc[0]['sessions_change_pct']
            organic_emoji = "🌿" if organic_change > 0 else "🍂"
            
            parts.append(
                f"\n{organic_emoji} **オーガニック検索セッション**: {organic_sessions:,} "
                f"(前週比 {organic_change:+.1f}%)"
            )
        
        return "\n".join(parts)
    
    @staticmethod
    def _generate_action_items(gsc_analysis: Dict, ga4_analysis: Dict) -> str:
        """改善アクションを生成"""
        parts = ["## 🎯 推奨アクション\n"]
        
        actions = []
        
        # GSCデータに基づくアクション
        clicks_change = gsc_analysis['summary_stats']['clicks']['change_pct']
        ctr_change = gsc_analysis['summary_stats']['ctr']['change_pct']
        position_change = gsc_analysis['summary_stats']['position']['change_pct']
        
        if clicks_change < -10:
            actions.append(
                "🔴 **緊急**: クリック数が大幅に減少しています。"
                "減少したクエリを分析し、コンテンツの改善や内部リンクの最適化を検討してください。"
            )
        elif clicks_change > 10:
            actions.append(
                "🟢 **好調**: クリック数が大幅に増加しています。"
                "成功要因を分析し、他のページにも同様の施策を展開しましょう。"
            )
        
        if ctr_change < -5:
            actions.append(
                "🟡 **注意**: CTRが低下しています。"
                "タイトルタグやメタディスクリプションの見直しを検討してください。"
            )
        
        if position_change > 5:  # 順位は高い方が悪化
            actions.append(
                "🟡 **注意**: 平均掲載順位が低下しています。"
                "コンテンツの品質向上とSEO最適化を強化しましょう。"
            )
        
        # 成長クエリに基づくアクション
        if len(gsc_analysis['biggest_movers']['improved']) > 0:
            actions.append(
                "💡 **機会**: 成長しているクエリに関連するコンテンツを拡充し、"
                "さらなるトラフィック増加を目指しましょう。"
            )
        
        # GA4データに基づくアクション
        sessions_change = ga4_analysis['summary_stats']['sessions']['change_pct']
        
        if sessions_change < -10:
            actions.append(
                "🔴 **緊急**: 全体のセッション数が大幅に減少しています。"
                "全チャネルのパフォーマンスを確認し、問題を特定してください。"
            )
        
        if not actions:
            actions.append(
                "✅ **安定**: 全体的に安定したパフォーマンスを維持しています。"
                "継続的な改善とモニタリングを続けましょう。"
            )
        
        parts.extend(actions)
        
        return "\n\n".join(parts)
