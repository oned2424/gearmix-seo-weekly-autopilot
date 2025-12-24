#!/usr/bin/env python3
"""
GearMix Weekly SEO Report Generator
週次SEOレポートを自動生成するメインスクリプト
"""

import os
import sys
from datetime import datetime
from pathlib import Path

import yaml

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from gmx_seo_reporter.clients.gsc_client import GmxGscClient
from gmx_seo_reporter.clients.ga4_client import GmxGa4Client
from gmx_seo_reporter.analyzers.data_analyzer import GmxDataAnalyzer
from gmx_seo_reporter.visualizers.graph_generator import GmxReportVisualizer
from gmx_seo_reporter.generators.summary_generator import GmxSummaryGenerator
from gmx_seo_reporter.generators.report_builder import GmxReportBuilder
from gmx_seo_reporter.clients.drive_client import GmxDriveClient


def load_config(config_path: str = None) -> dict:
    """設定ファイルを読み込み"""
    if config_path is None:
        config_path = project_root / 'config' / 'gmx_config.yaml'
    
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def main():
    """メイン処理"""
    print("=" * 60)
    print("GearMix Weekly SEO Report Generator")
    print("=" * 60)
    print()
    
    # 設定を読み込み
    print("📋 設定ファイルを読み込み中...")
    config = load_config()
    site_url = config['site']['url']
    print(f"   対象サイト: {site_url}")
    print()
    
    # 出力ディレクトリを作成
    today = datetime.now()
    output_dir = project_root / config['output']['directory'] / today.strftime('%Y-%m-%d')
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"📁 出力ディレクトリ: {output_dir}")
    print()
    
    # === STEP 1: データ取得 ===
    print("🔍 STEP 1: データ取得")
    print("-" * 60)
    
    # GSCクライアントを初期化
    print("   Google Search Consoleに接続中...")
    gsc_client = GmxGscClient()
    
    # GSCデータを取得
    print("   GSCデータを取得中...")
    gsc_this_week = gsc_client.get_this_week_data(
        site_url=site_url,
        dimensions=config['gsc']['dimensions'],
        row_limit=config['gsc']['row_limit']
    )
    gsc_last_week = gsc_client.get_last_week_data(
        site_url=site_url,
        dimensions=config['gsc']['dimensions'],
        row_limit=config['gsc']['row_limit']
    )
    print(f"   ✓ GSCデータ取得完了 (今週: {len(gsc_this_week)}件, 先週: {len(gsc_last_week)}件)")
    
    # GA4クライアントを初期化
    print("   Google Analytics 4に接続中...")
    ga4_client = GmxGa4Client()
    
    # GA4データを取得
    print("   GA4データを取得中...")
    ga4_this_week = ga4_client.get_this_week_data(
        dimensions=config['ga4']['dimensions'],
        metrics=config['ga4']['metrics']
    )
    ga4_last_week = ga4_client.get_last_week_data(
        dimensions=config['ga4']['dimensions'],
        metrics=config['ga4']['metrics']
    )
    print(f"   ✓ GA4データ取得完了 (今週: {len(ga4_this_week)}件, 先週: {len(ga4_last_week)}件)")
    print()
    
    # === STEP 2: データ分析 ===
    print("📊 STEP 2: データ分析")
    print("-" * 60)
    
    print("   GSCデータを分析中...")
    gsc_analysis = GmxDataAnalyzer.analyze_gsc_data(gsc_this_week, gsc_last_week)
    print("   ✓ GSC分析完了")
    
    print("   GA4データを分析中...")
    ga4_analysis = GmxDataAnalyzer.analyze_ga4_data(ga4_this_week, ga4_last_week)
    print("   ✓ GA4分析完了")
    print()
    
    # === STEP 3: グラフ生成 ===
    print("📈 STEP 3: グラフ生成")
    print("-" * 60)
    
    visualizer = GmxReportVisualizer(config=config.get('visualization', {}))
    graphs = []
    
    # クリック数トレンドグラフ
    print("   クリック数トレンドグラフを生成中...")
    clicks_graph_path = output_dir / f"gmx_graph_clicks_trend_{today.strftime('%Y-%m-%d')}.png"
    visualizer.create_clicks_trend_graph(gsc_analysis['summary_stats'], str(clicks_graph_path))
    graphs.append({'title': 'クリック数の推移', 'path': clicks_graph_path.name})
    print(f"   ✓ 保存: {clicks_graph_path.name}")
    
    # CTR比較グラフ
    print("   CTR比較グラフを生成中...")
    ctr_graph_path = output_dir / f"gmx_graph_ctr_comparison_{today.strftime('%Y-%m-%d')}.png"
    visualizer.create_ctr_comparison_graph(gsc_analysis['summary_stats'], str(ctr_graph_path))
    graphs.append({'title': 'CTRの推移', 'path': ctr_graph_path.name})
    print(f"   ✓ 保存: {ctr_graph_path.name}")
    
    # チャネル別セッショングラフ
    print("   チャネル別セッショングラフを生成中...")
    channel_graph_path = output_dir / f"gmx_graph_channel_sessions_{today.strftime('%Y-%m-%d')}.png"
    visualizer.create_channel_sessions_graph(ga4_analysis, str(channel_graph_path))
    graphs.append({'title': 'チャネル別セッション数', 'path': channel_graph_path.name})
    print(f"   ✓ 保存: {channel_graph_path.name}")
    
    # トップクエリグラフ
    print("   トップクエリグラフを生成中...")
    top_queries_graph_path = output_dir / f"gmx_graph_top_queries_{today.strftime('%Y-%m-%d')}.png"
    visualizer.create_top_queries_graph(gsc_analysis['top_queries'], str(top_queries_graph_path), n=10)
    graphs.append({'title': 'トップ10検索クエリ', 'path': top_queries_graph_path.name})
    print(f"   ✓ 保存: {top_queries_graph_path.name}")
    print()
    
    # === STEP 4: Executive Summary生成 ===
    print("📝 STEP 4: Executive Summary生成")
    print("-" * 60)
    
    print("   サマリーを生成中...")
    executive_summary = GmxSummaryGenerator.generate_executive_summary(
        gsc_analysis,
        ga4_analysis
    )
    print("   ✓ サマリー生成完了")
    print()
    
    # === STEP 5: HTMLレポート生成 ===
    print("🎨 STEP 5: HTMLレポート生成")
    print("-" * 60)
    
    print("   HTMLレポートを構築中...")
    report_builder = GmxReportBuilder(config=config.get('report', {}))
    
    # トップクエリをリストに変換
    top_queries_list = gsc_analysis['top_queries'].head(20).to_dict('records')
    
    # レポートを生成
    report_path = output_dir / f"gmx_weekly_report_{today.strftime('%Y-%m-%d')}.html"
    report_builder.build_report(
        executive_summary=executive_summary,
        graphs=graphs,
        top_queries=top_queries_list,
        output_path=str(report_path),
        title=config['report'].get('title', 'GearMix週次SEOレポート'),
        subtitle=config['report'].get('subtitle', '検索パフォーマンス分析')
    )
    print(f"   ✓ レポート保存: {report_path}")
    print()
    
    # === 完了 ===
    print("=" * 60)
    print("✅ レポート生成が完了しました!")
    print("=" * 60)
    print()
    print(f"📄 レポート: {report_path}")
    print(f"📊 グラフ: {len(graphs)}個")
    print()
    print("レポートをブラウザで開いてご確認ください。")
    print()

    # === STEP 6: Google Driveへアップロード ===
    if config.get('drive', {}).get('enabled', False):
        print("☁️ STEP 6: Google Driveへアップロード")
        print("-" * 60)
        
        drive_folder_id = os.environ.get('GMX_DRIVE_FOLDER_ID')
        if not drive_folder_id:
            print("   ⚠️ 環境変数 GMX_DRIVE_FOLDER_ID が設定されていないためスキップします")
        else:
            try:
                # 認証情報の取得 (Drive専用 -> 共通の順で探す)
                creds_json_str = os.environ.get('GMX_DRIVE_CREDENTIALS')
                if not creds_json_str:
                    print("   ℹ️ Drive専用の鍵が見つからないため、共通の鍵を使用します")
                    creds_json_str = os.environ.get('GMX_SERVICE_ACCOUNT_CREDENTIALS')
                
                if not creds_json_str:
                    print("   ❌ 認証情報が見つからないためスキップします")
                else:
                    import json
                    creds_json = json.loads(creds_json_str)
                    
                    print(f"   Google Driveに接続中... (Target ID: {drive_folder_id})")
                    drive_client = GmxDriveClient(
                        folder_id=drive_folder_id,
                        credentials_json=creds_json
                    )
                    
                    print(f"   フォルダをアップロード中...: {output_dir.name}")
                    uploaded_id = drive_client.upload_folder(output_dir)
                    print(f"   ✅ アップロード完了! (Folder ID: {uploaded_id})")
            except Exception as e:
                print(f"   ❌ アップロードに失敗しました: {e}")
                import traceback
                traceback.print_exc()
    print()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"\n❌ エラーが発生しました: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)
