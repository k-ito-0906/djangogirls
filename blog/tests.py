from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.cache import cache
from .models import Post
from django.utils import timezone

class BlogAppTests(TestCase):
    def setUp(self):
        # テスト用のユーザーとクライアントを準備
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = Client()
        cache.clear() # テストごとにキャッシュをリセットして影響をなくす

    def test_post_creation(self):
        # 1. データベースのテスト
        post = Post.objects.create(
            author=self.user,
            title='テストタイトル',
            text='テスト本文',
            published_date=timezone.now()
        )
        self.assertEqual(post.title, 'テストタイトル')

    def test_gate_page_redirect(self):
        # 2. 画面表示のテスト（未ログイン時はゲートページへ誘導されるか）
        response = self.client.get('/')
        self.assertRedirects(response, '/welcome/', target_status_code=200)

    def test_rate_limit(self):
        # 3. トラフィック制限のテスト
        # ゲストとしてセッションを持たせてトップページへアクセス可能にする
        session = self.client.session
        session['is_guest'] = True
        session.save()
        
        # 容量5.0，1アクセス1.0コストの場合，6回目のアクセスで429エラーになるか
        for _ in range(5):
            response = self.client.get('/')
            self.assertEqual(response.status_code, 200)
            
        # 6回目のアクセス
        response_limited = self.client.get('/')
        self.assertEqual(response_limited.status_code, 429)