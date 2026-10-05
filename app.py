import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
import time

st.set_page_config(page_title="지역별 그룹 지도 시각화", layout="wide")

st.title("🗺️ 지역별 그룹 및 조 관리 & 지도 시각화 웹")
st.markdown("사이드바 또는 아래 표에서 **주소, 그룹, 조, 그룹 수** 등을 직접 수정하면 실시간으로 지도와 통계에 반영됩니다!")

# 1. 초기 28명 데이터 정의 (내장형)
@st.cache_data
def load_data():
    data = [
        {"이름": "김민준", "지역": "중랑구", "주소": "서울특별시 중랑구 상봉동 100-5", "그룹": "그룹1", "조": "조1"},
        {"이름": "이지은", "지역": "중랑구", "주소": "서울특별시 중랑구 면목동 50-2", "그룹": "그룹1", "조": "조2"},
        {"이름": "박서준", "지역": "노원구", "주소": "서울특별시 노원구 상계동 120-1", "그룹": "그룹2", "조": "조1"},
        {"이름": "최유진", "지역": "남양주시", "주소": "경기도 남양주시 다산동 200-3", "그룹": "그룹3", "조": "조1"},
        {"이름": "정도현", "지역": "중랑구", "주소": "서울특별시 중랑구 중화동 45-12", "그룹": "그룹1", "조": "조1"},
        {"이름": "한소희", "지역": "중랑구", "주소": "서울특별시 중랑구 신내동 300-1", "그룹": "그룹1", "조": "조2"},
        {"이름": "오지호", "지역": "중랑구", "주소": "서울특별시 중랑구 망우동 88-4", "그룹": "그룹2", "조": "조1"},
        {"이름": "강서연", "지역": "중랑구", "주소": "서울특별시 중랑구 상봉동 150-2", "그룹": "그룹2", "조": "조2"},
        {"이름": "조민재", "지역": "중랑구", "주소": "서울특별시 중랑구 면목동 11-9", "그룹": "그룹3", "조": "조1"},
        {"이름": "윤서아", "지역": "중랑구", "주소": "서울특별시 중랑구 중화동 77-3", "그룹": "그룹3", "조": "조2"},
        {"이름": "임도윤", "지역": "중랑구", "주소": "서울특별시 중랑구 신내동 12-5", "그룹": "그룹1", "조": "조1"},
        {"이름": "신예은", "지역": "중랑구", "주소": "서울특별시 중랑구 망우동 22-1", "그룹": "그룹1", "조": "조2"},
        {"이름": "권지훈", "지역": "중랑구", "주소": "서울특별시 중랑구 상봉동 90-7", "그룹": "그룹2", "조": "조1"},
        {"이름": "서하윤", "지역": "중랑구", "주소": "서울특별시 중랑구 면목동 33-2", "그룹": "그룹2", "조": "조2"},
        {"이름": "황현우", "지역": "중랑구", "주소": "서울특별시 중랑구 중화동 102-4", "그룹": "그룹3", "조": "조1"},
        {"이름": "안채원", "지역": "중랑구", "주소": "서울특별시 중랑구 신내동 55-8", "그룹": "그룹3", "조": "조2"},
        {"이름": "송민서", "지역": "중랑구", "주소": "서울특별시 중랑구 망우동 14-3", "그룹": "그룹1", "조": "조1"},
        {"이름": "배준호", "지역": "중랑구", "주소": "서울특별시 중랑구 상봉동 65-1", "그룹": "그룹1", "조": "조2"},
        {"이름": "백예린", "지역": "중랑구", "주소": "서울특별시 중랑구 면목동 89-5", "그룹": "그룹2", "조": "조1"},
        {"이름": "유시우", "지역": "중랑구", "주소": "서울특별시 중랑구 중화동 12-1", "그룹": "그룹2", "조": "조2"},
        {"이름": "홍서진", "지역": "노원구", "주소": "서울특별시 노원구 중계동 10-5", "그룹": "그룹3", "조": "조1"},
        {"이름": "문도현", "지역": "노원구", "주소": "서울특별시 노원구 하계동 40-2", "그룹": "그룹3", "조": "조2"},
        {"이름": "양소율", "지역": "노원구", "주소": "서울특별시 노원구 상계동 77-8", "그룹": "그룹1", "조": "조1"},
        {"이름": "손예준", "지역": "남양주시", "주소": "경기도 남양주시 진접읍 100-2", "그룹": "그룹1", "조": "조2"},
        {"이름": "배지아", "지역": "남양주시", "주소": "경기도 남양주시 오남읍 55-1", "그룹": "그룹2", "조": "조1"},
        {"이름": "허도윤", "지역": "남양주시", "주소": "경기도 남양주시 별내동 120-4", "그룹": "그룹2", "조": "조2"},
        {"이름": "남지현", "지역": "남양주시", "주소": "경기도 남양주시 다산동 88-9", "그룹": "그룹3", "조": "조1"},
        {"이름": "심재원", "지역": "남양주시", "주소": "경기도 남양주시 진접읍 33-4", "그룹": "그룹3", "조": "조2"}
    ]
    return pd.DataFrame(data)

if 'df' not in st.session_state:
    st.session_state.df = load_data()

# 2. 사이드바 설정
st.sidebar.header("⚙️ 설정 및 데이터 관리")
num_groups = st.sidebar.slider("전체 그룹 수 설정", min_value=1, max_value=6, value=3)

# 데이터 편집기
st.subheader("📋 참여자 데이터 편집기 (주소, 그룹, 조 수정 가능)")
st.markdown("아래 표에서 내용을 직접 더블클릭하여 수정하거나 행을 추가/삭제할 수 있습니다.")
edited_df = st.data_editor(st.session_state.df, num_rows="dynamic", use_container_width=True)
st.session_state.df = edited_df

# 3. 지오코딩 함수
@st.cache_data
def get_lat_lon(address_list):
    geolocator = Nominatim(user_agent="my_geo_app_v1")
    lats, lons = [], []
    for addr in address_list:
        try:
            location = geolocator.geocode(addr, timeout=5)
            if location:
                lats.append(location.latitude)
                lons.append(location.longitude)
            else:
                lats.append(37.6065)
                lats.append(127.0926)
        except:
            lats.append(37.6065)
            lats.append(127.0926)
        time.sleep(0.5)
    return lats, lons

with st.spinner("주소를 지도 좌표(위도/경도)로 변환 중입니다... 잠시만 기다려주세요."):
    df_mapped = st.session_state.df.copy()
    lats, lons = get_lat_lon(df_mapped['주소'].tolist())
    df_mapped['lat'] = lats
    df_mapped['lon'] = lons

# 4. 지도 시각화
st.subheader("📍 그룹별 인터랙티브 지도 시각화")
color_palette = ['red', 'blue', 'green', 'purple', 'orange', 'darkred', 'darkblue', 'cadetblue']
unique_groups = df_mapped['그룹'].unique()
group_color_map = {group: color_palette[i % len(color_palette)] for i, group in enumerate(unique_groups)}

m = folium.Map(location=[37.6065, 127.0926], zoom_start=12)

for idx, row in df_mapped.iterrows():
    group_name = row['그룹']
    color = group_color_map.get(group_name, 'gray')
    
    popup_text = f"<b>이름:</b> {row['이름']}<br><b>지역:</b> {row['지역']}<br><b>그룹:</b> {row['그룹']} ({row['조']})<br><b>주소:</b> {row['주소']}"
    
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=8,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.7,
        popup=folium.Popup(popup_text, max_width=300),
        tooltip=f"{row['이름']} ({row['그룹']} / {row['조']})"
    ).add_to(m)

st_folium(m, width=1200, height=500)

st.markdown("### 🎨 그룹별 색상 범례")
cols = st.columns(len(unique_groups) if len(unique_groups) > 0 else 1)
for i, group in enumerate(unique_groups):
    col_color = group_color_map[group]
    with cols[i % len(cols)]:
        st.markdown(f"<span style='color:{col_color}; font-size:20px;'>●</span> **{group}**", unsafe_allow_html=True)

st.markdown("### 📊 지역 및 그룹별 현황 요약")
col1, col2 = st.columns(2)
with col1:
    st.markdown("#### 지역별 인원")
    st.write(df_mapped['지역'].value_counts())
with col2:
    st.markdown("#### 그룹별 인원")
    st.write(df_mapped['그룹'].value_counts())
