# backend README

## 概要

団体内で使う SNS（Twitter と Slack を融合したイメージ）を作成することを目的とします。
主な操作は「チャンネルに紐づく短文投稿」と「チャンネルのフォロー／タイムライン表示」「メッセージのスレッド（リプライ）」です。リアルタイム配信（WebSocket）をサポートします。

MVP の方針
- シンプルで導入しやすい実装（FastAPI チュートリアル準拠）
- スケールは小〜中規模を想定（read-time 集約で十分）
- 機能は最小限のモデレーション、JWT 認証、Markdown 対応（表示側で処理）

## 要件（確定）

- チャンネル可視性：`public` / `private`
  - `public`: 誰でも閲覧・投稿可能
  - `private`: 招待されたメンバーのみ閲覧・投稿可能
- 各ユーザーは自分のチャンネルを持つ（デフォルト `public`。後から `private` に変更可能）
- ユーザーは任意の新しいチャンネルを作成可能
- チャンネルをフォローできる
- タイムライン（ホーム）はフォロー中チャンネルの「親メッセージ（parent_id IS NULL）」のみを時系列に表示
  - 各メッセージに reply（リプライ）数を表示
  - スレッドを開くと当該メッセージの全リプライ（ツリー）を取得して表示
- 任意のメッセージに対してリプライ可能（リプライ自体もメッセージ）
- リアルタイム配信（WebSocket）
- メディア添付はフロントで content 中の URL を埋め込む方式
- 絵文字は `:emoji:` 形式をフロントで置換
- メッセージは Markdown 形式で保存（フロントでレンダリング・サニタイズ）
- JWT を認証トークンに採用

## 主なエンティティ（概念）

- User
- Channel
- ChannelMember
- Follow
- Message
- Reaction
- Notification

### 簡潔なフィールド例（実装は SQLModel を想定）

- User: id, username, display_name, password_hash, created_at
- Channel: id, owner_id, slug, name, description, visibility (`public`/`private`), created_at
- ChannelMember: id, channel_id, user_id, role, joined_at
- Follow: id, user_id, channel_id, created_at
- Message: id, channel_id, author_id, parent_id (nullable), thread_root_id (nullable), content (Markdown), reply_count, created_at, updated_at, deleted_at
- Reaction: id, message_id, user_id, type, created_at
- Notification: id, user_id, type, payload (JSON), read_at, created_at

インデックス推奨
- messages: (channel_id, created_at), (thread_root_id, created_at), (parent_id)
- follows: (user_id), (channel_id)
- channel_members: (channel_id, user_id)

## メッセージ／スレッドのルール

- 投稿時
  - parent_id が指定されない：親メッセージ（parent_id = NULL）
  - parent_id がある場合：thread_root_id を設定する
    - 親が root（parent.parent_id == NULL）なら thread_root_id = parent.id
    - 親が reply の場合は parent.thread_root_id を継承
  - 親または thread_root の reply_count をトランザクション内でインクリメント
- タイムライン（ホーム）
  - フォロー中のチャンネルのメッセージのうち parent_id IS NULL のものを created_at DESC で返す
  - 各メッセージに reply_count を含める
- スレッド表示
  - GET /messages/{id}/thread で thread_root_id をキーにスレッド内のメッセージを取得
  - フロントで parent_id を使ってネスト表示を再構築

### 設計上の注意

- parent_id のみだと深い再帰クエリが重くなるため、thread_root_id を持つことで高速にスレッドを取得できるようにする
- reply_count の整合性はトランザクションで担保する

## 認証 / 認可

- 認証方式：JWT（payload に user_id, username, exp など）
- チャンネル閲覧・投稿権限
  - public: 全員閲覧・投稿可能
  - private: channel_members に存在するユーザーのみ閲覧・投稿可能
- 管理操作（チャンネル削除、メンバー管理）は owner / admin のみ

### JWT の例（省略可）

- payload: { "sub": user_id, "username": "...", "exp": <timestamp> }

## API（主要エンドポイント）

API は /api/v1/ プレフィックスを想定。以下は主要なエンドポイント一覧（概要）

### 認証

- POST /api/v1/auth/signup
  - body: { username, email?, password }
  - returns: { access_token: JWT, token_type: "bearer" }
- POST /api/v1/auth/login
  - body: { username, password }
  - returns: { access_token: JWT, token_type: "bearer" }

### ユーザー

- GET /api/v1/users/{user_id}
- GET /api/v1/users/{user_id}/channel

### チャンネル

- POST /api/v1/channels
  - body: { name, slug?, description?, visibility? }  (owner は認証ユーザー)
- GET /api/v1/channels/{channel_id}
- PATCH /api/v1/channels/{channel_id}
- POST /api/v1/channels/{channel_id}/invite
- GET /api/v1/channels/{channel_id}/members

### フォロー

- POST /api/v1/channels/{channel_id}/follow
- DELETE /api/v1/channels/{channel_id}/unfollow
- GET /api/v1/users/{user_id}/follows

### メッセージ

- POST /api/v1/channels/{channel_id}/messages
  - body: { content: string (Markdown), parent_id?: int }
  - 動作: 権限チェック → parent 校正 → thread_root 計算 → insert → reply_count 更新 → WebSocket broadcast
- GET /api/v1/channels/{channel_id}/messages?before=&limit=
  - ここはチャンネル専用のメッセージ取得（既定では parent_id IS NULL のみを返す／オプションで全メッセージも可）
- GET /api/v1/messages/{id}
- GET /api/v1/messages/{id}/thread
  - thread_root をキーにスレッド内メッセージを返す
- PATCH /api/v1/messages/{id}
- DELETE /api/v1/messages/{id}

### タイムライン

- GET /api/v1/timeline/home?limit=&cursor=
  - フォロー中チャンネルの parent_id IS NULL の投稿を cursor-based（created_at, id）で返す

### リアクション・通知

- POST /api/v1/messages/{id}/reactions
- GET /api/v1/notifications

## WebSocket（リアルタイム）

- エンドポイント: `/ws?token=<JWT>`（接続時に JWT で認証）
- クライアント → サーバー: subscribe/unsubscribe（閲覧中の channel を指定）
  - 例: { "type": "subscribe", "channel_id": 123 }
- サーバー → クライアント: イベント送信
  - **閲覧中チャンネル**: 完全なメッセージデータを送信
  - **その他のフォロー中チャンネル**: 軽量通知のみ送信（未読カウント更新用）
  - event types:
    - `new_message`: { message_id, channel_id, author_id, content, created_at, parent_id, thread_root_id, reply_count }
      - 閲覧中チャンネルのみ完全データを送信
    - `channel_activity`: { channel_id, unread_count, last_message_at }
      - フォロー中だが閲覧していないチャンネルの新着通知（軽量）
    - `message_update`, `message_delete`, `reaction_added`, `notification`
- 実装
  - 接続時にユーザーのフォロー中チャンネルリストを取得し、全体を監視対象とする
  - 閲覧中チャンネル（subscribe済み）: 完全なイベントデータを送信
  - その他のフォロー中チャンネル: channel_activity イベントのみ送信
  - 単一インスタンス時はメモリのブロードキャスターで OK
  - 将来マルチインスタンスにする場合は Redis pub/sub に切替（抽象化しておく）

## Markdown / 絵文字 / メディアの扱い

- DB には生の Markdown を保存
- フロントエンドで Markdown → HTML に変換（必ずサニタイズして XSS を防止）
- 絵文字は `:emoji:` 形式をフロントで展開
- 画像／動画等は content 内の URL をフロントで検出して埋め込み表示（バックエンドは必要なら link preview API を提供）

## モデレーション（最小限）

- メッセージ削除（管理者または投稿者）
- ユーザー BAN（管理者）
- メッセージは論理削除（deleted_at）を推奨（追跡・復元が容易）

## DB / マイグレーション

- DB: 開発環境ではSQLite、本番環境ではPostgreSQLを使用
- マイグレーション: alembic を使用
- 初期マイグレーション: models の構造を alembic revision に反映

## テスト

- 単体テスト: models や CRUD ロジック（権限チェック、reply_count 増減）
- 結合テスト: 認証 → チャンネル作成 → 投稿 → フォロー → タイムライン取得
- WebSocket テスト: new_message イベント受信確認
- テストフレームワーク: pytest 推奨

## 実装・ファイル構成（推奨）

- backend/app/models.py  — SQLModel モデル群
- backend/app/schemas.py — Pydantic 入出力スキーマ
- backend/app/crud.py    — DB ロジック（トランザクションを集約）
- backend/app/routers/v1/
  - auth.py, channels.py, messages.py, timeline.py, ws.py
- backend/app/core/
  - config.py（環境変数読み取り）
  - security.py（JWT ヘルパー）
  - broadcaster.py（WS/Redis 抽象化）
- backend/alembic/…      — マイグレーション
- backend/tests/…        — 単体/統合テスト

## トランザクション例（メッセージ投稿の疑似フロー）

1. トランザクション開始
2. parent_id が指定されていれば parent メッセージを読み取り、channel_id の整合性チェック
3. thread_root_id を決定して message を INSERT
4. parent または thread_root の reply_count を UPDATE（+1）
5. トランザクションコミット
6. WebSocket で `new_message` を broadcast

（reply_count の増減はトランザクション内で行い整合性を保ちます）

## 環境変数（例）

- DATABASE_URL=postgresql://user:pass@host:port/dbname
- SECRET_KEY=...
- ACCESS_TOKEN_EXPIRE_MINUTES=60

backend/.env.sample を参照して設定してください。

## 今後の優先タスク（MVP）

1. SQLModel の models.py を作成し、alembic 初期マイグレーションを生成
2. 認証（signup/login → JWT）ルーター実装
3. チャンネル作成・自動ユーザーチャンネル作成・フォロー実装
4. メッセージ投稿（parent/thread_root/reply_count を含む）と関連 API
5. タイムライン（home）クエリ実装（read-time aggregation）
6. WebSocket 基本（接続・subscribe・new_message broadcast）
7. 最小限のテストケース

## 参考（実装時の方針）

- FastAPI チュートリアル（JWT 実装例）に沿う
- SQLModel のチュートリアルに沿った model / session の使い方
- WebSocket は FastAPI の標準機能を使い、Broadcast/Connection 管理は小さなマネージャクラスで抽象化
