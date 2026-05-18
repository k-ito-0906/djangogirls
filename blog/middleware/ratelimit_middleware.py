from django.http import HttpResponse
from blog.utils.rate_limiter import TokenBucketLimiter
from django.shortcuts import redirect

class TokenBucketMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        is_authenticated = request.user.is_authenticated

        #ゲストボタンが押されたときの処理
        if request.GET.get('guest') == 'true':
            request.session['is_guest'] = True
            return redirect('/')
        
        #認証チェック
        if not is_authenticated:
           #ログイン画面等へのアクセスはここではreturnせず，下の制限ロジックへ流す
           if 'welcome' in path or 'admin' in path or 'login' in path or path.startswith('/static/'):
               pass
           elif not request.session.get('is_guest'):
               return redirect('gate_page')

        #静的ファイル(CSSなど)は制限をかけずに通す
        if path.startswith('/static/'):
            return self.get_response(request)

        #コストの判定
        cost = 1.0 #通常の閲覧などは1コスト
        
        if request.method == 'POST':
            if 'login' in path:
                cost = 2.0 #ログイン処理は2コスト
            else:
                cost = 3.0 #記事の作成や編集などは3コスト

        user_ip = request.META.get('REMOTE_ADDR')
        #サイト全体に制限を広げるため，初期設定より少し容量を増やして調整します
        limiter = TokenBucketLimiter(user_ip, capacity = 5.0, rate = 0.5)

        #計算したコストを渡して判定
        if not limiter.is_allowed(cost=cost):
            message = "アクセスが集中しています．数秒待ってください．"
            return HttpResponse(
                message, 
                content_type="text/plain; charset=utf-8",
                status=429
            )
            
        return self.get_response(request)