from django.shortcuts import render
from .models import Post  # 倉庫(モデル)からPostを呼び出す

def post_list(request):
    # 倉庫から記事を全部取ってくる（QuerySetと言います）
    posts = Post.objects.all() 
    # blog/post_list.html という「お皿」に posts を載せてお客さんに返す
    return render(request, 'blog/post_list.html', {'posts': posts})