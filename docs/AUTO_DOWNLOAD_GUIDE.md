# レポート自動ダウンロード - セットアップガイド

## 📥 概要

このガイドでは、GitHub Actionsで生成された週次SEOレポートを、ローカルディレクトリに自動的にダウンロードする機能のセットアップ方法を説明します。

**ダウンロード先**: `/Users/apple/Library/CloudStorage/GoogleDrive-yuma2433@gmail.com/マイドライブ/ObsidianVault/13_クライアント/森川さん_home/1_分析_森川さん/1_分析データ_森川さん/001_site_週次・月次分析用_自動/001_週次`

**自動実行**: 毎週月曜日 9:30 AM

---

## 🔧 セットアップ手順

### 1. LaunchAgentの設定

LaunchAgentファイルを正しい場所にコピーします。

```bash
# LaunchAgentファイルをコピー
cp "/Users/apple/Library/CloudStorage/GoogleDrive-yuma2433@gmail.com/マイドライブ/ObsidianVault/13_クライアント/森川さん_home/1_分析_森川さん/1_分析データ_森川さん/000_週次自動データツール/com.gearmix.seo.report.downloader.plist" ~/Library/LaunchAgents/

# 権限を設定
chmod 644 ~/Library/LaunchAgents/com.gearmix.seo.report.downloader.plist

# LaunchAgentを読み込み
launchctl load ~/Library/LaunchAgents/com.gearmix.seo.report.downloader.plist
```

### 2. 動作確認

設定が正しく行われたか確認します。

```bash
# LaunchAgentが読み込まれているか確認
launchctl list | grep gearmix

# 手動で即座に実行してテスト
launchctl start com.gearmix.seo.report.downloader

# ログを確認
cat /tmp/gearmix-seo-report-downloader.log
```

---

## 🧪 手動実行

自動実行を待たずに、手動でレポートをダウンロードすることもできます。

```bash
cd "/Users/apple/Library/CloudStorage/GoogleDrive-yuma2433@gmail.com/マイドライブ/ObsidianVault/13_クライアント/森川さん_home/1_分析_森川さん/1_分析データ_森川さん/000_週次自動データツール"

python3 download_reports.py
```

---

## 📋 ログの確認

実行ログは以下の場所に保存されます:

- **標準出力**: `/tmp/gearmix-seo-report-downloader.log`
- **エラー出力**: `/tmp/gearmix-seo-report-downloader-error.log`

```bash
# 標準出力ログを確認
cat /tmp/gearmix-seo-report-downloader.log

# エラーログを確認
cat /tmp/gearmix-seo-report-downloader-error.log
```

---

## 🔄 LaunchAgentの管理

### 停止

```bash
launchctl unload ~/Library/LaunchAgents/com.gearmix.seo.report.downloader.plist
```

### 再起動

```bash
launchctl unload ~/Library/LaunchAgents/com.gearmix.seo.report.downloader.plist
launchctl load ~/Library/LaunchAgents/com.gearmix.seo.report.downloader.plist
```

### 削除

```bash
launchctl unload ~/Library/LaunchAgents/com.gearmix.seo.report.downloader.plist
rm ~/Library/LaunchAgents/com.gearmix.seo.report.downloader.plist
```

---

## 🐛 トラブルシューティング

### レポートがダウンロードされない

1. **ログを確認**
   ```bash
   cat /tmp/gearmix-seo-report-downloader.log
   cat /tmp/gearmix-seo-report-downloader-error.log
   ```

2. **手動実行でテスト**
   ```bash
   python3 download_reports.py
   ```

3. **ターゲットディレクトリの確認**
   - ダウンロード先ディレクトリが存在するか確認
   - 書き込み権限があるか確認

### LaunchAgentが動作しない

1. **LaunchAgentが読み込まれているか確認**
   ```bash
   launchctl list | grep gearmix
   ```

2. **plistファイルの構文エラーを確認**
   ```bash
   plutil -lint ~/Library/LaunchAgents/com.gearmix.seo.report.downloader.plist
   ```

3. **再読み込み**
   ```bash
   launchctl unload ~/Library/LaunchAgents/com.gearmix.seo.report.downloader.plist
   launchctl load ~/Library/LaunchAgents/com.gearmix.seo.report.downloader.plist
   ```

---

## ℹ️ 仕様

- **実行頻度**: 毎週月曜日 9:30 AM
- **ダウンロード対象**: GitHubリポジトリ内の最新の週次レポート
- **スキップ**: 既にダウンロード済みのファイルは再ダウンロードしない
- **ログ**: 実行結果は `/tmp/` ディレクトリに保存
