def server_durability(request):
    # ミドルウェアでセットしたデータを取得、無ければデフォルト値を返す
    status = getattr(request, 'defense_status', {'tokens': 5.0, 'capacity': 5.0})
    return {
        'durability': status['tokens'],
        'max_durability': status['capacity']
    }