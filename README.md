# Django Blog System with Traffic Control

PythonAnywhereの無料枠（Beginner Plan）という、制限されたインフラリソース下でシステムの可用性を最大化することを目的とした、Djangoブログアプリケーションのプロトタイプです。

## 1. 開発背景と技術的制約

本プロジェクトは、以下の制約を持つ環境へのデプロイを前提に設計されています。

* **シングル・Webワーカー**: 並列リクエスト処理が不可。1つの重い処理や連続アクセスが、全ユーザーのサービス停止（タイムアウト）に直結します。
* **CPU時間制限**: 1日2,000秒を超えるとスロットリングが発生し、レスポンス速度が極端に低下します。
* **外部通信制限**: プロキシ経由の許可リストのみ通信可能。外部Redis等の独自プロトコルを利用したミドルウェアの導入が困難です。

---

## 2. 実装の核心：トラフィック制御

インフラの脆弱性をアプリケーション層のロジックで補完するため、以下の機能を実装しました。

### トークンバケットによる流量制限
`blog/utils/rate_limiter.py` にて、バーストアクセスを許容しつつ定常レートを絞るアルゴリズムを実装しています。

* **アルゴリズム**: 
    $$\text{new\_tokens} = \min(\text{capacity}, \text{tokens}_{\text{current}} + \Delta t \times \text{rate})$$
* **設定**: 1.0 token/sec（補充）、10.0 tokens（最大貯蔵）
* **意図**: 突発的なアクセスによるCPUリソースの枯渇（Tarpit入り）を防止し、最低限の可用性を死守します。

### Middlewareによる階層防御
`TokenBucketMiddleware` により、Viewが実行（DBクエリ発行）される前の段階でリクエストを評価します。

* **429 Too Many Requests**: 制限超過時にDjango本体の処理を走らせず即座にレスポンスを返すことで、サーバー負荷を最小化。
* **セッション管理**: 未認証ユーザーを案内ページ（gate_page）へ強制誘導する多層的なアクセス制御。

### Cache抽象化による状態管理
Redisが使えない制約下で、Djangoの `LocMemCache`（ローカルメモリ）を活用しています。

* **疎結合設計**: 将来的なインフラ移行を見据え、`django.core.cache` を介した抽象化を実施。

---

## 3. 技術スタック

| カテゴリ | 使用技術 |
| :--- | :--- |
| **Backend** | Django (Python 3) |
| **Database** | SQLite3 |
| **Storage/Cache** | LocMemCache (Django Local-memory) |
| **Infrastructure** | PythonAnywhere |

---

## 4. セットアップ

ローカル環境での実行手順は以下の通りです。

```bash
# 依存パッケージのインストール
pip install -r requirements.txt

# データベースのマイグレーション
python manage.py migrate

# 開発サーバーの起動
python manage.py runserver
```
## 5. 公開URL
http://kokiito0906.pythonanywhere.com/