from django.http import JsonResponse
from blog.utils.rate_limiter import TokenBucketLimiter

class TokenBucketMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        #post_detailへのアクセスのみを制限
        if request.path.startswith('/post/'):
            user_ip = request.META.get('REMOTE_ADDR')

            limiter = TokenBucketLimiter(user_ip, capacity = 3.0, rate = 0.2)
            if not limiter.is_allowed():
                return JsonResponse(
                    {"status":"error", "message":"アクセスを制限しています。数秒待ってください。"}, 
                    status = 429
                )
            
        return self.get_response(request)