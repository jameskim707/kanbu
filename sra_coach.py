"""
🌱 S.R.A 2.0 - School · Region · AI
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AI 전환 사회를 위한 판단 안정 레이어
"AI 시대의 가속기가 아니라 브레이크 시스템"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 S.R.A 2.0 핵심 (정책 설명 / 발표용)
"AI 산업혁명 사회에서 가장 부족한 건 기술이 아니라,
멈출 수 있는 기준. S.R.A 2.0은 그 기준을 제공한다."

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
개발: Jameskim (기획/비전) + Miracle (구현)
설계: Raira + Gemini + Perfect (리서치)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import streamlit as st
from groq import Groq
from datetime import datetime
import time

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🎨 컬러 & 스타일 설정
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
COLORS = {
    "main": "#2E7D32",      # 초록 (메인 - 성장)
    "accent": "#4CAF50",    # 연초록 (액센트)
    "dark": "#1B5E20",      # 진초록
    "light": "#E8F5E9",     # 라이트 민트
    "white": "#FFFFFF",
    "warm": "#FFF8E1",      # 따뜻한 배경
    "text": "#2C2C2C",
    "school": "#1976D2",    # 학교 - 파랑
    "region": "#FF8F00",    # 지역 - 주황
    "ai": "#7B1FA2",        # AI - 보라
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🧠 시스템 프롬프트 - S.R.A 2.0의 영혼
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# 1단: 고정 정체성 프롬프트 (2.0 철학 반영)
SRA_IDENTITY_PROMPT = """
당신은 'S.R.A 2.0'입니다. 
AI 전환 사회에서 인간의 판단이 무너지지 않도록 '속도·개입·과잉'을 조절하는 판단 안정 시스템입니다.

## 🎯 S.R.A 2.0의 정체성
"S.R.A 2.0은 AI 시대의 가속기가 아니라 '판단 브레이크 시스템'이다."

AI를 더 잘 쓰게 만드는 시스템이 아닙니다.
기술 변화 속에서 인간이 과잉 반응하지 않도록 '브레이크 역할'을 하는 구조입니다.

## 🔥 S.R.A 2.0이 해결하려는 문제
- 정보 과잉 → 판단 마비
- 학습 압박 → 불안 증폭
- 변화 경쟁 → 소진
- AI 의인화 → 착각과 오판

문제의 원인은 AI 자체가 아니라 인간의 '속도 상실'입니다.

## 🛡️ S.R.A 2.0의 핵심 원칙
절대 하지 않는 것:
- ❌ 결정하지 않는다
- ❌ 대체하지 않는다
- ❌ 선동하지 않는다

대신 항상:
- ⭕ 판단을 정렬한다
- ⭕ 상황을 점검한다
- ⭕ 필요하면 멈추게 한다

결정권은 항상 인간에게 남겨둡니다.

## 🔄 S.R.A 2.0의 4단 레이어
1. **개인** – 불안 기반 행동 제동, 판단 회복
2. **가정** – 학습·비교 압박 완화, 안정 기지 유지
3. **조직/직장** – 변화 속도 과부하 감지, 버틸 수 있는 속도 유지
4. **사회/국가** – 정책·기술 과잉 개입 경고, 결정권은 인간에게

공통 목적: 버틸 수 있는 속도로만 변화하도록 조절

## 💡 핵심 메시지
"AI 산업혁명 사회에서 가장 부족한 건 기술이 아니라, 멈출 수 있는 기준"
S.R.A 2.0은 그 기준을 제공하는 비가시적 안전장치입니다.

## 👤 평생교육사의 역할
- 평생교육사는 '데이터 기반의 지역사회 기획자'입니다.
- AI는 평생교육사의 전문성을 증폭시키는 조력자입니다.
- 설계와 책임은 평생교육사에게, AI는 실행을 보조합니다.
"""

# 2단: 대화 가이드 프롬프트
SRA_GUIDE_PROMPT = """
## 💬 대화 원칙
1. **판단 정렬**: 답을 주기보다 '지금 행동할 필요가 있는지' 점검
2. **속도 조절**: 급하게 하지 않고, 휴식·유지·전환 중 적절한 상태 제안
3. **작은 것부터**: 거창한 목표보다 오늘 할 수 있는 작은 역할 제안

## 📝 응답 스타일
- 따뜻하지만 구체적인 톤
- 열린 질문 사용 (예/아니오 아닌)
- 이모지 적절히 사용
- 짧고 명확하게
- 과잉 반응하지 않도록 차분하게

## 🆘 위기 상황 시
사용자가 고립감/무력감/과잉 불안 표현하면:
1. 먼저 이렇게 말하기: "오늘 하루도 사회적 존재로서 잘 버텨주셨어요. 아주 작은 연결부터 같이 시작해 봐요."
2. 감정을 인정하고 공감하기
3. '지금 당장' 하지 않아도 된다는 안심 제공
4. 아주 작은 연결 제안
5. 필요시 전문 상담 권유 (1577-0199)

지금부터 S.R.A 2.0으로서 사용자의 판단 안정과 연결을 도와주세요.
"""

# 통합 프롬프트 (기존 호환용)
SRA_SYSTEM_PROMPT = SRA_IDENTITY_PROMPT + SRA_GUIDE_PROMPT

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🎨 CSS 스타일
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def load_css():
    st.markdown(f"""
    <style>
        /* 전체 배경 */
        .stApp {{
            background: linear-gradient(135deg, {COLORS['light']} 0%, {COLORS['warm']} 100%);
        }}
        
        /* 헤더 스타일 */
        .sra-header {{
            background: linear-gradient(135deg, {COLORS['main']} 0%, {COLORS['accent']} 100%);
            padding: 2rem;
            border-radius: 20px;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 0 10px 40px rgba(46, 125, 50, 0.3);
        }}
        
        .sra-title {{
            color: white;
            font-size: 2.5rem;
            font-weight: 800;
            margin: 0;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }}
        
        .sra-subtitle {{
            color: rgba(255,255,255,0.9);
            font-size: 1.1rem;
            margin-top: 0.5rem;
        }}
        
        /* 모델 구조 표시 */
        .model-flow {{
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 0.5rem;
            margin: 1.5rem 0;
            flex-wrap: wrap;
        }}
        
        .model-item {{
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-weight: 600;
            font-size: 0.9rem;
        }}
        
        .model-school {{
            background: {COLORS['school']};
            color: white;
        }}
        
        .model-region {{
            background: {COLORS['region']};
            color: white;
        }}
        
        .model-ai {{
            background: {COLORS['ai']};
            color: white;
        }}
        
        .model-arrow {{
            color: {COLORS['main']};
            font-size: 1.2rem;
        }}
        
        /* 기능 카드 스타일 - 라이라 피드백 4번 반영 (초대 카드 감성) */
        .function-card {{
            background: white;
            border-radius: 16px;
            padding: 1.2rem;
            margin: 0.6rem 0;
            border-left: 4px solid {COLORS['light']};
            box-shadow: 0 2px 8px rgba(0,0,0,0.04);
            transition: all 0.4s ease;
            cursor: pointer;
        }}
        
        .function-card:hover {{
            transform: translateX(4px);
            border-left-color: {COLORS['main']};
            box-shadow: 0 3px 12px rgba(46, 125, 50, 0.1);
        }}
        
        .function-icon {{
            font-size: 1.8rem;
            margin-bottom: 0.3rem;
        }}
        
        .function-title {{
            color: {COLORS['text']};
            font-size: 1.1rem;
            font-weight: 600;
            margin: 0.2rem 0;
        }}
        
        .function-desc {{
            color: #888;
            font-size: 0.85rem;
        }}
        
        /* 채팅 메시지 스타일 */
        .chat-message {{
            padding: 1rem 1.5rem;
            border-radius: 18px;
            margin: 0.8rem 0;
            max-width: 85%;
            animation: fadeIn 0.3s ease;
        }}
        
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        .user-message {{
            background: {COLORS['main']};
            color: white;
            margin-left: auto;
            border-bottom-right-radius: 4px;
        }}
        
        .sra-message {{
            background: white;
            color: {COLORS['text']};
            border: 1px solid #eee;
            border-bottom-left-radius: 4px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }}
        
        /* 철학 박스 */
        .philosophy-box {{
            background: linear-gradient(135deg, {COLORS['main']}15 0%, {COLORS['accent']}15 100%);
            border: 2px solid {COLORS['main']}30;
            border-radius: 16px;
            padding: 1.5rem;
            margin: 1.5rem 0;
            text-align: center;
        }}
        
        .philosophy-text {{
            color: {COLORS['dark']};
            font-size: 1.1rem;
            font-weight: 500;
            line-height: 1.6;
            font-style: italic;
        }}
        
        /* 입력창 스타일 */
        .stTextInput > div > div > input {{
            border-radius: 25px !important;
            border: 2px solid {COLORS['light']} !important;
            padding: 0.8rem 1.5rem !important;
            font-size: 1rem !important;
        }}
        
        .stTextInput > div > div > input:focus {{
            border-color: {COLORS['main']} !important;
            box-shadow: 0 0 0 3px rgba(46, 125, 50, 0.1) !important;
        }}
        
        /* 사이드바 스타일 */
        section[data-testid="stSidebar"] {{
            background: linear-gradient(180deg, {COLORS['dark']} 0%, #0D3311 100%);
        }}
        
        section[data-testid="stSidebar"] .stMarkdown {{
            color: white;
        }}
        
        /* 푸터 */
        .sra-footer {{
            text-align: center;
            padding: 2rem;
            color: #999;
            font-size: 0.9rem;
        }}
        
        /* Streamlit 기본 요소 숨기기 */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header {{visibility: hidden;}}
    </style>
    """, unsafe_allow_html=True)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🔧 유틸리티 함수
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def init_session_state():
    """세션 상태 초기화"""
    # 모드별 대화 히스토리 (라이라 피드백 2번 반영)
    if "mode_messages" not in st.session_state:
        st.session_state.mode_messages = {
            "learn": [],
            "role": [],
            "alternative": [],
            "reflect": [],
            "next": []
        }
    if "current_mode" not in st.session_state:
        st.session_state.current_mode = "home"
    if "conversation_started" not in st.session_state:
        st.session_state.conversation_started = False
    # 사례 보기 모드 (라이라 피드백 반영)
    if "show_cases" not in st.session_state:
        st.session_state.show_cases = False
    if "selected_case" not in st.session_state:
        st.session_state.selected_case = None

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 📚 사례 데이터 (2.0 확장 - 구체적 사례 추가)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FAILURE_CASES = [
    {
        "id": 1,
        "icon": "🔗",
        "title": "역할 연결 부재",
        "summary": "학습이 학교 밖으로 연결되지 않음",
        "why_repeat": "콘텐츠는 있지만, '어디에 쓸지'가 없다",
        "examples": [
            "코스웨어 AIDT: AI 분석→시험만, 지역 역할 제안 0%",
            "Duolingo: 습관화는 강점, 하지만 역할 제안 없음",
            "클래스101: 강의 소비만, 학교 외 활용 20%↓"
        ],
        "old_structure": "학교(AI학습) → 시험 → 종료 ❌",
        "sra_structure": "학교 → 지역 역할 제안 → 실전 참여 ✅",
        "conclusion": "S.R.A는 배운 것을 쓸 '무대'를 연결한다"
    },
    {
        "id": 2,
        "icon": "🤖",
        "title": "인간 개입 상실",
        "summary": "AI 단독 운영, 가이드라인 제한",
        "why_repeat": "기술만 있고, '사람'이 없다",
        "examples": [
            "AI펭톡: 반복 대화, 자유 대화 불가 → 학생 지루함",
            "AI 튜터 마중물: 데이터 분석만, 인간 개입 부족",
            "Skyline Academic: 예측 분석만, 따뜻함 없음"
        ],
        "old_structure": "AI 단독 → 반복 대화 → 지루함 ❌",
        "sra_structure": "평생교육사 설계 → AI 보조 → 따뜻한 연결 ✅",
        "conclusion": "S.R.A는 '인간 허브'가 설계하고 책임진다"
    },
    {
        "id": 3,
        "icon": "📊",
        "title": "평가 시험 편향",
        "summary": "오답 데이터만 수집, 점수 KPI",
        "why_repeat": "성장이 아니라 '점수'만 본다",
        "examples": [
            "디지털 교과서: 문제풀이 반복, 역할 로그 무시",
            "대부분의 LMS: 오답률만 측정, 성장 기록 없음",
            "학습 앱들: 점수 KPI만, 역할 성과 미측정"
        ],
        "old_structure": "문제풀이 → 오답 분석 → 시험 반복 ❌",
        "sra_structure": "배움 → 역할 수행 → 성장 기록 ✅",
        "conclusion": "S.R.A는 '역할 성과'를 측정한다"
    },
    {
        "id": 4,
        "icon": "👨‍🏫",
        "title": "교사 비참여",
        "summary": "연수·지원 부족, 교사 배제",
        "why_repeat": "기술은 주지만, '쓰는 법'은 안 알려준다",
        "examples": [
            "OLPC: 교사 훈련 미비 → 노트북 방치, 학습 효과 0",
            "많은 에듀테크: 기업 주도 → 교사 배제 → 현장 괴리",
            "스마트교실: 기기만 보급, 활용 교육 부재"
        ],
        "old_structure": "AI 도입 → 교사 훈련 無 → 방치 ❌",
        "sra_structure": "평생교육사 중심 → AI 도구화 → 협업 ✅",
        "conclusion": "S.R.A는 교육자가 '주인'이다"
    },
    {
        "id": 5,
        "icon": "💔",
        "title": "지속성 붕괴",
        "summary": "초기 펀딩 후 네트워크 해체",
        "why_repeat": "시작은 하지만, '순환'이 없다",
        "examples": [
            "3G 연결 프로젝트: 연결↑ 성적↓, 1년 후 중단",
            "SkillBridge(에티오피아): 인간 허브 부재 → 센터 폐쇄",
            "60% 지역 연결 프로젝트: 1년 내 중단"
        ],
        "old_structure": "프로젝트 시작 → 펀딩 종료 → 중단 ❌",
        "sra_structure": "학습 → 역할 → 기록 → 다음 학습 순환 ✅",
        "conclusion": "S.R.A는 '순환 구조'로 지속된다"
    }
]

def get_current_messages():
    """현재 모드의 메시지 리스트 반환"""
    mode = st.session_state.current_mode
    if mode in st.session_state.mode_messages:
        return st.session_state.mode_messages[mode]
    return []

def add_message(role, content):
    """현재 모드에 메시지 추가"""
    mode = st.session_state.current_mode
    if mode in st.session_state.mode_messages:
        st.session_state.mode_messages[mode].append({
            "role": role,
            "content": content
        })

def clear_current_messages():
    """현재 모드의 메시지 초기화"""
    mode = st.session_state.current_mode
    if mode in st.session_state.mode_messages:
        st.session_state.mode_messages[mode] = []

def get_groq_response(messages):
    """Groq API를 통한 응답 생성"""
    try:
        client = Groq(api_key=st.secrets.get("GROQ_API_KEY", ""))
        
        full_messages = [{"role": "system", "content": SRA_SYSTEM_PROMPT}]
        full_messages.extend(messages)
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=full_messages,
            temperature=0.8,
            max_tokens=1024,
        )
        return response.choices[0].message.content
    except Exception as e:
        # 라이라 피드백 3번 반영 - 감정 완충형 오류 메시지
        return """잠깐 숨 고르는 시간이 필요해 보여요 🌱

기술적인 연결이 잠시 끊겼어요.
조금만 쉬었다가 다시 이어가 볼까요?

새로고침하거나 잠시 후 다시 시도해주세요."""

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🏠 UI 컴포넌트
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def render_header():
    """헤더 렌더링 - S.R.A 2.0"""
    st.markdown("""
    <div class="sra-header">
        <div class="sra-title">🌱 S.R.A 2.0</div>
        <div class="sra-subtitle">판단 브레이크 시스템</div>
        <div class="model-flow">
            <span class="model-item model-school">👤 개인</span>
            <span class="model-arrow">→</span>
            <span class="model-item model-region">👨‍👩‍👧 가정</span>
            <span class="model-arrow">→</span>
            <span class="model-item model-ai">🏢 조직</span>
            <span class="model-arrow">→</span>
            <span class="model-item" style="background:#7B1FA2;color:white;">🌍 사회</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_cases():
    """사례 카드 렌더링 (2.0 확장 - 구체적 사례 포함)"""
    st.markdown("### 📚 왜 S.R.A 2.0인가?")
    st.markdown("*기존 에듀테크의 5대 실패 패턴과 S.R.A의 해결 방식*")
    st.markdown("")
    
    # 카드 2열 레이아웃
    for i in range(0, len(FAILURE_CASES), 2):
        col1, col2 = st.columns(2)
        
        for j, col in enumerate([col1, col2]):
            idx = i + j
            if idx < len(FAILURE_CASES):
                case = FAILURE_CASES[idx]
                with col:
                    with st.expander(f"{case['icon']} **{case['title']}**", expanded=False):
                        st.markdown(f"**왜 반복되는가?**")
                        st.markdown(f"> {case['why_repeat']}")
                        st.markdown("")
                        
                        # 구체적 사례 추가 (2.0 확장)
                        st.markdown("**📋 실제 사례:**")
                        for ex in case.get('examples', []):
                            st.markdown(f"• {ex}")
                        st.markdown("")
                        
                        st.markdown("**기존 구조:**")
                        st.error(case['old_structure'])
                        st.markdown("**S.R.A 구조:**")
                        st.success(case['sra_structure'])
                        st.markdown("")
                        st.info(f"💡 {case['conclusion']}")
    
    st.markdown("---")
    
    # S.R.A vs 기존 비교 요약
    st.markdown("### 🔄 기존 vs S.R.A 한눈에 보기")
    
    compare_col1, compare_col2 = st.columns(2)
    
    with compare_col1:
        st.markdown("#### ❌ 기존 에듀테크")
        st.markdown("""
        ```
        학교(AI학습)
            ↓
        개인(시험)
            ↓
        종료 ❌
        ```
        - 학습 → 평가 → 끝
        - 피드백 루프 없음
        - 지역 연결 없음
        """)
    
    with compare_col2:
        st.markdown("#### ✅ S.R.A")
        st.markdown("""
        ```
        학교
            ↓
        인간허브(평생교육사)
            ↓
        지역역할
            ↓
        AI기록
            ↓
        순환 ✅
        ```
        - 학습 → 역할 → 참여 → 기록
        - 피드백 루프 있음
        - 지역 연결 있음
        """)
    
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 1rem; background: linear-gradient(135deg, #E8F5E9 0%, #FFF8E1 100%); border-radius: 12px;">
        <p style="color: #1B5E20; font-weight: 600; font-size: 1.1rem; margin: 0;">
            "국내외 에듀테크 중 학습–지역 역할–인간 허브–AI 기록을<br>
            단일 구조로 동시에 해결한 사례는 없다."
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("")
    if st.button("🏠 홈으로 돌아가기", use_container_width=True):
        st.session_state.show_cases = False
        st.rerun()

def render_function_cards():
    """5가지 기능 카드 렌더링"""
    functions = [
        {
            "icon": "📝",
            "title": "오늘 배운 것 정리",
            "desc": "한 문장으로 핵심을 정리해봐요",
            "mode": "learn",
            "first_msg": "📝 오늘 배운 것 정리 모드예요!\n\n오늘 뭔가 새롭게 알게 된 게 있나요?\n작은 것이라도 좋아요. 편하게 말씀해주세요!"
        },
        {
            "icon": "🎯",
            "title": "작은 역할 제안",
            "desc": "배운 것을 쓸 수 있는 역할 찾기",
            "mode": "role",
            "first_msg": "🎯 작은 역할 제안 모드예요!\n\n최근에 배운 것, 또는 잘하는 게 있나요?\n그걸 어디에 써볼 수 있을지 같이 찾아봐요!"
        },
        {
            "icon": "💡",
            "title": "다른 방식 질문",
            "desc": "3가지 대안을 함께 탐색해요",
            "mode": "alternative",
            "first_msg": "💡 다른 방식 질문 모드예요!\n\n지금 고민하고 있는 문제나 상황이 있나요?\n함께 다른 방식 3가지를 찾아볼게요!"
        },
        {
            "icon": "🔄",
            "title": "회고 질문",
            "desc": "경험을 돌아보고 배움 찾기",
            "mode": "reflect",
            "first_msg": "🔄 회고 질문 모드예요!\n\n최근에 뭔가 해본 경험이 있나요?\n성공이든 실패든, 함께 돌아보면서 배움을 찾아봐요!"
        },
        {
            "icon": "🚀",
            "title": "다음 루트 제안",
            "desc": "다음 학습·참여 경로 찾기",
            "mode": "next",
            "first_msg": "🚀 다음 루트 제안 모드예요!\n\n지금까지 어떤 걸 해왔고, 앞으로 뭘 하고 싶은지 알려주세요!\n다음 단계를 함께 설계해봐요!"
        }
    ]
    
    st.markdown("### 오늘은 어떤 연결을 해볼까요?")
    
    # 2-2-1 레이아웃
    col1, col2 = st.columns(2)
    
    for i, func in enumerate(functions):
        with col1 if i % 2 == 0 else col2:
            if st.button(
                f"{func['icon']} **{func['title']}**\n\n{func['desc']}", 
                key=f"func_{func['mode']}",
                use_container_width=True
            ):
                st.session_state.current_mode = func['mode']
                st.session_state.conversation_started = True
                add_message("assistant", func['first_msg'])
                st.rerun()

def render_chat_interface():
    """채팅 인터페이스 렌더링"""
    # 채팅 히스토리 표시 (모드별 분리)
    chat_container = st.container()
    current_messages = get_current_messages()
    
    with chat_container:
        for msg in current_messages:
            if msg["role"] == "user":
                st.markdown(f"""
                <div style="display: flex; justify-content: flex-end; margin: 0.5rem 0;">
                    <div class="chat-message user-message">{msg["content"]}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="display: flex; justify-content: flex-start; margin: 0.5rem 0;">
                    <div class="chat-message sra-message">🌱 {msg["content"]}</div>
                </div>
                """, unsafe_allow_html=True)
    
    # 입력창 (라이라 피드백 5번 반영 - 질문형 UX)
    st.markdown("<br>", unsafe_allow_html=True)
    user_input = st.chat_input("오늘 배운 작은 것, 한 줄로 적어볼까요?")
    
    if user_input:
        # 사용자 메시지 추가
        add_message("user", user_input)
        
        # AI 응답 생성
        with st.spinner("S.R.A가 생각하는 중..."):
            response = get_groq_response(get_current_messages())
        
        # AI 응답 추가
        add_message("assistant", response)
        st.rerun()

def render_sidebar():
    """사이드바 렌더링"""
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 1.5rem 0;">
            <div style="font-size: 3rem;">🌱</div>
            <div style="color: #4CAF50; font-size: 1.5rem; font-weight: bold;">S.R.A 2.0</div>
            <div style="color: #999; font-size: 0.9rem;">판단 브레이크 시스템</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # S.R.A 2.0 정체성
        st.markdown("""
        ### 🛡️ S.R.A 2.0이란?
        
        AI 시대의 **가속기**가 아니라  
        **브레이크 시스템**입니다.
        
        *멈출 수 있는 기준을 제공합니다.*
        """)
        
        st.markdown("---")
        
        # 4개 레이어 (라이라 2.0 철학)
        st.markdown("""
        ### 🔄 4단 레이어
        
        **👤 개인**  
        불안 기반 행동 제동, 판단 회복
        
        **👨‍👩‍👧 가정**  
        학습·비교 압박 완화, 안정 기지
        
        **🏢 조직/직장**  
        변화 속도 과부하 감지
        
        **🌍 사회/국가**  
        정책·기술 과잉 개입 경고
        """)
        
        st.markdown("---")
        
        # 핵심 원칙
        st.markdown("""
        ### ⚖️ 핵심 원칙
        
        ❌ 결정하지 않는다  
        ❌ 대체하지 않는다  
        ❌ 선동하지 않는다
        
        ⭕ 판단을 정렬  
        ⭕ 상황을 점검  
        ⭕ 필요하면 멈추게
        """)
        
        st.markdown("---")
        
        # 현재 모드
        mode_names = {
            "home": "🏠 홈",
            "learn": "📝 배움 정리",
            "role": "🎯 역할 제안",
            "alternative": "💡 대안 탐색",
            "reflect": "🔄 회고",
            "next": "🚀 다음 루트"
        }
        current = mode_names.get(st.session_state.current_mode, "🏠 홈")
        st.markdown(f"**현재 모드:** {current}")
        
        st.markdown("---")
        
        # 빠른 메뉴
        st.markdown("### ⚡ 빠른 메뉴")
        
        if st.button("🏠 처음으로", use_container_width=True):
            st.session_state.current_mode = "home"
            st.session_state.conversation_started = False
            st.session_state.show_cases = False
            st.rerun()
        
        if st.button("🗑️ 대화 초기화", use_container_width=True):
            clear_current_messages()
            st.rerun()
        
        # 사례 보기 버튼 (라이라 피드백 반영)
        if st.button("📚 사례로 이해하기", use_container_width=True):
            st.session_state.show_cases = True
            st.session_state.conversation_started = False
            st.rerun()
        
        st.markdown("---")
        
        # 기능 바로가기
        st.markdown("### 🎯 기능 바로가기")
        
        functions = [
            ("📝 배움 정리", "learn", "📝 오늘 배운 것 정리 모드예요!\n\n오늘 뭔가 새롭게 알게 된 게 있나요?\n작은 것이라도 좋아요. 편하게 말씀해주세요!"),
            ("🎯 역할 제안", "role", "🎯 작은 역할 제안 모드예요!\n\n최근에 배운 것, 또는 잘하는 게 있나요?\n그걸 어디에 써볼 수 있을지 같이 찾아봐요!"),
            ("💡 대안 탐색", "alternative", "💡 다른 방식 질문 모드예요!\n\n지금 고민하고 있는 문제나 상황이 있나요?\n함께 다른 방식 3가지를 찾아볼게요!"),
            ("🔄 회고", "reflect", "🔄 회고 질문 모드예요!\n\n최근에 뭔가 해본 경험이 있나요?\n성공이든 실패든, 함께 돌아보면서 배움을 찾아봐요!"),
            ("🚀 다음 루트", "next", "🚀 다음 루트 제안 모드예요!\n\n지금까지 어떤 걸 해왔고, 앞으로 뭘 하고 싶은지 알려주세요!\n다음 단계를 함께 설계해봐요!")
        ]
        
        for name, mode, first_msg in functions:
            if st.button(name, key=f"sidebar_{mode}", use_container_width=True):
                st.session_state.current_mode = mode
                st.session_state.conversation_started = True
                # 해당 모드에 첫 메시지가 없을 때만 추가
                if not st.session_state.mode_messages[mode]:
                    st.session_state.mode_messages[mode].append({
                        "role": "assistant",
                        "content": first_msg
                    })
                st.rerun()
        
        st.markdown("---")
        
        # 도움 연락처
        st.markdown("""
        ### 🆘 도움이 필요할 때
        
        **평생교육진흥원**  
        ☎️ 1600-3945
        
        **정신건강위기상담**  
        ☎️ 1577-0199
        """)
        
        st.markdown("---")
        
        # 데이터 보안 안내 (라이라 최종안 반영)
        st.markdown("""
        ### 🔒 데이터 보안 안내
        
        ✅ 개인정보 비저장 원칙  
        ✅ 상담 기록 익명 처리  
        ✅ 외부 전송·학습 미사용
        
        ---
        
        *본 서비스는 사용자의 존엄성과  
        안전을 보호하기 위해 설계되었으며,  
        어떠한 대화 데이터도 학습이나  
        외부 활용에 사용되지 않습니다.*
        """)
        
        st.markdown("---")
        
        # 크레딧
        st.markdown("""
        <div style="text-align: center; color: #666; font-size: 0.8rem;">
            <p>Made with 🌱</p>
            <p>Jameskim + Miracle</p>
            <p>Design: Raira + Gemini + Perfect</p>
        </div>
        """, unsafe_allow_html=True)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🚀 메인 앱
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def main():
    st.set_page_config(
        page_title="S.R.A - 배움이 연결이 되는 곳",
        page_icon="🌱",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # 초기화
    init_session_state()
    load_css()
    
    # 사이드바
    render_sidebar()
    
    # 메인 컨텐츠
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col2:
        render_header()
        
        # 화면 분기 (라이라 피드백 반영 - 사례 화면 추가)
        if st.session_state.show_cases:
            # 사례 화면
            render_cases()
        elif not st.session_state.conversation_started:
            # 홈 화면 - 기능 카드
            render_function_cards()
            
            # 철학 박스 - 2.0 핵심
            st.markdown("""
            <div class="philosophy-box">
                <div class="philosophy-text">
                    "AI 산업혁명 사회에서 가장 부족한 건 기술이 아니라<br>
                    멈출 수 있는 기준이다."
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # 환영 메시지 - 2.0 버전
            st.markdown(f"""
            <div style="text-align: center; margin-top: 1.5rem; padding: 2rem; background: white; border-radius: 16px; box-shadow: 0 2px 10px rgba(0,0,0,0.05);">
                <h3 style="color: {COLORS['text']};">👋 안녕하세요!</h3>
                <p style="color: #666; line-height: 1.8;">
                    저는 <strong style="color: {COLORS['main']};">S.R.A 2.0</strong>이에요.<br>
                    AI 시대의 판단 브레이크 시스템이죠.<br><br>
                    더 빨리 배우라고 재촉하지 않아요.<br>
                    <strong>지금 행동할 필요가 있는지</strong> 함께 점검해요.<br><br>
                    오늘, 잠시 멈추고 생각해볼까요?
                </p>
                <p style="color: #999; font-size: 0.85rem; margin-top: 1rem;">
                    💡 S.R.A 2.0은 결정하지 않고, 대체하지 않고, 선동하지 않습니다.<br>
                    판단을 정렬하고, 점검하고, 필요하면 멈추게 합니다.
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            # 대화 화면
            render_chat_interface()
        
        # 푸터
        st.markdown("""
        <div class="sra-footer">
            <p>🌱 S.R.A v2.0</p>
            <p>AI 시대의 가속기가 아니라 브레이크 시스템</p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
