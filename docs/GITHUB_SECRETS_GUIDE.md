# GitHub Secretsの設定ガイド

このガイドでは、GitHubリポジトリにAPI認証情報を安全に登録する方法を説明します。

---

## 📋 必要なもの

以下のファイル/情報が必要です:

1. ✅ サービスアカウントのJSONキーファイル (例: `gearmix-seo-weekly-autopilot-xxxxx.json`)
2. ✅ GA4プロパティID (例: `123456789`)

これらは [SERVICE_ACCOUNT_GUIDE.md](SERVICE_ACCOUNT_GUIDE.md) と [SETUP_GUIDE.md](SETUP_GUIDE.md) の手順で取得済みのはずです。

---

## 🔐 STEP 1: GitHubリポジトリの設定画面を開く

### 1-1. リポジトリにアクセス

ブラウザで以下のURLを開いてください:

```
https://github.com/oned2424/gearmix-seo-weekly-autopilot
```

### 1-2. Settings タブを開く

リポジトリのページ上部にあるタブから「**Settings**」をクリックしてください。

> **📝 注意**: Settingsタブが表示されない場合、リポジトリの管理者権限がない可能性があります。

---

## 🔑 STEP 2: Secrets and variables 画面を開く

### 2-1. 左側メニューから選択

画面左側のメニューから以下を選択してください:

1. 「**Secrets and variables**」をクリック
2. サブメニューが表示されるので「**Actions**」をクリック

---

## 📝 STEP 3: サービスアカウント認証情報を登録

### 3-1. New repository secret をクリック

画面右上の「**New repository secret**」ボタンをクリックしてください。

### 3-2. JSONファイルの内容をコピー

1. ダウンロードしたJSONキーファイル(例: `gearmix-seo-weekly-autopilot-xxxxx.json`)を**テキストエディタ**で開く
2. ファイルの**全内容**を選択してコピー

JSONファイルの中身は以下のような形式です:

```json
{
  "type": "service_account",
  "project_id": "gearmix-seo-weekly-autopilot",
  "private_key_id": "...",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
  "client_email": "gmx-seo-reporter-bot@...",
  "client_id": "...",
  "auth_uri": "...",
  "token_uri": "...",
  "auth_provider_x509_cert_url": "...",
  "client_x509_cert_url": "..."
}
```

> **⚠️ 重要**: `{` から `}` まで、**全て**をコピーしてください!

### 3-3. Secretを作成

1. **Name** に以下を入力:
   ```
   GMX_SERVICE_ACCOUNT_CREDENTIALS
   ```

2. **Secret** に、先ほどコピーしたJSONファイルの全内容を貼り付け

3. 「**Add secret**」ボタンをクリック

### 3-4. 確認

Secretsのリストに `GMX_SERVICE_ACCOUNT_CREDENTIALS` が表示されていればOKです!

---

## 🔢 STEP 4: GA4プロパティIDを登録

### 4-1. New repository secret をクリック

再度、画面右上の「**New repository secret**」ボタンをクリックしてください。

### 4-2. プロパティIDを入力

1. **Name** に以下を入力:
   ```
   GMX_GA4_PROPERTY_ID
   ```

2. **Secret** に、GA4のプロパティIDを入力 (例: `123456789`)

   > **📝 確認方法**: [SETUP_GUIDE.md](SETUP_GUIDE.md) の「STEP 5-1」を参照

3. 「**Add secret**」ボタンをクリック

### 4-3. 確認

Secretsのリストに以下の2つが表示されていればOKです:

- ✅ `GMX_SERVICE_ACCOUNT_CREDENTIALS`
- ✅ `GMX_GA4_PROPERTY_ID`

---

## ✅ セットアップ完了!

お疲れ様でした!GitHub Secretsの設定が完了しました。

### 次のステップ

これで全ての準備が整いました。次は以下のいずれかを実行してください:

#### オプション1: 手動でテスト実行

1. GitHubリポジトリの「**Actions**」タブを開く
2. 左側のワークフロー一覧から「**GMX Weekly SEO Report Generator**」を選択
3. 右側の「**Run workflow**」ボタンをクリック
4. 「**Run workflow**」を再度クリックして実行

数分後、レポートが `reports/weekly/YYYY-MM-DD/` に生成されます!

#### オプション2: 自動実行を待つ

毎週月曜日の朝9時(JST)に自動的にレポートが生成されます。

---

## ❓ トラブルシューティング

### Q: Secretsが保存できない

A: リポジトリの管理者権限があることを確認してください。

### Q: JSONファイルの内容をコピーしたが、エラーが出る

A: 以下を確認してください:
- `{` から `}` まで全てコピーしたか
- 余計な空白や改行が入っていないか
- JSONファイルが正しいフォーマットか

### Q: プロパティIDがわからない

A: [SETUP_GUIDE.md](SETUP_GUIDE.md) の「STEP 5-1: GA4プロパティIDを確認」を参照してください。

### Q: ワークフローが失敗する

A: GitHubの「Actions」タブでエラーログを確認してください。認証エラーの場合は、Secretsが正しく設定されているか再確認してください。

---

## 🎉 完了!

これで週次SEOレポート自動化ツールのセットアップが完全に完了しました!

毎週月曜日の朝、自動的に最新のSEOレポートが生成されます。

レポートは `reports/weekly/` ディレクトリに保存され、GitHubリポジトリから確認できます。
