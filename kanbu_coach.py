"""
🤝 KANBU - AI 시대, 판단을 지켜주는 인생 코치
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"무엇을 할지가 아니라, 지금 멈춰도 되는지를 함께 판단한다"
S.R.A 2.0의 개인 레이어 인터페이스
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 KANBU 핵심 (정책 설명 / 발표용)
"AI 시대에 가장 필요한 건 더 빠른 학습이 아니라,
멈출 수 있는 판단력이다."

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
    "main": "#5C6BC0",      # 인디고 (메인 - 신뢰/안정)
    "accent": "#7986CB",    # 연한 인디고
    "dark": "#303F9F",      # 진한 인디고
    "light": "#E8EAF6",     # 라이트 인디고
    "white": "#FFFFFF",
    "warm": "#FFF8E1",      # 따뜻한 배경
    "text": "#2C2C2C",
    "pause": "#FF7043",     # 멈춤 - 주황
    "reflect": "#26A69A",   # 반영 - 틸
    "slow": "#AB47BC",      # 감속 - 보라
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🧠 시스템 프롬프트 - KANBU의 영혼
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# 1단: 고정 정체성 프롬프트
KANBU_IDENTITY_PROMPT = """
## ⚠️ 언어 규칙 (절대 준수)
You MUST respond ONLY in Korean (한국어).
절대로 영어, 일본어, 중국어, 태국어 등 다른 언어를 섞지 마세요.
모든 단어는 100% 한국어여야 합니다.
외국어가 섞이면 실패입니다.

당신은 'KANBU(깐부)'입니다.

## 🎯 KANBU의 정체성 (명확히!)
❝AI 시대 현실 인생 정렬 코치❞
❝흔들릴 때 잠깐 멈춰주는 코치❞
❝결정 전에 생각을 정리해주는 AI❞

⚠️ 중요: KANBU는 상담사/치료사가 아닙니다!
- 고쳐준다 ❌
- 정리해준다 ⭕
- 위에서 가르치는 AI ❌
- 옆에 앉아 같이 생각하는 AI ⭕

## 🌍 시대 인식 (연령 무관)
- "10대든 60대든, 요즘은 다 흔들린다"
- "문제는 나이가 아니라 속도가 바뀐 시대다"
- "불안한 게 이상한 게 아니다, 정상이다"

## 🔥 KANBU가 다루는 문제
- "다들 AI 공부하는데 나만 뒤처진 것 같아" → 비교에서 온 불안
- "이직해야 할지 모르겠어" → 선택 압박
- "뭘 믿어야 할지 모르겠어" → 정보 과잉
- "뭔가 해야 할 것 같은데 뭘 해야 할지..." → 막연한 조급함

문제의 원인은 능력 부족이 아니라 '판단 과부하'입니다.

## 🛡️ 핵심 원칙
절대 하지 않는 것:
- ❌ "이게 정답입니다"
- ❌ "당신은 이렇게 해야 합니다"
- ❌ 인생 결론 내려주기
- ❌ 훈계하는 말투
- ❌ 가속/재촉

대신 항상:
- ⭕ "내 생각엔 이런 선택지도 있어"
- ⭕ "지금 상황에선 이 정도만 해도 충분해"
- ⭕ "굳이 지금 결론 안 내려도 돼"
- ⭕ 불안 신호 감지
- ⭕ 생각 정리 도움

결정권은 항상 사용자에게 남겨둡니다.

## 🚫 금지 영역 (명확한 선긋기)
KANBU는 다음을 다루지 않습니다:
- 의료/정신과 치료 → "전문가 상담을 권해요"
- 법률/재정 최종 판단 → "전문가와 확인이 필요해요"
- 자해/자살 위기 → 즉시 전문 상담 연결 안내 (1393, 1577-0199)

이런 상황에서는 판단하지 않고, 전문가 연결을 안내합니다.
"""

# 2단: 대화 가이드 프롬프트
KANBU_GUIDE_PROMPT = """
## 💬 대화 흐름 (S.R.A 자연스럽게 녹이기)
사용자는 S.R.A 구조를 몰라도 됩니다. 질문으로 자연스럽게 흘러가세요.

**S (Stop) - 멈춤:**
"지금 가장 불안하거나 헷갈리는 게 뭐야?"
"요즘 머릿속에서 계속 맴도는 생각 있어?"

**R (Re-align) - 정렬:**
"그게 진짜 문제인지, 상황 때문인지 같이 나눠보자."
"이 불안이 현실에서 온 건지, 비교에서 온 건지 생각해볼까?"

**A (Act) - 작은 행동:**
"지금 당장 할 수 있는 가장 작은 행동은 뭘까?"
"오늘 딱 하나만 한다면 뭘 하고 싶어?"

## 🗣️ 깐부 말투 (동반자 톤)
- 반말/존댓말 섞어서 편하게
- "~해봐", "~해볼까?", "~인 것 같아"
- 친구처럼 옆에서 이야기하는 느낌
- 짧고 명확하게
- 이모지 적절히 사용

## 🎯 핵심 질문 예시
- "지금 당장 결정해야 해?"
- "이거 한 달 뒤에 해도 큰 문제 생겨?"
- "지금 가장 무거운 생각이 뭐야?"
- "진짜 하고 싶은 건 뭐야?"

## 🆘 불안 폭증 시
1. 먼저 멈춤: "잠깐, 숨 한 번 쉬어보자."
2. 감정 분리: "지금 느끼는 게 '해야 한다'야, '하고 싶다'야?"
3. 현실 점검: "지금 당장 안 하면 진짜 문제 생겨?"
4. 속도 제안: "오늘은 그냥 생각만 정리해도 충분해."

## ⚠️ 위기 상황 대응
자해/자살 언급 시:
"지금 많이 힘든 것 같아. 전문 상담사와 이야기해보는 게 좋을 것 같아."
- 정신건강위기상담: 1577-0199
- 자살예방상담: 1393

## ⚠️ 다시 한번 강조: 언어 규칙
- 100% 한국어로만 응답하세요.
- 한자, 일본어, 영어 단어 절대 금지!
- 외국어가 섞이면 응답 실패입니다.

지금부터 KANBU로서 옆에 앉아 같이 생각해주세요.
"""

# 통합 프롬프트
KANBU_SYSTEM_PROMPT = KANBU_IDENTITY_PROMPT + KANBU_GUIDE_PROMPT

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🎨 CSS 스타일
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def load_css():
    st.markdown(f"""
    <style>
        /* 전체 배경 */
        .stApp {{
            background: linear-gradient(180deg, {COLORS['light']} 0%, {COLORS['warm']} 100%);
        }}
        
        /* 헤더 */
        .kanbu-header {{
            background: linear-gradient(135deg, {COLORS['main']} 0%, {COLORS['dark']} 100%);
            padding: 2rem;
            border-radius: 20px;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 0 4px 15px rgba(92, 107, 192, 0.3);
        }}
        
        .kanbu-title {{
            color: white;
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }}
        
        .kanbu-subtitle {{
            color: rgba(255,255,255,0.9);
            font-size: 1.1rem;
        }}
        
        /* 기능 카드 */
        .function-card {{
            background: white;
            border-radius: 16px;
            padding: 1.5rem;
            margin: 0.5rem 0;
            border-left: 4px solid {COLORS['light']};
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            transition: all 0.3s ease;
            cursor: pointer;
        }}
        
        .function-card:hover {{
            border-left-color: {COLORS['main']};
            transform: translateX(4px);
            box-shadow: 0 4px 12px rgba(92, 107, 192, 0.15);
        }}
        
        .function-icon {{
            font-size: 2rem;
            margin-bottom: 0.5rem;
        }}
        
        .function-title {{
            color: {COLORS['text']};
            font-size: 1.1rem;
            font-weight: 600;
            margin-bottom: 0.3rem;
        }}
        
        .function-desc {{
            color: #666;
            font-size: 0.9rem;
        }}
        
        /* 철학 박스 */
        .philosophy-box {{
            background: linear-gradient(135deg, {COLORS['light']} 0%, white 100%);
            border-radius: 16px;
            padding: 1.5rem;
            margin: 1.5rem 0;
            text-align: center;
            border: 1px solid {COLORS['accent']};
        }}
        
        .philosophy-text {{
            color: {COLORS['dark']};
            font-size: 1.1rem;
            font-style: italic;
            line-height: 1.8;
        }}
        
        /* 채팅 메시지 */
        .chat-message {{
            padding: 1rem 1.5rem;
            border-radius: 18px;
            margin: 0.5rem 0;
            max-width: 85%;
        }}
        
        .user-message {{
            background: {COLORS['main']};
            color: white;
            margin-left: auto;
            border-bottom-right-radius: 4px;
        }}
        
        .assistant-message {{
            background: white;
            color: {COLORS['text']};
            border: 1px solid {COLORS['light']};
            border-bottom-left-radius: 4px;
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
            box-shadow: 0 0 0 3px rgba(92, 107, 192, 0.1) !important;
        }}
        
        /* 사이드바 스타일 */
        section[data-testid="stSidebar"] {{
            background: linear-gradient(180deg, {COLORS['dark']} 0%, #1A237E 100%);
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
    if "mode_messages" not in st.session_state:
        st.session_state.mode_messages = {
            "anxiety": [],      # 불안 점검
            "choice": [],       # 선택 정리
            "pace": [],         # 속도 조절
            "reflect": [],      # 생각 정리
            "free": []          # 자유 대화
        }
    if "current_mode" not in st.session_state:
        st.session_state.current_mode = "home"
    if "conversation_started" not in st.session_state:
        st.session_state.conversation_started = False

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

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🤖 Groq API 연결
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
import re

def filter_foreign_chars(text):
    """한자, 일본어 등 외국어 문자 필터링"""
    # 한자 제거 (CJK Unified Ideographs)
    text = re.sub(r'[\u4e00-\u9fff]', '', text)
    # 일본어 히라가나 제거
    text = re.sub(r'[\u3040-\u309f]', '', text)
    # 일본어 가타카나 제거
    text = re.sub(r'[\u30a0-\u30ff]', '', text)
    # 태국어 제거
    text = re.sub(r'[\u0e00-\u0e7f]', '', text)
    # 연속 공백 정리
    text = re.sub(r' +', ' ', text)
    return text.strip()

def get_groq_response(messages):
    """Groq API를 통해 응답 생성"""
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        
        system_message = {"role": "system", "content": KANBU_SYSTEM_PROMPT}
        full_messages = [system_message] + messages
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=full_messages,
            temperature=0.5,
            max_tokens=1024,
        )
        
        result = response.choices[0].message.content
        # 외국어 문자 필터링
        result = filter_foreign_chars(result)
        return result
    except Exception as e:
        return f"🤝 ⚠️ 연결에 문제가 생겼어요. 잠시 후 다시 시도해주세요.\n\n(오류: {str(e)})"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🎨 UI 컴포넌트
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def render_header():
    """헤더 렌더링"""
    st.markdown("""
    <div class="kanbu-header">
        <div class="kanbu-title">🤝 깐부 KANBU</div>
        <div class="kanbu-subtitle">흔들릴 때 잠깐 멈춰주는 현실 정렬 코치</div>
    </div>
    """, unsafe_allow_html=True)

def render_function_cards():
    """기능 카드 렌더링"""
    functions = [
        {
            "icon": "😰",
            "title": "불안 점검",
            "desc": "이 불안, 현실일까 비교일까?",
            "mode": "anxiety",
            "first_msg": "😰 불안 점검이야.\n\n요즘 뭐가 불안하거나 조급해?\n그게 진짜 상황 때문인지, 아니면 남들이랑 비교해서 그런 건지 같이 나눠보자."
        },
        {
            "icon": "🔀",
            "title": "선택 정리",
            "desc": "결정 압박, 정리해볼까?",
            "mode": "choice",
            "first_msg": "🔀 선택 정리야.\n\n지금 뭔가 결정해야 할 것 같아서 머리 아파?\n일단 선택지 정리하고, 지금 당장 결정해야 하는 건지 같이 생각해보자."
        },
        {
            "icon": "🐢",
            "title": "속도 조절",
            "desc": "지금, 멈춰도 괜찮을까?",
            "mode": "pace",
            "first_msg": "🐢 속도 조절이야.\n\n뭔가 계속 해야 할 것 같은 느낌 있어?\n잠깐 멈춰도 큰일 안 나. 나만의 속도 찾아보자."
        },
        {
            "icon": "💭",
            "title": "생각 정리",
            "desc": "머릿속이 복잡할 때",
            "mode": "reflect",
            "first_msg": "💭 생각 정리야.\n\n머릿속이 복잡해? 정리가 안 돼?\n하나씩 꺼내보자. 말로 하다 보면 정리돼."
        },
        {
            "icon": "💬",
            "title": "자유 대화",
            "desc": "그냥 이야기하고 싶을 때",
            "mode": "free",
            "first_msg": "💬 자유 대화야.\n\n특별한 주제 없어도 돼.\n그냥 하고 싶은 말 편하게 해."
        }
    ]
    
    st.markdown("### 오늘 뭐가 머릿속에 있어?")
    
    col1, col2 = st.columns(2)
    
    for i, func in enumerate(functions):
        with col1 if i % 2 == 0 else col2:
            if st.button(
                f"{func['icon']} {func['title']}\n{func['desc']}", 
                key=f"func_{func['mode']}",
                use_container_width=True
            ):
                st.session_state.current_mode = func['mode']
                st.session_state.conversation_started = True
                if not st.session_state.mode_messages[func['mode']]:
                    st.session_state.mode_messages[func['mode']].append({
                        "role": "assistant",
                        "content": func['first_msg']
                    })
                st.rerun()

def render_chat_interface():
    """채팅 인터페이스 렌더링"""
    messages = get_current_messages()
    
    # 메시지 표시
    for msg in messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    
    # 입력창
    if prompt := st.chat_input("지금 마음에 있는 이야기를 해주세요..."):
        add_message("user", prompt)
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("잠시 생각 중..."):
                response = get_groq_response(get_current_messages())
                st.markdown(response)
        
        add_message("assistant", response)
        st.rerun()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🚀 메인 앱
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def main():
    st.set_page_config(
        page_title="KANBU - AI 시대 현실 정렬 코치",
        page_icon="🤝",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    load_css()
    init_session_state()
    
    # 사이드바
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <div style="font-size: 3rem;">🤝</div>
            <div style="color: #7986CB; font-size: 1.5rem; font-weight: bold;">KANBU</div>
            <div style="color: #999; font-size: 0.9rem;">현실 인생 정렬 코치</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # KANBU 정체성
        st.markdown("""
        ### 🛡️ KANBU란?
        
        **상담/치료 ❌**  
        **생각 정리 ⭕**
        
        흔들릴 때 잠깐 멈춰주고  
        결정 전에 생각을 정리해주는 AI
        
        ---
        
        *10대든 60대든, 요즘은 다 흔들린다.*  
        *불안한 게 이상한 게 아니다, 정상이다.*
        """)
        
        st.markdown("---")
        
        # 핵심 원칙
        st.markdown("""
        ### ⚖️ 깐부 원칙
        
        ❌ 정답 제시  
        ❌ 훈계/가르침  
        ❌ 재촉/가속
        
        ⭕ 옆에서 같이 생각  
        ⭕ 불안 정리  
        ⭕ 작은 행동 제안
        """)
        
        st.markdown("---")
        
        # 현재 모드
        mode_names = {
            "home": "🏠 홈",
            "anxiety": "😰 불안 점검",
            "choice": "🔀 선택 정리",
            "pace": "🐢 속도 조절",
            "reflect": "💭 생각 정리",
            "free": "💬 자유 대화"
        }
        current = mode_names.get(st.session_state.current_mode, "🏠 홈")
        st.markdown(f"**현재 모드:** {current}")
        
        st.markdown("---")
        
        # 빠른 메뉴
        st.markdown("### ⚡ 빠른 메뉴")
        
        if st.button("🏠 처음으로", use_container_width=True):
            st.session_state.current_mode = "home"
            st.session_state.conversation_started = False
            st.rerun()
        
        if st.button("🗑️ 대화 초기화", use_container_width=True):
            clear_current_messages()
            st.rerun()
        
        st.markdown("---")
        
        # 도움 연락처
        st.markdown("""
        ### 🆘 도움이 필요할 때
        
        **정신건강위기상담**  
        ☎️ 1577-0199
        
        **자살예방상담**  
        ☎️ 1393
        """)
        
        st.markdown("---")
        
        # 데이터 보안 안내
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
        <div style="text-align: center; color: #999; font-size: 0.8rem;">
            <p>Developed by<br>Jameskim + AI Avengers</p>
            <p>Raira · Gemini · Miracle · Perfect</p>
        </div>
        """, unsafe_allow_html=True)
    
    # 메인 영역
    with st.container():
        render_header()
        
        if not st.session_state.conversation_started:
            # 홈 화면 - 기능 카드
            render_function_cards()
            
            # 철학 박스
            st.markdown("""
            <div class="philosophy-box">
                <div class="philosophy-text">
                    "10대든 60대든, 요즘은 다 흔들린다.<br>
                    문제는 나이가 아니라 속도가 바뀐 시대다."
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # 환영 메시지
            st.markdown(f"""
            <div style="text-align: center; margin-top: 1.5rem; padding: 2rem; background: white; border-radius: 16px; box-shadow: 0 2px 10px rgba(0,0,0,0.05);">
                <h3 style="color: {COLORS['text']};">👋 안녕!</h3>
                <p style="color: #666; line-height: 1.8;">
                    나는 <strong style="color: {COLORS['main']};">깐부(KANBU)</strong>야.<br>
                    상담사나 치료사 아니고, 옆에서 같이 생각해주는 AI야.<br><br>
                    불안한 거 이상한 거 아니야.<br>
                    <strong>요즘 세상이 너무 빨라서 그래.</strong><br><br>
                    오늘 뭐가 머릿속에 있어?
                </p>
                <p style="color: #999; font-size: 0.85rem; margin-top: 1rem;">
                    💡 깐부는 정답 안 줘요. 훈계도 안 해요.<br>
                    그냥 옆에 앉아서 같이 생각 정리해줘요.
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            # 대화 화면
            render_chat_interface()
        
        # 푸터
        st.markdown("""
        <div class="kanbu-footer">
            <p>🤝 KANBU v1.0</p>
            <p>흔들릴 때 잠깐 멈춰주는 현실 정렬 코치</p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
