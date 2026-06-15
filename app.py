import streamlit as st
import pandas as pd
import os

# 1. 페이지 제목 및 레이아웃 설정
st.set_page_config(page_title="국가 소득 수준 예측 AI", page_icon="🌍", layout="centered")

st.title("🌍 국가 코드 기준 소득 수준 예측 서비스")
st.markdown("3자리 국가 코드를 입력하면, 해당 국가가 속한 지역의 데이터를 기반으로 소득 수준을 예측합니다.")

# 2. 데이터 불러오기
@st.cache_data
def load_data():
    path = "./" 
    df = pd.read_csv(os.path.join(path, 'country_codes.csv'))
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"데이터 파일을 찾을 수 없습니다. 경로를 확인해주세요. 에러: {e}")
    st.stop()

# ------------------------------------------------------------------
# ✨ [추가된 기능] 국가 코드 안내 가이드 (접고 펼치기)
# ------------------------------------------------------------------
with st.expander("💡 3자리 국가 코드 목록 확인하기 (클릭해서 열기)"):
    st.markdown("알고 싶은 국가의 3자리 코드를 찾아서 아래 검색창에 입력해 보세요.")
    
    # 깔끔하게 보여주기 위해 정렬 및 컬럼명 변경 후 출력
    guide_df = df[['country_code', 'region']].sort_values(by='country_code').reset_index(drop=True)
    guide_df.columns = ['국가 코드 (Code)', '지역 (Region)']
    
    # 스트림릿 테이블로 출력 (데이터가 많으므로 스크롤이 가능한 dataframe 형태)
    st.dataframe(guide_df, use_container_width=True, height=250)

# ------------------------------------------------------------------

# 3. 사이드바 또는 메인 화면에 입력창 만들기
st.subheader("🔍 국가 조회 및 예측")
target_country = st.text_input("조회할 국가 코드(3자리)를 입력하세요 (예: ABW, AFG, ALB):", max_chars=3)

# 4. 조회 및 예측 로직 실행
if target_country:
    target_country = target_country.strip().upper()
    country_info = df[df['country_code'] == target_country]
    
    if not country_info.empty:
        current_region = country_info['region'].values[0]
        actual_income = country_info['income_group'].values[0]
        
        st.divider()
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric(label="입력한 국가 코드", value=target_country)
            st.info(f"📍 **소속 지역:**\n{current_region}")
            
        with col2:
            same_region_df = df[df['region'] == current_region]
            income_ratio = same_region_df['income_group'].value_counts(normalize=True)
            main_income_group = income_ratio.idxmax()
            
            st.metric(label="🔮 AI 예측 소득 수준", value=main_income_group)
            st.success(f"💡 이 지역 국가들의 주된 소득 수준은 **{main_income_group}** 입니다.")

        st.subheader(f"📊 {current_region} 지역의 소득 수준 분포")
        chart_data = income_ratio.reset_index()
        chart_data.columns = ['소득 수준', '비율']
        st.bar_chart(data=chart_data, x='소득 수준', y='비율', color="#1f77b4")
        st.caption(f"참고: 이 국가의 실제 등록된 소득 수준은 [{actual_income}] 입니다.")
        
    else:
        st.error(f"❌ '{target_country}'은(는) 존재하지 않는 국가 코드입니다. 대소문자나 코드를 다시 확인해 주세요.")
