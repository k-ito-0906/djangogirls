from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'), # トップページは views.py の post_list 関数を呼ぶ
]