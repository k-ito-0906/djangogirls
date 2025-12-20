from django.shortcuts import render, get_object_or_404, redirect # redirectを追加
from .models import Post
from .forms import PostForm # これを追加
from django.utils import timezone

# ...他のビューはそのまま...

def post_new(request):
    if request.method == "POST":
        # 保存ボタンが押されたとき
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        # 最初に見る時（空のフォームを表示）
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})