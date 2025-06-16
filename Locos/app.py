import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from streamlit_javascript import st_javascript

from Service import Service


def main():
    st.title('locos\n-地域のお店発見-')
    screen = st.sidebar.selectbox("", ["ホーム", "クーポン", "ブックマーク"])
    if screen == "ホーム":
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
    coords = st_javascript(
        """
        navigator.geolocation.getCurrentPosition(
            (position) => {
                const coords = {
                    latitude: position.coords.latitude,
                    longitude: position.coords.longitude
                };
                window.parent.postMessage({type: 'streamlit:setComponentValue', value: coords}, '*')
            }
        );
        """
    )
    
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
