import streamlit as st
import pandas as pd
import os

# 1. 페이지 제목 및 레이아웃 설정
st.set_page_config(page_title="국가 소득 수준 예측 AI", page_icon="🌍", layout="centered")

st.title("🌍 국가 코드 기준 소득 수준 예측 서비스")
st.markdown("3자리 국가 코드를 입력하면, 해당 국가가 속한 지역의 데이터를 기반으로 소득 수준을 예측합니다.")

# 2. 데이터 불러오기 (기존 코드 활용)
@st.cache_data # 데이터를 매번 새로 읽지 않고 캐싱하여 속도를 높입니다.
def load_data():
    path = "./" 
    df = pd.read_csv(os.path.join(path, 'country_codes.csv'))
    return df

try:
    df = load_data()
except Exception as e:
    # 💡 문법 에러가 날 수 있는 잘못된 옵션(class_name)을 제거했습니다.
    st.error(f"데이터 파일을 찾을 수 없습니다. 경로를 확인해주세요. 에러: {e}")
    st.stop()

# ------------------------------------------------------------------

# 3. 사이드바 또는 메인 화면에 입력창 만들기
st.subheader("🔍 국가 조회 및 예측")
target_country = st.text_input("조회할 국가 코드(3자리)를 입력하세요 (예: ABW, AFG, ALB):", max_chars=3)

# 4. 조회 및 예측 로직 실행
if target_country:
    # 대문자 공백 제거 처리
    target_country = target_country.strip().upper()
    
    # 입력한 국가의 정보 찾기
    country_info = df[df['country_code'] == target_country]
    
    if not country_info.empty:
        current_region = country_info['region'].values[0]
        actual_income = country_info['income_group'].values[0]
        
        # 화면 구분선
        st.divider()
        
        # 결과 레이아웃 구성 (좌우 2개 컬럼)
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric(label="입력한 국가 코드", value=target_country)
            st.info(f"📍 **소속 지역:**\n{current_region}")
            
        with col2:
            # 알고리즘 가동: '동일한 지역'에 속한 국가들 필터링
            same_region_df = df[df['region'] == current_region]
            # 주변 국가들의 소득 수준 비율 계산
            income_ratio = same_region_df['income_group'].value_counts(normalize=True)
            # 가장 높은 비율의 소득 수준 선택
            main_income_group = income_ratio.idxmax()
            
            st.metric(label="🔮 AI 예측 소득 수준", value=main_income_group)
            st.success(f"💡 이 지역 국가들의 주된 소득 수준은 **{main_income_group}** 입니다.")

        # 5. 시각적 요소 추가: 해당 지역의 소득 분포 차트 그리기
        st.subheader(f"📊 {current_region} 지역의 소득 수준 분포")
        
        # 스트림릿 내장 바 차트 활용을 위한 데이터 정제
        chart_data = income_ratio.reset_index()
        chart_data.columns = ['소득 수준', '비율']
        
        # 바 차트 출력
        st.bar_chart(data=chart_data, x='소득 수준', y='비율', color="#1f77b4")
        
        # 실제 정답 데이터도 참고용으로 슬쩍 보여주기
        st.caption(f"참고: 이 국가의 실제 등록된 소득 수준은 [{actual_income}] 입니다.")
        
    else:
        st.error(f"❌ '{target_country}'은(는) 존재하지 않는 국가 코드입니다. 대소문자나 코드를 다시 확인해 주세요.")

# 🎯 문제의 원인이었던 맨 밑의 터미널 명령어(git clone 등)들을 완전히 삭제했습니다!
