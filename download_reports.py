#!/usr/bin/env python3
"""
週次SEOレポート自動ダウンロードスクリプト

GitHubリポジトリから最新の週次レポートをダウンロードし、
指定されたローカルディレクトリに保存します。
"""

import os
import sys
import json
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path

# 設定
GITHUB_REPO = "oned2424/gearmix-seo-weekly-autopilot"
GITHUB_BRANCH = "main"
REPORTS_PATH = "reports/weekly"
TARGET_DIR = "/Users/apple/Library/CloudStorage/GoogleDrive-yuma2433@gmail.com/マイドライブ/ObsidianVault/13_クライアント/森川さん_home/1_分析_森川さん/1_分析データ_森川さん/001_site_週次・月次分析用_自動/001_週次"

# GitHub API URL
GITHUB_API_BASE = "https://api.github.com"
GITHUB_RAW_BASE = "https://raw.githubusercontent.com"


def log(message):
    """ログメッセージを出力"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")


def get_latest_report_date():
    """GitHubから最新のレポート日付を取得"""
    url = f"{GITHUB_API_BASE}/repos/{GITHUB_REPO}/contents/{REPORTS_PATH}?ref={GITHUB_BRANCH}"
    
    try:
        log(f"GitHubから最新レポートを確認中: {url}")
        req = urllib.request.Request(url)
        req.add_header('Accept', 'application/vnd.github.v3+json')
        req.add_header('User-Agent', 'Python-Report-Downloader')
        
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            
        # ディレクトリのみをフィルタリング
        directories = [item['name'] for item in data if item['type'] == 'dir']
        
        if not directories:
            log("レポートディレクトリが見つかりませんでした")
            return None
            
        # 日付形式のディレクトリを降順でソート
        directories.sort(reverse=True)
        latest_date = directories[0]
        
        log(f"最新のレポート日付: {latest_date}")
        return latest_date
        
    except urllib.error.HTTPError as e:
        error_body = e.read().decode() if e.fp else ""
        log(f"HTTPエラー: {e.code} - {e.reason}")
        log(f"エラー詳細: {error_body}")
        return None
    except Exception as e:
        log(f"エラー: {str(e)}")
        import traceback
        log(f"トレースバック: {traceback.format_exc()}")
        return None


def get_report_files(report_date):
    """指定された日付のレポートファイル一覧を取得"""
    url = f"{GITHUB_API_BASE}/repos/{GITHUB_REPO}/contents/{REPORTS_PATH}/{report_date}?ref={GITHUB_BRANCH}"
    
    try:
        log(f"レポートファイル一覧を取得中: {report_date}")
        req = urllib.request.Request(url)
        req.add_header('Accept', 'application/vnd.github.v3+json')
        
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            
        # ファイルのみをフィルタリング
        files = [item for item in data if item['type'] == 'file']
        
        log(f"{len(files)}個のファイルが見つかりました")
        return files
        
    except Exception as e:
        log(f"エラー: {str(e)}")
        return []


def download_file(file_info, target_dir, report_date):
    """ファイルをダウンロード"""
    filename = file_info['name']
    download_url = file_info['download_url']
    
    # 日付ごとのサブディレクトリを作成
    date_dir = os.path.join(target_dir, report_date)
    os.makedirs(date_dir, exist_ok=True)
    
    target_path = os.path.join(date_dir, filename)
    
    # 既にファイルが存在する場合はスキップ
    if os.path.exists(target_path):
        log(f"スキップ (既存): {filename}")
        return True
    
    try:
        log(f"ダウンロード中: {filename}")
        urllib.request.urlretrieve(download_url, target_path)
        log(f"保存完了: {target_path}")
        return True
        
    except Exception as e:
        log(f"ダウンロード失敗 ({filename}): {str(e)}")
        return False


def main():
    """メイン処理"""
    log("=== 週次SEOレポート自動ダウンロード開始 ===")
    
    # ターゲットディレクトリの確認
    target_dir = Path(TARGET_DIR)
    if not target_dir.exists():
        log(f"エラー: ターゲットディレクトリが存在しません: {TARGET_DIR}")
        sys.exit(1)
    
    log(f"ターゲットディレクトリ: {TARGET_DIR}")
    
    # 最新のレポート日付を取得
    latest_date = get_latest_report_date()
    if not latest_date:
        log("最新のレポートが見つかりませんでした")
        sys.exit(1)
    
    # レポートファイル一覧を取得
    files = get_report_files(latest_date)
    if not files:
        log("ダウンロードするファイルがありません")
        sys.exit(1)
    
    # 各ファイルをダウンロード
    success_count = 0
    for file_info in files:
        if download_file(file_info, TARGET_DIR, latest_date):
            success_count += 1
    
    log(f"=== ダウンロード完了: {success_count}/{len(files)}個のファイル ===")
    log(f"保存先: {os.path.join(TARGET_DIR, latest_date)}")
    
    if success_count == 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
