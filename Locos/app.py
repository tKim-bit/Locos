import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from streamlit_js_eval import streamlit_js_eval

from Service.Service import Service
from Data.UserData import UserData
from Data.ShopData import ShopData # ShopDataをインポート

def dummydata():
    """
    userDataクラスのインスタンスを作成し、
    cooponListにダミーデータを挿入する関数。
    クーポンダミーデータをより詳細な辞書形式で挿入するよう変更。
    """
    user = UserData() # userDataクラスのインスタンスを作成

    # cooponListにクーポンを追加 (ShopDataのインスタンスを格納)
    # 各クーポンは辞書形式で詳細情報を持つ
    shop1 = ShopData(name="カフェ ドリーム", cooponList=[
        {"name": "10%オフクーポン", "conditions": "1回のご利用につき1枚限り有効。", "expiry": "2025年12月31日", "target": "全商品"},
        {"name": "ドリンク1杯無料券", "conditions": "他割引券との併用不可。", "expiry": "2025年11月30日", "target": "全てのドリンク"}
    ])
    shop2 = ShopData(name="パン工房 メロン", cooponList=[
        {"name": "50円引きクーポン", "conditions": "パン300円以上購入で利用可能。", "expiry": "2025年10月15日", "target": "パン"},
        {"name": "ラスクプレゼント券", "conditions": "会計時に提示。", "expiry": "2025年9月30日", "target": "ラスク（小）"}
    ])
    shop3 = ShopData(name="ラーメン 大吉", cooponList=[
        {"name": "麺大盛り無料券", "conditions": "お一人様1回限り。", "expiry": "2026年3月31日", "target": "ラーメン類"}
    ])

    user.cooponList.append(shop1)
    user.cooponList.append(shop2)
    user.cooponList.append(shop3)

    return user # クーポンが挿入されたuserインスタンスを返す


def main():
    st.title('locos\n-地域のお店発見-')
    
    # セッションステートで現在の画面を管理
    if 'screen' not in st.session_state:
        st.session_state['screen'] = "ホーム"
    if 'selected_coupon' not in st.session_state:
        st.session_state['selected_coupon'] = None

    screen_selection = st.sidebar.selectbox("", ["ホーム", "クーポン", "ブックマーク"], key="sidebar_select")
    
    # サイドバーの選択に応じて画面を切り替え
    if screen_selection != st.session_state['screen']:
        st.session_state['screen'] = screen_selection
        st.session_state['selected_coupon'] = None # 画面遷移時に選択中のクーポンをリセット

    if st.session_state['screen'] == "ホーム":
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
    elif st.session_state['screen'] == "クーポン":
        # ここから変更箇所
        if st.session_state['selected_coupon']:
            # クーポンが選択されている場合は詳細画面を表示
            coupon_detail_screen(st.session_state['selected_coupon']['shop_name'], st.session_state['selected_coupon']['coupon_details'])
        else:
            # クーポンが選択されていない場合は一覧表示
            st.title('クーポン一覧')
            shop_name_search = st.text_input("店名でクーポンを検索")
            user_with_coupons = dummydata() # dummydataを呼び出し
            
            filtered_coupons = []
            if shop_name_search:
                for shop in user_with_coupons.cooponList:
                    if shop_name_search.lower() in shop.name.lower():
                        filtered_coupons.append(shop)
            else:
                filtered_coupons = user_with_coupons.cooponList
                
            display_coupons_by_shop(filtered_coupons)
        # ここまで変更箇所
    elif st.session_state['screen'] == "ブックマーク":
        st.title('ブックマーク一覧')
        # ここは元のままでOKですが、read_csv()の引数が必要です
        # df = pd.read_csv("path/to/your/bookmark_data.csv") 
        # st.dataframe(df, column_config={"shopData":st.column_config.LinkColumn("店名", display_text="http://(.*?)\.locos_app.py")},)

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
        result = service.get_nearby_places(coords["latitude"], coords["longitude"], shopList=fullShopList) # 周辺店舗を取得
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
    if search_button:
        shopList=list()
        shopList=Service.getShopList()
        # Service.searchNameの呼び出しに引数が不足している可能性があります。
        # 適切な引数（例: keyword, shopname, min_reviewなど）を渡してください。
        # shopList=Service.searchName(shopList,) 
        disp_shopList(shopList)

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

def display_coupons_by_shop(shops_with_coupons):
    """
    店名とそれに対応するクーポンを一覧で表示するメソッド。
    クーポンをクリック可能なリンクとして表示し、詳細画面へ遷移させる。

    Args:
        shops_with_coupons (list): ShopDataインスタンスのリスト。
                                    各ShopDataにはcooponListが含まれることを想定。
    """
    if shops_with_coupons:
        for shop in shops_with_coupons:
            if shop.cooponList: # shop.cooponList にクーポンがあるか確認
                st.subheader(shop.name) # 店名を表示
                for i, coupon in enumerate(shop.cooponList): # クーポンを列挙
                    # クーポンをボタンとして表示
                    if st.button(f"✨ {coupon['name']}", key=f"coupon_{shop.name}_{i}"): # クーポン名をボタン表示
                        st.session_state['selected_coupon'] = {
                            'shop_name': shop.name,
                            'coupon_details': coupon # クーポンの詳細情報を保存
                        }
                        st.rerun() # 画面を再描画して詳細画面へ遷移
            else:
                st.write(f"{shop.name}: 現在利用可能なクーポンはありません。")
    else:
        st.info("現在利用可能なクーポンはありません。")

def coupon_detail_screen(shop_name, coupon_details):
    """
    クーポンの詳細と使用方法を表示する画面。
    Args:
        shop_name (str): クーポンが提供される店舗名。
        coupon_details (dict): クーポンの詳細情報を含む辞書。
                                例: {"name": "10%オフクーポン", "conditions": "...", "expiry": "...", "target": "..."}
    """
    st.title(f"{shop_name} のクーポン詳細")
    st.header(coupon_details['name']) # クーポン名を表示

    st.markdown("---") # 区切り線

    st.subheader("利用条件:")
    st.write(f"- {coupon_details.get('conditions', '情報なし')}") # 利用条件を表示

    st.subheader("有効期限:")
    st.write(f"- {coupon_details.get('expiry', '情報なし')}") # 有効期限を表示

    st.subheader("対象商品:")
    st.write(f"- {coupon_details.get('target', '情報なし')}") # 対象商品を表示

    st.warning("利用時にスタッフにこの画面を提示してください。")

    st.markdown("---") # 区切り線
    
    if st.button("このクーポンを使用する"):
        st.success(f"『{coupon_details['name']}』を使用しました！店舗スタッフにご提示ください。")
        # ここに、クーポン使用履歴の記録や、使用済みフラグの更新などのバックエンド処理を追加できます。

    if st.button("クーポン一覧に戻る"):
        st.session_state['selected_coupon'] = None
        st.rerun() # 画面を再描画してクーポン一覧に戻る


if __name__ == "__main__":
    main()
