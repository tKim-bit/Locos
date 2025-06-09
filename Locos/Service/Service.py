import csv
import os
from Data import ShopData

class Service:
    
    def getShopList(self):
        shopList=list()
        csv_path = os.path.join(os.path.dirname(__file__), "../csvfiles/shopData_dummy.csv")
        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile) 
            next(reader)
            for row in reader:
                shop=ShopData(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],
                                row[8],row[9],row[10],row[11],row[12])
                shopList.append(shop)
        return shopList
    
    def searchName(self,shopList,name):
        result=list()
        if not name.strip():
            # 付近の店を出す
            pass
        else:
            result=list()
            for shop in shopList:
                if name in shop.name:
                    result.append(shop)
        return result
    
    def searchKeyword(self,shopList,keyword):
        if len(keyword)==0:
            return shopList
        else:
            result=list()
            for shop in shopList:
                if all(word in shop.keyword for word in keyword):
                    result.append(shop)
            return result
    
    def searchParking(self,shopList,parking):
        result=list()
        for shop in shopList:
            if parking==shop.parking:
                result.append(shop)
        return result
    
    def searchReview(self,shopList,review,only=False):
        result=list()
        for shop in shopList:
            if only:
                if review-0.5<=shop.reviewAvg<=review+0.5:
                    result.append(shop)
            else:
                if review<=shop.reviewAvg:
                    result.append(shop)
        return result