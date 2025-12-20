# Django Girls Blog App

Djangoを利用したシンプルなブログアプリケーションです。
大学での学習および、Webエンジニアとしての長期インターン獲得を目指したポートフォリオの第一歩として制作しています。

## 概要
プログラミング未経験者向けのチュートリアル「Django Girls」をベースに、Web開発の基本概念（MVTモデル、認証、CRUD操作）を実装しました。

## 実装済み機能
- **記事一覧・詳細表示**: データベースから投稿記事を取得し、一覧および個別ページで表示
- **記事の投稿・編集機能**: ログインユーザー専用の投稿・編集フォームの実装
- **認証・セキュリティ**: 
    - Django標準の認証システムを利用したログイン機能
    - デコレータ（@login_required）による未ログインユーザーのアクセス制限
    - CSRF対策等のセキュリティ設定
- **レスポンシブデザイン**: Bootstrap 5 を使用したモバイル対応のレイアウト

## 使用技術
- **Language**: Python 3.13.3
- **Framework**: Django 6.0
- **Database**: SQLite3
- **Frontend**: HTML5, CSS3, Bootstrap 5, Google Fonts
- **Version Control**: Git / GitHub

## 環境構築・実行方法
1. リポジトリをクローンまたはダウンロード
2. 仮想環境の作成と起動
   ```bash
   python3 -m venv myvenv
   source myvenv/bin/activate
3. パッケージのインストール
   pip install django
4. マイグレーションの実行
   python manage.py migrate
5. サーバーの起動
   python manage.py runserver