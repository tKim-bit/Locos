import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from streamlit_javascript import st_javascript
from Service import Service

def main():
    st.title('locos\n-地域のお店発見-')
    screen = st.sidebar.selectbox("", ["ホーム", "クーポン", "ブックマーク"])
    if screen == "ホーム":
        st.button('周辺の店舗検索')
        st.map()
    elif screen == "クーポン":
        st.text_input("店名検索")
    elif screen == "ブックマーク":
        df = pd.DataFrame({"shopData":["http://sample.locos_app.py"],})
        st.dataframe(df, column_config={"shopData":st.column_config.LinkColumn("店名", display_text="http://(.*?)\.locos_app.py")},)

def get_geolocation():
    components.html(
        """
        <script>
        navigator.geolocation.getCurrentPosition(
            function(position){
                console.log("位置情報が取得できました。", );
            },
            function(error) {
                condole.log("位置情報の取得に失敗しました。", error.message)
            }
        )
        </script>
        """,
        height=0
    )
    
    result = st_javascript(
        """
        new Promise((resolve) => {
            window.addEventListener("message", (event) => {
                resolve(event.data);
            }, {once: true});
        });
        """
    )
    
    return result


main()
