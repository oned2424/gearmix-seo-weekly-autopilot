# セットアップガイド

このガイドでは、週次SEOレポート自動化ツールを動かすために必要なAPI認証情報の取得方法を説明します。

---

## 📋 必要なもの

1. Googleアカウント
2. Google Search Consoleへのアクセス権限(gearmix.co.jpの所有者または権限保持者)
3. Google Analytics 4へのアクセス権限
4. GitHubアカウント(既に作成済み)

---

## 🔑 STEP 1: Google Cloud Projectの作成

### 1-1. Google Cloud Consoleにアクセス

1. [Google Cloud Console](https://console.cloud.google.com/)にアクセス
2. Googleアカウントでログイン

### 1-2. 新規プロジェクトを作成

1. 画面上部の「プロジェクトを選択」をクリック
2. 「新しいプロジェクト」をクリック
3. プロジェクト名を入力: `gearmix-seo-reporter`
4. 「作成」をクリック

> **📝 メモ**: プロジェクトIDが自動生成されます。後で使用するのでメモしておいてください。

---

## 🔌 STEP 2: APIの有効化

### 2-1. Search Console APIを有効化

1. 左側メニューから「APIとサービス」→「ライブラリ」を選択
2. 検索ボックスに「Search Console API」と入力
3. 「Google Search Console API」をクリック
4. 「有効にする」をクリック

### 2-2. Google Analytics Data APIを有効化

1. 同じく「ライブラリ」画面で「Google Analytics Data API」を検索
2. 「Google Analytics Data API」をクリック
3. 「有効にする」をクリック

---

## 🎫 STEP 3: サービスアカウントの作成

### 3-1. サービスアカウントを作成

1. 左側メニューから「APIとサービス」→「認証情報」を選択
2. 「認証情報を作成」→「サービスアカウント」をクリック
3. 以下の情報を入力:
   - **サービスアカウント名**: `gmx-seo-reporter-bot`
   - **サービスアカウントID**: `gmx-seo-reporter-bot` (自動入力)
   - **説明**: `週次SEOレポート自動生成用のサービスアカウント`
4. 「作成して続行」をクリック
5. ロールの選択画面では何も選択せず「続行」をクリック
6. 「完了」をクリック

### 3-2. JSONキーをダウンロード

1. 作成したサービスアカウント(`gmx-seo-reporter-bot@...`)をクリック
2. 「キー」タブを選択
3. 「鍵を追加」→「新しい鍵を作成」をクリック
4. 「JSON」を選択して「作成」をクリック
5. JSONファイルが自動的にダウンロードされます

> **⚠️ 重要**: このJSONファイルは秘密情報です。安全な場所に保管し、絶対にGitHubにコミットしないでください!

### 3-3. サービスアカウントのメールアドレスをコピー

ダウンロードしたJSONファイルを開き、`client_email`の値をコピーしてください。

例:
```
gmx-seo-reporter-bot@gearmix-seo-reporter.iam.gserviceaccount.com
```

このメールアドレスは次のステップで使用します。

---

## 🔗 STEP 4: Search Consoleへのアクセス権限付与

### 4-1. Search Consoleにアクセス

1. [Google Search Console](https://search.google.com/search-console)にアクセス
2. `gearmix.co.jp`のプロパティを選択

### 4-2. サービスアカウントにアクセス権限を付与

1. 左側メニューから「設定」をクリック
2. 「ユーザーと権限」をクリック
3. 「ユーザーを追加」をクリック
4. STEP 3-3でコピーしたサービスアカウントのメールアドレスを入力
5. 権限レベルで「フル」を選択
6. 「追加」をクリック

---

## 📊 STEP 5: Google Analytics 4へのアクセス権限付与

### 5-1. GA4プロパティIDを確認

1. [Google Analytics](https://analytics.google.com/)にアクセス
2. gearmix.co.jpのプロパティを選択
3. 左下の「管理」(歯車アイコン)をクリック
4. 「プロパティ設定」をクリック
5. 「プロパティID」をコピー(例: `123456789`)

> **📝 メモ**: このプロパティIDは後でGitHub Secretsに登録します。

### 5-2. サービスアカウントにアクセス権限を付与

1. 「管理」画面で「プロパティのアクセス管理」をクリック
2. 右上の「+」ボタンをクリック
3. 「ユーザーを追加」を選択
4. STEP 3-3でコピーしたサービスアカウントのメールアドレスを入力
5. 役割で「閲覧者」を選択
6. 「追加」をクリック

---

## 🔐 STEP 6: GitHub Secretsの設定

### 6-1. GitHubリポジトリにアクセス

1. https://github.com/oned2424/gearmix-seo-weekly-autopilot にアクセス
2. 「Settings」タブをクリック
3. 左側メニューから「Secrets and variables」→「Actions」を選択

### 6-2. サービスアカウント認証情報を登録

1. 「New repository secret」をクリック
2. 以下の情報を入力:
   - **Name**: `GMX_SERVICE_ACCOUNT_CREDENTIALS`
   - **Secret**: STEP 3-2でダウンロードしたJSONファイルの**全内容**をコピー&ペースト
3. 「Add secret」をクリック

### 6-3. GA4プロパティIDを登録

1. 再度「New repository secret」をクリック
2. 以下の情報を入力:
   - **Name**: `GMX_GA4_PROPERTY_ID`
   - **Secret**: STEP 5-1で確認したプロパティID(例: `123456789`)
3. 「Add secret」をクリック

---

## ✅ セットアップ完了チェックリスト

以下の項目が全て完了していることを確認してください:

- [ ] Google Cloud Projectを作成した
- [ ] Search Console APIを有効化した
- [ ] Google Analytics Data APIを有効化した
- [ ] サービスアカウントを作成した
- [ ] サービスアカウントのJSONキーをダウンロードした
- [ ] Search Consoleにサービスアカウントのアクセス権限を付与した
- [ ] GA4にサービスアカウントのアクセス権限を付与した
- [ ] GA4プロパティIDを確認した
- [ ] GitHub Secretsに`GMX_SERVICE_ACCOUNT_CREDENTIALS`を登録した
- [ ] GitHub Secretsに`GMX_GA4_PROPERTY_ID`を登録した

---

## 🎉 次のステップ

セットアップが完了したら、次は実装フェーズに進みます!

コードの実装が完了すると、以下のことが自動的に行われます:

1. **毎週月曜日の朝9時**に自動実行
2. **先週のSEOデータ**を自動取得
3. **前週との比較分析**を実行
4. **美しいHTMLレポート**を自動生成
5. **GitHubリポジトリ**に自動保存

---

## ❓ トラブルシューティング

### Q: JSONキーのダウンロードに失敗する

A: ブラウザのポップアップブロックを無効にしてから再試行してください。

### Q: Search Consoleにユーザーを追加できない

A: gearmix.co.jpのプロパティに対して「所有者」権限があることを確認してください。

### Q: GA4プロパティIDが見つからない

A: 正しいGA4プロパティを選択しているか確認してください。UA(ユニバーサルアナリティクス)ではなく、GA4のプロパティである必要があります。

### Q: GitHub Secretsが保存できない

A: リポジトリの管理者権限があることを確認してください。
