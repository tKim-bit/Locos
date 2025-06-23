import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from streamlit_js_eval import st_js_eval

from Service.Service import Service

def main():
    st.title('locos\n-地域のお店発見-')
    screen = st.sidebar.selectbox("", ["ホーム", "クーポン", "ブックマーク"])
    if screen == "ホーム":
        search_button = st.button('詳細条件で検索')
        get_geolocation()
        st.button('周辺の店舗検索')
        st.map(st.session_state.geoloc)
    elif screen == "クーポン":
        st.title('ブックマーク一覧')
        st.text_input("店名検索")
        st.dataframe(df, column_config={"shopData":st.column_config.LinkColumn("店名", )})
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
    st.text(type(coords))
    
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
main()

def get_coupon_list():
    """
    Retrieves and filters the list of available coupons from shop data.
    """
    service = Service()
    all_shops = service.getShopList()

    coupon_data = []
    for shop in all_shops:
        if shop.cooponList and shop.cooponList != "[]": # Check if cooponList is not empty or literal '[]'
            # Assuming cooponList is a string representation of a list, e.g., "['10%オフ', 'ドリンク1杯無料']"
            # We need to parse it. Using ast.literal_eval is safer for actual lists.
            # For this example, let's assume it's just a simple string for now or a proper list.
            try:
                import ast
                coupons = ast.literal_eval(shop.cooponList)
            except (ValueError, SyntaxError):
                coupons = [shop.cooponList] # Treat as a single string if parsing fails

            for coupon in coupons:
                coupon_data.append({
                    "店名": shop.name,
                    "クーポン": coupon,
                    "shopData": shop.pageLink # Storing the link for the LinkColumn
                })

    df_coupons = pd.DataFrame(coupon_data)

    if shop_name_filter:
        df_coupons = df_coupons[df_coupons["店名"].str.contains(shop_name_filter, case=False, na=False)]
    
    return df_coupons
