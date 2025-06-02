class UserData:
    """id ユーザーID
    name ユーザーネーム
    password パスワード
    mailadress メールアドレス
    goodList いいねリスト
    reviewList レビューリスト
    bookmarkList ブックマークリスト
    cooponList クーポンリスト
    """
    
    def __init__(self,id=0,name="未設定",password="",mailadress=""):
        self.id=id
        self.name=name
        self.password=password
        self.mailadress=mailadress
        self.goodList=list()
        self.reviewList=list()
        self.bookmarkList=list()
        self.cooponList=list()