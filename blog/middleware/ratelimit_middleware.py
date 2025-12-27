from django.http import HttpResponse
from blog.utils.rate_limiter import TokenBucketLimiter
from django.shortcuts import redirect

class TokenBucketMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        #変数に情報を整理
        path = request.path
        is_authenticated = request.user.is_authenticated

        #ゲストボタンが押されたときの処理
        if request.GET.get('guest') == 'true':
            request.session['is_guest'] = True
            return redirect('/')
        
        if not is_authenticated:
           if 'welcome' in path or 'admin' in path or 'login' in path:
              return self.get_response(request)
           
           if not request.session.get('is_guest'):
               return redirect('gate_page')
            
        #メインページへのアクセスのみを制限
        if path == '/':
            user_ip = request.META.get('REMOTE_ADDR')
            limiter = TokenBucketLimiter(user_ip, capacity = 10.0, rate = 1.0)

            if not limiter.is_allowed():
                message =  "アクセスを制限しています。数秒待ってください。"
                return HttpResponse(
                    message, 
                    content_type = "text/plain; charset=utf-8", #イコールの前後にスペースを入れると文字化けした
                    status = 429
                )
            
        return self.get_response(request)