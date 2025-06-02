class Review:
    """img 画像
    text 文章
    point 5段階評価
    user 投稿者
    """
    
    def __init__(self,point,user):
        self.img=""
        self.text=""
        self.point=point
        self.user=user