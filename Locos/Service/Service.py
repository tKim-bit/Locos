import csv
import os
from Data import ShopData

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
                                row[8],row[9],row[10],row[11],row[12])
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
    
    # ここから、位置情報関係
    def get_nearby_places(self, lat, lng, radius=500):
        api_key="";#取得したらここを変える
        url = (
            f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
            f"location={lat},{lng}&radius={radius}&type=store&key={api_key}"
        )
        response = requests.get(url)
        data = response.json()
        results = data.get("results", [])
        return [{"name": place["name"], "address": place["vicinity"]} for place in results]