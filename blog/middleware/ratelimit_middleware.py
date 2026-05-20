from django.http import HttpResponse
from blog.utils.rate_limiter import TokenBucketLimiter
from django.shortcuts import redirect
from django.urls import resolve

class TokenBucketMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 変数に情報を整理
        path = request.path
        is_authenticated = request.user.is_authenticated
        
        # ゲストボタンが押されたときの処理
        if request.GET.get('guest') == 'true':
            request.session['is_guest'] = True
            return redirect('/')
        
        # 認証チェック
        try:
            url_name = resolve(path).url_name
        except Exception:
            url_name = None

        allowed_url_names = ['gate_page', 'login']
        is_static_or_admin = path.startswith('/static/') or path.startswith('/admin/')

        if not is_authenticated:
            #ログイン画面等へのアクセスはここではreturnせず，下の制限ロジックへ流す
            if url_name in allowed_url_names or is_static_or_admin:
                pass
            elif not request.session.get('is_guest'):
                return redirect('gate_page')

        # 静的ファイル(CSSなど)は制限をかけずに通す
        if path.startswith('/static/'):
            return self.get_response(request)

        # コストの判定
        cost = 1.0 # 通常の閲覧などは1コスト
        if request.method == 'POST':
            if url_name == 'login':
                cost = 2.0 # ログイン処理は2コスト
            else:
                cost = 3.0 # 記事の作成や編集などは3コスト

        # IPアドレスの正確な取得
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            user_ip = x_forwarded_for.split(',')[0].strip()
        else:
            user_ip = request.META.get('REMOTE_ADDR')

        # サイト全体に制限を広げるため，初期設定より少し容量を増やして調整します
        limiter = TokenBucketLimiter(user_ip, capacity=5.0, rate=0.5)
        is_allowed = limiter.is_allowed(cost=cost)

        # テンプレートに渡すための耐久値ステータスをリクエストに格納
        # 小数点以下を丸めて見やすくします
        request.defense_status = {
            'tokens': round(limiter.current_tokens, 1),
            'capacity': limiter.capacity
        }

        # 計算したコストを渡して判定
        if not is_allowed:
            message = "アクセスが集中しています．数秒待ってください．"
            return HttpResponse(
                message, 
                content_type="text/plain; charset=utf-8",
                status=429
            )
            
        return self.get_response(request)