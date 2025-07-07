import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from streamlit_js_eval import streamlit_js_eval

from Service.Service import Service
from Data.UserData import UserData

def dummydata():
    """
    userDataクラスのインスタンスを作成し、
    cooponListにダミーデータを挿入する関数。
    """
    user = UserData() # userDataクラスのインスタンスを作成

    # cooponListにクーポンを追加
    user.cooponList.append('10%オフ')
    user.cooponList.append('ドリンク1杯無料')

    return user # クーポンが挿入されたuserインスタンスを返す


def main():
    st.title('locos\n-地域のお店発見-')
    screen = st.sidebar.selectbox("", ["ホーム", "クーポン", "ブックマーク"])
    if screen == "ホーム":
        search_button = st.button('詳細条件で検索')
        if search_button:
            searchform()
        get_geolocation()
        st.button('周辺の店舗検索')
        coords = st.session_state.get("geoloc")
        if coords and "latitude" in coords and "longitude" in coords:
            df = pd.DataFrame({"lat": [coords["latitude"]], "lon": [coords["longitude"]]})
            st.map(df)
        else:
            st.write("位置情報を取得してください。")
        if search_button:
            searchform()
    elif screen == "クーポン":
        st.title('クーポン一覧')
        st.text_input("店名検索")
        # dummydata関数を実行し、userDataインスタンスを取得
        user_with_coupons = dummydata()
        display_coupons_simple(user_with_coupons.cooponList)
    elif screen == "ブックマーク":
        st.title('ブックマーク一覧')
        df = pd.read_csv()
        st.dataframe(df, column_config={"shopData":st.column_config.LinkColumn("店名", display_text="http://(.*?)\.locos_app.py")},)

def get_geolocation():
    # JSで現在地取得
    coords = streamlit_js_eval(
        js_expressions=
        """
        new Promise((resolve, reject) => {
            navigator.geolocation.watchPosition(
                pos => {resolve({latitude: pos.coords.latitude,
                                longitude: pos.coords.longitude});},
                err => reject(err),
                { enableHighAccuracy: true }
        );
    });
    """,
    key="get_location")
    
    st.session_state['geoloc'] = coords
    
    # 現在地が取得できたら店情報を表示
    if coords and "latitude" in coords and "longitude" in coords:
        service = Service()
        fullShopList = service.getShopList()  # 既存の詳細付きデータ
        result = service.get_nearby_places(coords["latitude"], coords["longitude"], shopList=fullShopList)
        st.write("付近の店:")
        for shop in result:
            st.markdown(f"- **{shop.name}**（{shop.adress}）")
    else:
        st.write("位置情報の取得を許可してください。")


def searchform():
    keyword=st.text_input('キーワード検索')
    shopname=st.text_input('店名検索',help="正確な店名を入力してください")
    st.header("評価で絞り込み")
    min_review = st.number_input(
        '最低評価値',
        min_value=1.0,  # 最小許容値
        max_value=5.0,  # 最大許容値
        value=None,     # 初期値をNoneに設定 (何も入力されていない状態)
        step=0.1,       # 0.1刻みで入力可能
        help='1.0から5.0の間の数字を入力してください。空欄の場合、最低評価は適用されません。',
        format="%.1f"   # 小数点以下1桁で表示
    )
    max_review = st.number_input(
        '最大評価値',
        min_value=1.0,  # 最小許容値
        max_value=5.0,  # 最大許容値
        value=None,     # 初期値をNoneに設定 (何も入力されていない状態)
        step=0.1,       # 0.1刻みで入力可能
        help='1.0から5.0の間の数字を入力してください。空欄の場合、最大評価は適用されません。',
        format="%.1f"   # 小数点以下1桁で表示
    )
    parking=st.checkbox('駐車場有')
    
    search_button = st.button('この条件で検索')

def searchform():
    keyword=st.text_input('キーワード検索')
    shopname=st.text_input('店名検索',help="正確な店名を入力してください")
    st.header("評価で絞り込み")
    min_review = st.number_input(
        '最低評価値',
        min_value=1.0,  # 最小許容値
        max_value=5.0,  # 最大許容値
        value=None,     # 初期値をNoneに設定 (何も入力されていない状態)
        step=0.1,       # 0.1刻みで入力可能
        help='1.0から5.0の間の数字を入力してください。空欄の場合、最低評価は適用されません。',
        format="%.1f"   # 小数点以下1桁で表示
    )
    max_review = st.number_input(
        '最大評価値',
        min_value=1.0,  # 最小許容値
        max_value=5.0,  # 最大許容値
        value=None,     # 初期値をNoneに設定 (何も入力されていない状態)
        step=0.1,       # 0.1刻みで入力可能
        help='1.0から5.0の間の数字を入力してください。空欄の場合、最大評価は適用されません。',
        format="%.1f"   # 小数点以下1桁で表示
    )
    parking=st.checkbox('駐車場有')
    
    search_button = st.button('この条件で検索')
    if search_button:
        shopList=list()
        shopList=Service.getShopList()
        shopList=Service.searchName(shopList,)
        disp_shopList()

def disp_shopList(shopList=list()):
    for shopData in shopList:
        st.write(shopData.name)


def display_coupons_simple(coupons):
    """
    クーポン一覧をシンプルなテキストで表示するメソッド。

    Args:
        coupons (list): クーポン名のリスト。例: ["500円OFFクーポン", "送料無料クーポン"]
    """
    if coupons:
        for i, coupon in enumerate(coupons):
            st.write(f"- {coupon}")
    else:
        st.info("現在利用可能なクーポンはありません。")

    

main()
