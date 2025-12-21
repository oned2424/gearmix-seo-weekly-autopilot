# GearMix 週次SEOレポート自動化ツール

gearmix.co.jpの週次SEOパフォーマンスを自動分析・レポート生成するツールです。

## 🎯 機能

- **自動データ取得**: Google Search Console & Google Analytics 4からデータを自動取得
- **前週比較分析**: Week over Week(WoW)での変化を自動計算
- **日本語レポート**: 美しいHTMLレポートを日本語で生成
- **Executive Summary**: データに基づく要約と改善提案を自動生成
- **GitHub Actions**: 毎週月曜日朝9時に自動実行

## 📊 取得データ

### Google Search Console
- 検索クエリ別のクリック数、表示回数、CTR、平均掲載順位
- デバイス別、ページ別のパフォーマンス

### Google Analytics 4
- チャネル別セッション数
- ユーザー数
- ページビュー数

## 🚀 セットアップ

### 1. API認証情報の取得

詳細は [docs/SERVICE_ACCOUNT_GUIDE.md](docs/SERVICE_ACCOUNT_GUIDE.md) を参照してください。

### 2. GitHub Secretsの設定

以下のSecretsをリポジトリに登録してください:

- `GMX_SERVICE_ACCOUNT_CREDENTIALS`: サービスアカウントのJSONキー(全内容)
- `GMX_GA4_PROPERTY_ID`: GA4のプロパティID

### 3. 設定ファイルの編集

`config/gmx_config.yaml`を編集して、サイトURLなどを設定してください。

## 📁 プロジェクト構造

```
gearmix-seo-weekly-autopilot/
├── gmx_seo_reporter/          # メインパッケージ
│   ├── __init__.py
│   ├── clients/               # APIクライアント
│   │   ├── __init__.py
│   │   ├── gsc_client.py     # Search Console API
│   │   └── ga4_client.py     # GA4 API
│   ├── analyzers/             # データ分析
│   │   ├── __init__.py
│   │   └── data_analyzer.py
│   ├── visualizers/           # グラフ生成
│   │   ├── __init__.py
│   │   └── graph_generator.py
│   └── generators/            # レポート生成
│       ├── __init__.py
│       ├── summary_generator.py
│       └── report_builder.py
├── reports/                   # 生成されたレポート
│   └── weekly/
├── assets/                    # 静的ファイル
│   ├── templates/
│   └── styles/
├── config/                    # 設定ファイル
│   └── gmx_config.yaml
├── docs/                      # ドキュメント
│   ├── SETUP_GUIDE.md
│   └── SERVICE_ACCOUNT_GUIDE.md
├── .github/
│   └── workflows/
│       └── weekly-report.yml
├── gmx_weekly_report.py       # メインスクリプト
├── requirements.txt
├── .gitignore
└── README.md
```

## 🔧 使い方

### ローカルで実行

```bash
# 依存関係のインストール
pip install -r requirements.txt

# レポート生成
python gmx_weekly_report.py
```

### GitHub Actionsで自動実行

毎週月曜日の朝9時(JST)に自動実行されます。

手動実行する場合:
1. GitHubリポジトリの「Actions」タブを開く
2. 「GMX Weekly SEO Report Generator」を選択
3. 「Run workflow」をクリック

## 📈 レポートの見方

生成されたレポートは `reports/weekly/YYYY-MM-DD/` に保存されます。

- `gmx_weekly_report_YYYY-MM-DD.html`: メインレポート
- `gmx_graph_*.png`: 各種グラフ

## 🛠️ 技術スタック

- **Python 3.11**
- **Google API Client**: Search Console & GA4データ取得
- **pandas**: データ分析
- **matplotlib**: グラフ生成
- **Jinja2**: HTMLテンプレート
- **GitHub Actions**: 自動実行

## 📝 ライセンス

Private Project

## 🤝 サポート

問題が発生した場合は、Issueを作成してください。
