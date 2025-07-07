class ShopData:
    """ name 店名
        adress 住所
        tell 電話番号
        openTime 営業時間
        closeDay 定休日
        parking 駐車場有無
        keyword キーワード(リスト)
        imagList 画像リスト
        cooponList クーポンリスト
        checkCnt 閲覧数
        reviewSum 評価合計数
        reviewAvg 評価平均
        SNSLink SNSリンク(dict)
        pageLink ページのリンク
        lat 緯度
        lng 軽度
        """

    def __init__(self,name="未設定",adress="未設定",tell="未設定",openTime="未設定",
                 closeDay="未設定",parking="未設定",keyword=list(),imagList=list(),
                 cooponList=list(),checkCnt=0,reviewSum=0,reviewCnt=0,reviewAvg="-",
                 SNSLink=dict(),pageLink="",lat=0,lng=0):
        self.name=name
        self.adress=adress
        self.tell=tell
        self.openTime=openTime
        self.closeDay=closeDay
        self.parking=parking
        self.keyword=keyword
        self.imagList=imagList
        self.cooponList=cooponList
        self.checkCnt=checkCnt
        self.reviewSum=reviewSum
        self.reviewCnt=reviewCnt
        self.reviewAvg=reviewAvg
        self.SNSLink=SNSLink
        self.pageLink=pageLink
        self.lat=lat
        self.lng=lng
        
    def appendImg(self,imgPathList):
        for imgPath in imgPathList:
            self.imagList.append(imgPath)

    def delImg(self,imgPathList):
        for imgPath in imgPathList:
            self.imagList.remove(imgPath)
            
    def checked(self):
        self.checkCnt+=1
    
    def reviewed(self,point):
        self.reviewCnt+=1
        self.reviewSum+=point
        if self.reviewCnt>0:
            self.reviewAvg=self.reviewSum/self.reviewCnt
