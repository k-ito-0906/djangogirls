from django.conf import settings
from django.db import models
from django.utils import timezone

class Post(models.Model): #クラスでテーブルを定義
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) #FREIGNKEYは外部キー制約、CASCADEは連鎖削除
    title = models.CharField(max_length=200)#長さの制限
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)#フォームの空欄を許可、NULLを許可

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title