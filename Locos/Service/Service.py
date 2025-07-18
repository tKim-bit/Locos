import csv
import os
from Data.ShopData import ShopData

import requests  # 位置情報から店情報を取得するために使用（例: Google Places API）


class Service:
    def getShopList(self):
        shopList=list()
        csv_path = os.path.join(os.path.dirname(__file__), "../csvfiles/shopData_dummy.csv")
        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile) 
            next(reader)
            for row in reader:
                shop=ShopData(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],
                                row[8],row[9],row[10],row[11],row[12],row[13],row[14])
                shopList.append(shop)
        return shopList
    
    def searchName(self,shopList,name,lat,lng):
        result=list()
        if not name.strip():
            # 付近の店を出す（緯度経度が必要）
            result = self.get_nearby_places(lat, lng)
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
    
    def searchReview(self,shopList,revew_min,revew_max):
        result=list()
        for shop in shopList:
            if revew_min==None and revew_max==None:
                result.append(shop)
            elif revew_min==None and revew_max !=None:
                if shop.reviewAvg<=revew_max:
                    result.append(shop)
            elif revew_min !=None and revew_max ==None:
                if revew_min<=shop.reviewAvg:
                    result.append(shop)
            elif revew_min!=None and revew_max!=None:
                if revew_min<=shop.reviewAvg<=revew_max:
                    result.append(shop)
        return result
    
    # ここから、位置情報関係
    def get_nearby_places(self, lat, lng, radius=500, shopList=None):
        api_key = "459bd2c3a10f466e8ec2db677078c5eb"  # ここにGeoapifyのAPIキーを入力
        url = (
            f"https://api.geoapify.com/v2/places?categories=commercial.supermarket,"
            f"commercial.shopping_mall,commercial.convenience&filter=circle:{lng},{lat},{radius}"
            f"&limit=20&apiKey={api_key}"
        )
        response = requests.get(url)
        data = response.json()
        results = data.get("features", [])

        shopDataList = []
        for place in results:
            name = place.get("name", "未設定")
            address = place.get("vicinity", "未設定")

            # shopListから詳細情報を補完（名前一致で検索）
            if shopList is None:
                shopList = self.getShopList()
            matched = next((s for s in shopList if s.name == name), None)

            if matched:
                shopDataList.append(matched)
            else:
                shopDataList.append(ShopData(name=name, adress=address))

        return shopDataList
    
    
    # if coords and "latitude" in coords and "longitude" in coords:
    # service = Service()
    # fullShopList = service.getShopList()  # 既存の詳細付きデータ
    # result = service.get_nearby_places(coords["latitude"], coords["longitude"], shopList=fullShopList)
    # for shop in result:
    #     st.markdown(f"- **{shop.name}**（{shop.adress}）")
