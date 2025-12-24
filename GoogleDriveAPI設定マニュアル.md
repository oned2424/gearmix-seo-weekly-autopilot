# Google Drive自動連携設定マニュアル (v2: OAuth版)

以前の方法（サービスアカウント）では容量制限でエラーになったため、**「あなたのアカウントとして」** ツールを動かす新しい方法（OAuth）を設定します。

## 手順1: OAuth同意画面の作成

1. **Google Cloud Console** (https://console.cloud.google.com/) にアクセスし、プロジェクト `gearmix-seo-weekly-autopilot` を選択。
2. 左メニュー「APIとサービス」→「OAuth同意画面」をクリック。
3. **User Type**: 「外部」を選択し、「作成」。
4. **アプリ情報**:
   - アプリ名: `WeeklyReportApp`
   - ユーザーサポートメール: あなたのメールアドレス
   - デベロッパーの連絡先情報: あなたのメールアドレス
   - 「保存して次へ」。
5. **スコープ**: 何もせず「保存して次へ」。
6. **テストユーザー**: 
   - 「+ ADD USERS」をクリック。
   - **あなたのGmailアドレス**を入力して追加。「保存して次へ」。
7. 概要が表示されたら「ダッシュボードに戻る」。
8. **重要**: 「公開ステータス」のところにある「アプリを公開」ボタンを押し、「確認」をクリックして**「本番環境」**にします。

---

## 手順2: 認証情報の作成（OAuth 2.0 クライアントID）

1. 左メニュー「認証情報」をクリック。
2. 「＋ 認証情報を作成」→「OAuth クライアント ID」を選択。
3. **アプリケーションの種類**: 「デスクトップ アプリ」を選択。
4. **名前**: `Desktop Client`（なんでもOK）
5. 「作成」をクリック。
6. **JSONをダウンロード**:
   - 「OAuth クライアントを作成しました」というポップアップが出ます。
   - 「JSON をダウンロード」をクリックして、ファイルを保存してください。
   - ファイル名を `credentials.json` に変更し、このマニュアルと同じフォルダ（`000_週次自動データツール`）に入れてください。

---

## 手順3: トークン（合言葉）の発行

ここが一番の山場です！あなたのPCで認証を行います。

1. **ターミナル**を開きます（Macのスポットライト検索で「Terminal」と入力）。
2. 以下のコマンドを1行ずつコピー＆ペーストして実行してください（パスワードを聞かれたらPCのログインパスワードを入力）。

```bash
cd "/Users/apple/Library/CloudStorage/GoogleDrive-yuma2433@gmail.com/マイドライブ/ObsidianVault/13_クライアント/森川さん_home/1_分析_森川さん/1_分析データ_森川さん/000_週次自動データツール"
pip3 install google-auth-oauthlib
python3 generate_token.py
```

3. 「Please visit this URL to authorize...」というURLが表示されたら、クリックしてブラウザで開きます。
4. あなたのアカウントを選択し、「続行」→「許可」をクリックします。
5. 「The authentication flow has completed.」と出たらブラウザを閉じます。
6. フォルダ内に新しく `token.json` というファイルができているはずです！

---

## 手順4: GitHubへの登録

最後に、作成された `token.json`（合言葉）をGitHubに登録します。

1. `token.json` をメモ帳などで開き、中身を**すべてコピー**します。
2. GitHubのリポジトリページ → 「Settings」 → 「Secrets and variables」 → 「Actions」を開く。
3. 以前登録した `GMX_DRIVE_CREDENTIALS` は削除してください（ゴミ箱アイコン）。
4. 「New repository secret」をクリック。
   - **Name**: `GMX_DRIVE_TOKEN_JSON`
   - **Secret**: コピーした `token.json` の中身を貼り付け。
5. `GMX_DRIVE_FOLDER_ID` はそのままでOKです。

これですべて完了です！
GitHub Actionsを「Re-run」すれば、今度こそあなたのドライブに保存されます。
