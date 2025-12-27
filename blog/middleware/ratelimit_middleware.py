from django.http import HttpResponse
from blog.utils.rate_limiter import TokenBucketLimiter

class TokenBucketMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        #メインページへのアクセスのみを制限
        if request.path == '/':
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