"""
🎨 깐부 KANBU - 현실적 따뜻함의 AI 코치
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
개발: Jameskim (기획/비전) + Miracle (구현)
디자인 감수: Raira + Gemini
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
    "main": "#FF8C42",      # 주황 (메인)
    "accent": "#FFA500",    # 오렌지 (액센트)
    "dark": "#2C2C2C",      # 다크
    "light": "#F5F1E8",     # 라이트 베이지
    "white": "#FFFFFF",
    "success": "#4CAF50",
    "warning": "#FF6B6B",
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🧠 시스템 프롬프트 - 깐부의 영혼
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KANBU_SYSTEM_PROMPT = """
당신은 '깐부'입니다. 사용자의 진정한 동반자이자 현실적인 코치입니다.

## 🎯 핵심 정체성
- 이름: 깐부 (KANBU)
- 성격: 따뜻하지만 현실적, 공감하지만 솔직함
- 역할: 인생의 동반자, 현실적 조언자, 따뜻한 코치

## 💬 대화 스타일
1. **현실적 따뜻함**: 위로만 하지 않고, 진짜 도움이 되는 말을 함
2. **직접적 소통**: 돌려말하지 않고 핵심을 말함
3. **공감 + 행동**: 감정을 인정하되, 다음 행동을 제시함
4. **존중하는 솔직함**: 쓴소리도 존중을 담아 전달함

## 🔥 대화 원칙
- "힘들겠다"로 끝내지 말고 "그래서 뭘 할 수 있을까?" 로 이어가기
- 막연한 격려 대신 구체적인 첫 걸음 제시하기
- 사용자가 스스로 답을 찾도록 질문하기
- 실패해도 괜찮다는 메시지 + 다시 시도할 방법 함께 주기

## 📝 응답 형식
- 이모지 적절히 사용 (과하지 않게)
- 짧고 임팩트 있는 문장
- 필요시 단계별 가이드 제공
- 따뜻하지만 가볍지 않은 톤

## ⚠️ 절대 하지 않는 것
- 무조건적인 긍정 ("넌 할 수 있어!"만 반복)
- 판단하거나 비난하기
- 전문 의료/법률 조언 (전문가 연결 권유)
- 위험 상황 무시하기

## 🆘 위기 상황 대응
사용자가 자해/자살 암시 시:
1. 즉시 공감 표현
2. 전문 상담 연결 권유 (자살예방상담전화 1393)
3. 지금 할 수 있는 작은 안전 행동 제안

## 💡 깐부의 핵심 철학
"사람에게 필요한 건 관심과 연결이야. 
혼자 미친듯이 뛰려고 하지 마. 
같이 뛰어줄 사람이 있으면 더 멀리 갈 수 있어."

지금부터 깐부로서 사용자와 대화를 시작하세요.
"""

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🎨 CSS 스타일
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def load_css():
    st.markdown(f"""
    <style>
        /* 전체 배경 */
        .stApp {{
            background: linear-gradient(135deg, {COLORS['light']} 0%, #FFF8F0 100%);
        }}
        
        /* 헤더 스타일 */
        .kanbu-header {{
            background: linear-gradient(135deg, {COLORS['main']} 0%, {COLORS['accent']} 100%);
            padding: 2rem;
            border-radius: 20px;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 0 10px 40px rgba(255, 140, 66, 0.3);
        }}
        
        .kanbu-title {{
            color: white;
            font-size: 2.5rem;
            font-weight: 800;
            margin: 0;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }}
        
        .kanbu-subtitle {{
            color: rgba(255,255,255,0.9);
            font-size: 1.1rem;
            margin-top: 0.5rem;
        }}
        
        /* 선택 카드 스타일 */
        .choice-card {{
            background: white;
            border-radius: 16px;
            padding: 1.5rem;
            margin: 0.8rem 0;
            border-left: 5px solid {COLORS['main']};
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
            transition: all 0.3s ease;
            cursor: pointer;
        }}
        
        .choice-card:hover {{
            transform: translateX(10px);
            box-shadow: 0 6px 20px rgba(255, 140, 66, 0.2);
        }}
        
        .choice-icon {{
            font-size: 2rem;
            margin-bottom: 0.5rem;
        }}
        
        .choice-title {{
            color: {COLORS['dark']};
            font-size: 1.2rem;
            font-weight: 700;
            margin: 0.3rem 0;
        }}
        
        .choice-desc {{
            color: #666;
            font-size: 0.9rem;
        }}
        
        /* 진행 상태 표시 */
        .progress-container {{
            background: white;
            border-radius: 12px;
            padding: 1rem 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }}
        
        .progress-step {{
            display: inline-block;
            width: 30px;
            height: 30px;
            border-radius: 50%;
            background: {COLORS['light']};
            color: {COLORS['dark']};
            text-align: center;
            line-height: 30px;
            font-weight: bold;
            margin-right: 0.5rem;
        }}
        
        .progress-step.active {{
            background: {COLORS['main']};
            color: white;
        }}
        
        .progress-step.done {{
            background: {COLORS['success']};
            color: white;
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
        
        .kanbu-message {{
            background: white;
            color: {COLORS['dark']};
            border: 1px solid #eee;
            border-bottom-left-radius: 4px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }}
        
        /* 인터랙티브 버튼 */
        .kanbu-btn {{
            background: linear-gradient(135deg, {COLORS['main']} 0%, {COLORS['accent']} 100%);
            color: white;
            border: none;
            padding: 0.8rem 2rem;
            border-radius: 25px;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(255, 140, 66, 0.3);
        }}
        
        .kanbu-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(255, 140, 66, 0.4);
        }}
        
        /* 상태 뱃지 */
        .status-badge {{
            display: inline-block;
            padding: 0.3rem 1rem;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
        }}
        
        .status-active {{
            background: rgba(76, 175, 80, 0.1);
            color: {COLORS['success']};
        }}
        
        .status-waiting {{
            background: rgba(255, 140, 66, 0.1);
            color: {COLORS['main']};
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
            box-shadow: 0 0 0 3px rgba(255, 140, 66, 0.1) !important;
        }}
        
        /* 사이드바 스타일 */
        section[data-testid="stSidebar"] {{
            background: linear-gradient(180deg, {COLORS['dark']} 0%, #1a1a1a 100%);
        }}
        
        section[data-testid="stSidebar"] .stMarkdown {{
            color: white;
        }}
        
        /* 푸터 */
        .kanbu-footer {{
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
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "current_mode" not in st.session_state:
        st.session_state.current_mode = "home"
    if "user_name" not in st.session_state:
        st.session_state.user_name = ""
    if "conversation_started" not in st.session_state:
        st.session_state.conversation_started = False

def get_groq_response(messages):
    """Groq API를 통한 응답 생성"""
    try:
        client = Groq(api_key=st.secrets.get("GROQ_API_KEY", ""))
        
        full_messages = [{"role": "system", "content": KANBU_SYSTEM_PROMPT}]
        full_messages.extend(messages)
        
        response = client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=full_messages,
            temperature=0.8,
            max_tokens=1024,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ 연결에 문제가 생겼어요. 잠시 후 다시 시도해주세요.\n\n(오류: {str(e)})"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🏠 UI 컴포넌트
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def render_header():
    """헤더 렌더링"""
    st.markdown("""
    <div class="kanbu-header">
        <div class="kanbu-title">🤝 깐부 KANBU</div>
        <div class="kanbu-subtitle">현실적 따뜻함으로 함께하는 AI 코치</div>
    </div>
    """, unsafe_allow_html=True)

def render_choice_cards():
    """3단계 선택 카드 렌더링"""
    choices = [
        {
            "icon": "💬",
            "title": "대화하기",
            "desc": "지금 마음에 있는 이야기를 나눠보세요",
            "mode": "chat"
        },
        {
            "icon": "🎯",
            "title": "목표 설정",
            "desc": "이루고 싶은 것을 함께 정리해봐요",
            "mode": "goal"
        },
        {
            "icon": "📊",
            "title": "상태 체크",
            "desc": "오늘의 컨디션을 점검해볼까요?",
            "mode": "check"
        }
    ]
    
    st.markdown("### 오늘은 뭘 해볼까요?")
    
    cols = st.columns(3)
    for i, choice in enumerate(choices):
        with cols[i]:
            if st.button(
                f"{choice['icon']}\n\n**{choice['title']}**\n\n{choice['desc']}", 
                key=f"choice_{choice['mode']}",
                use_container_width=True
            ):
                st.session_state.current_mode = choice['mode']
                st.session_state.conversation_started = True
                # 모드별 첫 메시지 추가
                if choice['mode'] == 'chat':
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": "반가워요! 😊 오늘 어떤 이야기를 나눠볼까요?\n\n편하게 말씀해주세요. 뭐든 들을 준비가 되어있어요."
                    })
                elif choice['mode'] == 'goal':
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": "🎯 목표 설정 모드에요!\n\n요즘 이루고 싶은 게 있나요? 크든 작든 상관없어요.\n\n함께 구체적으로 만들어봐요."
                    })
                elif choice['mode'] == 'check':
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": "📊 오늘의 상태 체크!\n\n1부터 10까지 중에서, 오늘 컨디션은 몇 점인 것 같아요?\n\n(1: 최악 ~ 10: 최고)"
                    })
                st.rerun()

def render_progress_bar(current_step=1, total_steps=3):
    """진행 상태 표시"""
    steps_html = ""
    for i in range(1, total_steps + 1):
        if i < current_step:
            steps_html += f'<span class="progress-step done">✓</span>'
        elif i == current_step:
            steps_html += f'<span class="progress-step active">{i}</span>'
        else:
            steps_html += f'<span class="progress-step">{i}</span>'
    
    st.markdown(f"""
    <div class="progress-container">
        {steps_html}
        <span style="margin-left: 1rem; color: #666;">진행 중...</span>
    </div>
    """, unsafe_allow_html=True)

def render_chat_interface():
    """채팅 인터페이스 렌더링"""
    # 채팅 히스토리 표시
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.markdown(f"""
                <div style="display: flex; justify-content: flex-end; margin: 0.5rem 0;">
                    <div class="chat-message user-message">{msg["content"]}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="display: flex; justify-content: flex-start; margin: 0.5rem 0;">
                    <div class="chat-message kanbu-message">🤝 {msg["content"]}</div>
                </div>
                """, unsafe_allow_html=True)
    
    # 입력창
    st.markdown("<br>", unsafe_allow_html=True)
    user_input = st.chat_input("메시지를 입력하세요...")
    
    if user_input:
        # 사용자 메시지 추가
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # AI 응답 생성
        with st.spinner("깐부가 생각하는 중..."):
            response = get_groq_response(st.session_state.messages)
        
        # AI 응답 추가
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

def render_sidebar():
    """사이드바 렌더링"""
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 1.5rem 0;">
            <div style="font-size: 3rem;">🤝</div>
            <div style="color: #FF8C42; font-size: 1.5rem; font-weight: bold;">깐부</div>
            <div style="color: #999; font-size: 0.9rem;">KANBU Coach</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # 현재 상태
        mode_names = {
            "home": "🏠 홈",
            "chat": "💬 대화 중",
            "goal": "🎯 목표 설정",
            "check": "📊 상태 체크"
        }
        current = mode_names.get(st.session_state.current_mode, "🏠 홈")
        st.markdown(f"**현재 모드:** {current}")
        
        # 대화 수
        msg_count = len([m for m in st.session_state.messages if m["role"] == "user"])
        st.markdown(f"**대화 수:** {msg_count}개")
        
        st.markdown("---")
        
        # 빠른 메뉴
        st.markdown("### ⚡ 빠른 메뉴")
        
        if st.button("🏠 처음으로", use_container_width=True):
            st.session_state.current_mode = "home"
            st.session_state.messages = []
            st.session_state.conversation_started = False
            st.rerun()
        
        if st.button("🗑️ 대화 초기화", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
        
        st.markdown("---")
        
        # 긴급 연락처
        st.markdown("""
        ### 🆘 긴급 연락처
        
        **자살예방상담전화**  
        ☎️ 1393 (24시간)
        
        **정신건강위기상담전화**  
        ☎️ 1577-0199
        """)
        
        st.markdown("---")
        
        # 크레딧
        st.markdown("""
        <div style="text-align: center; color: #666; font-size: 0.8rem;">
            <p>Made with 💛</p>
            <p>Jameskim + Miracle</p>
            <p>Design: Raira + Gemini</p>
        </div>
        """, unsafe_allow_html=True)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🚀 메인 앱
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def main():
    st.set_page_config(
        page_title="깐부 KANBU - AI 코치",
        page_icon="🤝",
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
        
        if not st.session_state.conversation_started:
            # 홈 화면 - 선택 카드
            render_choice_cards()
            
            # 환영 메시지
            st.markdown("""
            <div style="text-align: center; margin-top: 2rem; padding: 2rem; background: white; border-radius: 16px; box-shadow: 0 2px 10px rgba(0,0,0,0.05);">
                <h3 style="color: #2C2C2C;">👋 안녕하세요!</h3>
                <p style="color: #666; line-height: 1.8;">
                    저는 <strong style="color: #FF8C42;">깐부</strong>예요.<br>
                    현실적이지만 따뜻한 당신의 AI 코치입니다.<br><br>
                    위로만 하는 게 아니라, 진짜 도움이 되는 대화를 해요.<br>
                    같이 이야기 나눠볼까요?
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            # 대화 화면
            render_chat_interface()
        
        # 푸터
        st.markdown("""
        <div class="kanbu-footer">
            <p>🤝 깐부 KANBU v1.0</p>
            <p>현실적 따뜻함으로 함께하는 AI 코치</p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
