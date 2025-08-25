import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go

# 페이지 설정
st.set_page_config(
    page_title="개인 운동 계획 생성기",
    page_icon="💪",
    layout="wide"
)

# 운동 데이터베이스
EXERCISES = {
    "cardio": {
        "러닝": {"calories_per_min": 10, "difficulty": "중급", "equipment": "없음"},
        "빠른 걷기": {"calories_per_min": 6, "difficulty": "초급", "equipment": "없음"},
        "자전거": {"calories_per_min": 8, "difficulty": "중급", "equipment": "자전거"},
        "줄넘기": {"calories_per_min": 12, "difficulty": "중급", "equipment": "줄넘기"},
        "수영": {"calories_per_min": 11, "difficulty": "고급", "equipment": "수영장"},
        "계단 오르기": {"calories_per_min": 15, "difficulty": "고급", "equipment": "없음"},
        "댄스": {"calories_per_min": 7, "difficulty": "초급", "equipment": "없음"},
        "하이킹": {"calories_per_min": 9, "difficulty": "중급", "equipment": "없음"}
    },
    "strength": {
        "팔굽혀펴기": {"calories_per_min": 8, "difficulty": "중급", "equipment": "없음", "target": "가슴, 팔"},
        "스쿼트": {"calories_per_min": 9, "difficulty": "초급", "equipment": "없음", "target": "하체"},
        "플랭크": {"calories_per_min": 5, "difficulty": "중급", "equipment": "없음", "target": "코어"},
        "버피": {"calories_per_min": 12, "difficulty": "고급", "equipment": "없음", "target": "전신"},
        "런지": {"calories_per_min": 8, "difficulty": "중급", "equipment": "없음", "target": "하체"},
        "마운틴 클라이머": {"calories_per_min": 10, "difficulty": "고급", "equipment": "없음", "target": "전신"},
        "덤벨 컬": {"calories_per_min": 6, "difficulty": "중급", "equipment": "덤벨", "target": "팔"},
        "데드리프트": {"calories_per_min": 9, "difficulty": "고급", "equipment": "바벨", "target": "등, 하체"},
        "벤치프레스": {"calories_per_min": 7, "difficulty": "고급", "equipment": "벤치", "target": "가슴"},
        "풀업": {"calories_per_min": 10, "difficulty": "고급", "equipment": "풀업바", "target": "등, 팔"}
    },
    "flexibility": {
        "요가": {"calories_per_min": 3, "difficulty": "초급", "equipment": "요가매트"},
        "스트레칭": {"calories_per_min": 2, "difficulty": "초급", "equipment": "없음"},
        "필라테스": {"calories_per_min": 4, "difficulty": "중급", "equipment": "요가매트"},
        "태극권": {"calories_per_min": 3, "difficulty": "중급", "equipment": "없음"}
    }
}

# 앱 제목
st.title("💪 개인 운동 계획 생성기")
st.markdown("### 당신만의 맞춤형 운동 계획을 만들어보세요!")
st.markdown("---")

# 사이드바 - 사용자 정보 입력
st.sidebar.header("📝 개인 정보")

# 기본 정보
name = st.sidebar.text_input("이름", placeholder="홍길동")
age = st.sidebar.slider("나이", 10, 80, 25)
weight = st.sidebar.slider("체중 (kg)", 30, 150, 70)
height = st.sidebar.slider("키 (cm)", 120, 220, 170)

# BMI 계산 및 표시
if height > 0:
    bmi = weight / ((height/100) ** 2)
    bmi_status = ""
    if bmi < 18.5:
        bmi_status = "저체중"
        bmi_color = "blue"
    elif bmi < 25:
        bmi_status = "정상"
        bmi_color = "green"
    elif bmi < 30:
        bmi_status = "과체중"
        bmi_color = "orange"
    else:
        bmi_status = "비만"
        bmi_color = "red"
    
    st.sidebar.markdown(f"**BMI**: {bmi:.1f} (:{bmi_color}[{bmi_status}])")

st.sidebar.markdown("---")

# 운동 목표 및 선호도
st.sidebar.header("🎯 운동 목표")
goal = st.sidebar.selectbox(
    "주요 목표",
    ["체중 감량", "근육 증가", "체력 향상", "건강 유지", "스트레스 해소"]
)

fitness_level = st.sidebar.selectbox(
    "운동 경험",
    ["초보자 (운동 경험 거의 없음)", "초급자 (가끔 운동)", "중급자 (정기적으로 운동)", "고급자 (전문적으로 운동)"]
)

available_time = st.sidebar.slider("일일 운동 가능 시간 (분)", 15, 120, 45)
days_per_week = st.sidebar.slider("주당 운동 일수", 1, 7, 3)

equipment = st.sidebar.multiselect(
    "보유 장비",
    ["덤벨", "바벨", "벤치", "풀업바", "요가매트", "줄넘기", "자전거", "런닝머신"],
    default=["요가매트"]
)

# 메인 화면
col1, col2 = st.columns([2, 1])

with col1:
    st.header("🏋️ 운동 계획 생성")
    
    if st.button("✨ 나만의 운동 계획 생성하기!", type="primary", use_container_width=True):
        # 사용자 정보를 바탕으로 운동 계획 생성
        user_equipment = equipment + ["없음"]  # 맨몸 운동도 포함
        
        # 목표에 따른 운동 비율 설정
        if goal == "체중 감량":
            cardio_ratio, strength_ratio, flexibility_ratio = 0.6, 0.3, 0.1
        elif goal == "근육 증가":
            cardio_ratio, strength_ratio, flexibility_ratio = 0.2, 0.7, 0.1
        elif goal == "체력 향상":
            cardio_ratio, strength_ratio, flexibility_ratio = 0.5, 0.4, 0.1
        elif goal == "건강 유지":
            cardio_ratio, strength_ratio, flexibility_ratio = 0.4, 0.4, 0.2
        else:  # 스트레스 해소
            cardio_ratio, strength_ratio, flexibility_ratio = 0.3, 0.2, 0.5
        
        # 운동 계획 생성
        weekly_plan = []
        for day in range(days_per_week):
            daily_plan = {
                "day": f"Day {day + 1}",
                "exercises": [],
                "total_time": 0,
                "total_calories": 0
            }
            
            remaining_time = available_time
            
            # 유산소 운동 추가
            cardio_time = int(remaining_time * cardio_ratio)
            if cardio_time > 0:
                available_cardio = [ex for ex, info in EXERCISES["cardio"].items() 
                                 if info["equipment"] in user_equipment]
                if available_cardio:
                    cardio_ex = random.choice(available_cardio)
                    daily_plan["exercises"].append({
                        "name": cardio_ex,
                        "type": "유산소",
                        "duration": cardio_time,
                        "calories": cardio_time * EXERCISES["cardio"][cardio_ex]["calories_per_min"]
                    })
                    daily_plan["total_time"] += cardio_time
                    daily_plan["total_calories"] += cardio_time * EXERCISES["cardio"][cardio_ex]["calories_per_min"]
            
            # 근력 운동 추가
            strength_time = int(remaining_time * strength_ratio)
            if strength_time > 0:
                available_strength = [ex for ex, info in EXERCISES["strength"].items() 
                                    if info["equipment"] in user_equipment]
                if available_strength:
                    strength_ex = random.choice(available_strength)
                    daily_plan["exercises"].append({
                        "name": strength_ex,
                        "type": "근력",
                        "duration": strength_time,
                        "calories": strength_time * EXERCISES["strength"][strength_ex]["calories_per_min"]
                    })
                    daily_plan["total_time"] += strength_time
                    daily_plan["total_calories"] += strength_time * EXERCISES["strength"][strength_ex]["calories_per_min"]
            
            # 유연성 운동 추가
            flexibility_time = int(remaining_time * flexibility_ratio)
            if flexibility_time > 0:
                available_flexibility = [ex for ex, info in EXERCISES["flexibility"].items() 
                                       if info["equipment"] in user_equipment]
                if available_flexibility:
                    flexibility_ex = random.choice(available_flexibility)
                    daily_plan["exercises"].append({
                        "name": flexibility_ex,
                        "type": "유연성",
                        "duration": flexibility_time,
                        "calories": flexibility_time * EXERCISES["flexibility"][flexibility_ex]["calories_per_min"]
                    })
                    daily_plan["total_time"] += flexibility_time
                    daily_plan["total_calories"] += flexibility_time * EXERCISES["flexibility"][flexibility_ex]["calories_per_min"]
            
            weekly_plan.append(daily_plan)
        
        # 세션 상태에 저장
        st.session_state.workout_plan = weekly_plan
        st.session_state.user_info = {
            "name": name,
            "goal": goal,
            "fitness_level": fitness_level,
            "bmi": bmi,
            "bmi_status": bmi_status
        }

with col2:
    st.header("📊 운동 정보")
    
    # 운동 강도별 칼로리 소모량 차트
    intensity_data = {
        "운동 종류": ["유산소 (저강도)", "유산소 (고강도)", "근력 운동", "유연성 운동"],
        "칼로리/분": [6, 12, 8, 3]
    }
    
    fig = px.bar(intensity_data, x="운동 종류", y="칼로리/분", 
                 title="운동별 칼로리 소모량", color="칼로리/분")
    fig.update_layout(height=300)
    st.plotly_chart(fig, use_container_width=True)

# 생성된 운동 계획 표시
if 'workout_plan' in st.session_state:
    st.markdown("---")
    st.header(f"🗓️ {st.session_state.user_info['name']}님의 운동 계획")
    
    # 요약 정보
    total_weekly_time = sum(day['total_time'] for day in st.session_state.workout_plan)
    total_weekly_calories = sum(day['total_calories'] for day in st.session_state.workout_plan)
    
    summary_cols = st.columns(4)
    with summary_cols[0]:
        st.metric("🎯 목표", st.session_state.user_info['goal'])
    with summary_cols[1]:
        st.metric("⏱️ 주간 총 시간", f"{total_weekly_time}분")
    with summary_cols[2]:
        st.metric("🔥 주간 소모 칼로리", f"{total_weekly_calories:.0f}kcal")
    with summary_cols[3]:
        st.metric("📈 BMI", f"{st.session_state.user_info['bmi']:.1f}")
    
    # 일별 운동 계획
    st.subheader("📅 주간 운동 스케줄")
    
    plan_cols = st.columns(min(len(st.session_state.workout_plan), 3))
    
    for i, day_plan in enumerate(st.session_state.workout_plan):
        col_idx = i % 3
        with plan_cols[col_idx]:
            with st.container():
                st.markdown(f"### {day_plan['day']}")
                st.markdown(f"**총 시간**: {day_plan['total_time']}분")
                st.markdown(f"**소모 칼로리**: {day_plan['total_calories']:.0f}kcal")
                
                for exercise in day_plan['exercises']:
                    st.markdown(f"""
                    <div style="
                        background-color: #f0f2f6;
                        padding: 10px;
                        border-radius: 5px;
                        margin: 5px 0;
                        border-left: 4px solid #ff6b35;
                    ">
                        <strong>{exercise['name']}</strong> ({exercise['type']})<br>
                        ⏱️ {exercise['duration']}분 | 🔥 {exercise['calories']:.0f}kcal
                    </div>
                    """, unsafe_allow_html=True)
    
    # 주간 통계 차트
    st.subheader("📈 주간 운동 통계")
    
    chart_cols = st.columns(2)
    
    with chart_cols[0]:
        # 일별 칼로리 소모량
        daily_calories = [day['total_calories'] for day in st.session_state.workout_plan]
        daily_labels = [day['day'] for day in st.session_state.workout_plan]
        
        fig_calories = go.Figure(data=go.Bar(x=daily_labels, y=daily_calories))
        fig_calories.update_layout(
            title="일별 칼로리 소모량",
            xaxis_title="요일",
            yaxis_title="칼로리 (kcal)",
            height=400
        )
        st.plotly_chart(fig_calories, use_container_width=True)
    
    with chart_cols[1]:
        # 운동 유형별 시간 분포
        cardio_time = sum(ex['duration'] for day in st.session_state.workout_plan 
                         for ex in day['exercises'] if ex['type'] == '유산소')
        strength_time = sum(ex['duration'] for day in st.session_state.workout_plan 
                           for ex in day['exercises'] if ex['type'] == '근력')
        flexibility_time = sum(ex['duration'] for day in st.session_state.workout_plan 
                              for ex in day['exercises'] if ex['type'] == '유연성')
        
        fig_pie = go.Figure(data=go.Pie(
            labels=['유산소', '근력', '유연성'],
            values=[cardio_time, strength_time, flexibility_time],
            hole=0.4
        ))
        fig_pie.update_layout(title="운동 유형별 시간 분포", height=400)
        st.plotly_chart(fig_pie, use_container_width=True)
    
    # 운동 팁
    st.subheader("💡 운동 팁")
    tips = {
        "체중 감량": [
            "운동 전후 충분한 수분 섭취하기",
            "유산소 운동을 꾸준히 하되, 과도하지 않게",
            "근력 운동으로 기초대사량 높이기"
        ],
        "근육 증가": [
            "운동 후 단백질 섭취하기 (30분 이내)",
            "충분한 휴식과 수면 취하기",
            "점진적으로 운동 강도 높이기"
        ],
        "체력 향상": [
            "꾸준함이 가장 중요!",
            "운동 강도를 단계별로 높이기",
            "다양한 운동으로 지루함 방지"
        ],
        "건강 유지": [
            "무리하지 말고 꾸준히",
            "스트레칭으로 부상 예방하기",
            "즐거운 마음으로 운동하기"
        ],
        "스트레스 해소": [
            "좋아하는 음악과 함께 운동하기",
            "자연 속에서 운동해보기",
            "운동 후 명상이나 요가로 마음 진정하기"
        ]
    }
    
    current_tips = tips.get(st.session_state.user_info['goal'], tips['건강 유지'])
    for tip in current_tips:
        st.success(f"✅ {tip}")
    
    # 계획 저장 및 공유
    st.subheader("💾 계획 관리")
    
    save_cols = st.columns(3)
    with save_cols[0]:
        if st.button("📱 계획 저장하기"):
            st.success("운동 계획이 저장되었습니다!")
    
    with save_cols[1]:
        if st.button("🔄 새 계획 생성"):
            del st.session_state.workout_plan
            st.rerun()
    
    with save_cols[2]:
        # 계획을 데이터프레임으로 변환
        plan_data = []
        for day in st.session_state.workout_plan:
            for exercise in day['exercises']:
                plan_data.append({
                    "요일": day['day'],
                    "운동명": exercise['name'],
                    "운동 유형": exercise['type'],
                    "시간(분)": exercise['duration'],
                    "칼로리": f"{exercise['calories']:.0f}kcal"
                })
        
        df_plan = pd.DataFrame(plan_data)
        st.download_button(
            "📊 Excel로 다운로드",
            df_plan.to_csv(index=False, encoding='utf-8-sig'),
            file_name=f"{name}_workout_plan.csv",
            mime="text/csv"
        )

else:
    st.info("👆 개인 정보를 입력하고 '나만의 운동 계획 생성하기!' 버튼을 클릭해주세요.")

# 운동 데이터베이스 보기
st.markdown("---")
with st.expander("🏃 전체 운동 데이터베이스 보기"):
    st.subheader("💨 유산소 운동")
    cardio_df = pd.DataFrame(EXERCISES["cardio"]).T
    st.dataframe(cardio_df)
    
    st.subheader("💪 근력 운동")
    strength_df = pd.DataFrame(EXERCISES["strength"]).T
    st.dataframe(strength_df)
    
    st.subheader("🧘 유연성 운동")
    flexibility_df = pd.DataFrame(EXERCISES["flexibility"]).T
    st.dataframe(flexibility_df)

# 푸터
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: gray;">
    <p>💪 건강한 생활을 위한 개인 운동 계획 생성기 💪</p>
    <p>⚠️ 운동 전 충분한 준비운동을 하고, 몸에 무리가 가지 않도록 주의하세요!</p>
</div>
""", unsafe_allow_html=True)
