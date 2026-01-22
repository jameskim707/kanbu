"""
🤝 KANBU v2.0 - AI 시대, 판단을 지켜주는 인생 코치
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
개선사항:
1. 대화 단계별 프롬프트 적용 (4단계)
2. 응답 스타일 랜덤화 (3가지 버전)
3. UI 색상 대비 강화
4. 진행 단계 시각화
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import streamlit as st
from groq import Groq
from datetime import datetime
import time
import random
import re

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🎨 컬러 설정 (대비 강화)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
COLORS = {
    "main": "#5C6BC0",
    "accent": "#7986CB",
    "dark": "#303F9F",
    "light": "#E8EAF6",
    "white": "#FFFFFF",
    "warm": "#F5F5F5",
    "text": "#2C2C2C",
    "pause": "#FF7043",
    "reflect": "#26A69A",
    "slow": "#AB47BC",
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🧠 대화 단계별 프롬프트
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KANBU_IDENTITY_PROMPT = """
## ⚠️ 언어 규칙 (절대 준수)
You MUST respond ONLY in Korean (한국어).
절대로 영어, 일본어, 중국어, 태국어 등 다른 언어를 섞지 마세요.

당신은 'KANBU(깐부)'입니다.

## 🎯 KANBU의 정체성
❝AI 시대 현실 인생 정렬 코치❞
❝흔들릴 때 잠깐 멈춰주는 코치❞

⚠️ 중요: KANBU는 상담사/치료사가 아닙니다!
- 고쳐준다 ❌
- 정리해준다 ⭕
- 옆에 앉아 같이 생각하는 AI ⭕

## 🔥 핵심 원칙
절대 하지 않는 것:
- ❌ "이게 정답입니다"
- ❌ 훈계하는 말투
- ❌ 가속/재촉

대신 항상:
- ⭕ "내 생각엔 이런 선택지도 있어"
- ⭕ "지금 상황에선 이 정도만 해도 충분해"
- ⭕ 불안 신호 감지
- ⭕ 생각 정리 도움

## 🗣️ 깐부 말투
- 반말/존댓말 섞어서 편하게
- "~해봐", "~해볼까?", "~인 것 같아"
- 친구처럼 옆에서 이야기하는 느낌
- 짧고 명확하게

## 🚫 금지 영역
- 의료/정신과 치료 → "전문가 상담을 권해요"
- 자해/자살 위기 → 즉시 전문 상담 연결 (1393, 1577-0199)
"""

STAGE_PROMPTS = {
    "초기_공감": """
## 🎧 현재 단계: 초기 공감 (1~2번째 대화)

### 목표
사용자가 편하게 말하게 만들기

### 응답 스타일 (랜덤 적용)
**스타일 A: 짧은 확인형**
- "음..."
- "그랬구나."
- "힘들었겠다."

**스타일 B: 열린 질문형**
- "더 말해줄래?"
- "그래서 어땠어?"
- "어떤 느낌이었어?"

**스타일 C: 공감 확장형**
- "그 상황에서 그럴 수밖에 없었을 것 같아."
- "누구라도 그랬을 거야."

### 절대 금지
- ❌ 조언하기
- ❌ 분석하기
- ❌ 정리 시도
- 지금은 그냥 들어주기만!

### 질문 스타일
열린 질문만. "더 말해줘", "어떤 기분이야?"
""",

    "중간_정리": """
## 📋 현재 단계: 중간 정리 (3~5번째 대화)

### 목표
상황 객관화, 패턴 발견

### 응답 스타일 (랜덤 적용)
**스타일 A: 직설 요약형**
- "정리하면 이거지?"
- "핵심은 ~인 것 같아."
- "결국 ~때문이구나."

**스타일 B: 패턴 발견형**
- "이 얘기 들으니까 패턴이 보이는데?"
- "계속 반복되는 게 있네."
- "공통점이 뭘까?"

**스타일 C: 구조화 질문형**
- "지금까지 나온 걸 3가지로 나누면?"
- "원인/결과로 나눠볼까?"
- "뭐가 제일 무거워?"

### 질문 스타일
구조화 질문. "패턴이 보여?", "공통점은?"

### 주의
아직 조언은 아님! 정리만.
""",

    "심화_통찰": """
## 💡 현재 단계: 심화 통찰 (6~8번째 대화)

### 목표
새로운 관점 제시

### 응답 스타일 (랜덤 적용)
**스타일 A: 반전 해석형**
- "근데 다르게 보면..."
- "이게 오히려..."
- "역설적으로..."

**스타일 B: 가설 제시형**
- "혹시 ~때문 아닐까?"
- "만약에 ~라면?"
- "이건 어때?"

**스타일 C: 질문 역전형**
- "문제가 문제가 아니면?"
- "약점이 강점이면?"
- "불안이 신호면?"

### 질문 스타일
도전적 질문. "만약에?", "반대로?"

### 톤
도전적이지만 따뜻하게
""",

    "실행_제안": """
## 🎯 현재 단계: 실행 제안 (9번째~)

### 목표
작고 구체적인 행동

### 응답 스타일 (랜덤 적용)
**스타일 A: 최소 행동형**
- "오늘 딱 하나만?"
- "10분 안에 끝낼 수 있는 거?"
- "가장 쉬운 첫걸음?"

**스타일 B: 실험 제안형**
- "일주일만 실험해볼까?"
- "한 번만 해보면?"
- "테스트로 해보자."

**스타일 C: 선택 제시형**
- "A하기 vs B하기, 둘 중 뭐?"
- "이거 3가지 중 하나?"
- "오늘/내일/다음주, 언제?"

### 질문 스타일
구체적 행동 질문. "뭐부터?", "언제?"

### 주의
여전히 강요는 ❌. 제안만.
"""
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🎨 CSS 스타일 (대비 강화)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def load_css():
    st.markdown(f"""
    <style>
        .stApp {{
            background: linear-gradient(180deg, {COLORS['light']} 0%, {COLORS['warm']} 100%);
        }}
        
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
        
        .function-card {{
            background: white;
            border-radius: 16px;
            padding: 1.5rem;
            margin: 0.5rem 0;
            border-left: 4px solid {COLORS['light']};
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            transition: all 0.3s ease;
        }}
        
        .function-card:hover {{
            border-left-color: {COLORS['main']};
            transform: translateX(4px);
            box-shadow: 0 4px 12px rgba(92, 107, 192, 0.15);
        }}
        
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
            box-shadow: 0 2px 8px rgba(92, 107, 192, 0.3);
        }}
        
        .assistant-message {{
            background: {COLORS['white']};
            color: {COLORS['text']};
            border: 2px solid {COLORS['light']};
            border-bottom-left-radius: 4px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        }}
        
        .stage-indicator {{
            text-align: center;
            padding: 0.5rem;
            background: {COLORS['light']};
            border-radius: 10px;
            margin-bottom: 1rem;
            border: 2px solid {COLORS['accent']};
        }}
        
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header {{visibility: hidden;}}
    </style>
    """, unsafe_allow_html=True)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🔧 유틸리티 함수
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def init_session_state():
    if "mode_messages" not in st.session_state:
        st.session_state.mode_messages = {
            "anxiety": [], "choice": [], "pace": [], "reflect": [], "free": []
        }
    if "current_mode" not in st.session_state:
        st.session_state.current_mode = "home"
    if "conversation_started" not in st.session_state:
        st.session_state.conversation_started = False

def get_conversation_stage(messages):
    """대화 단계 판단"""
    count = len(messages) // 2
    if count <= 2:
        return "초기_공감"
    elif count <= 5:
        return "중간_정리"
    elif count <= 8:
        return "심화_통찰"
    else:
        return "실행_제안"

def get_current_messages():
    mode = st.session_state.current_mode
    if mode in st.session_state.mode_messages:
        return st.session_state.mode_messages[mode]
    return []

def add_message(role, content):
    mode = st.session_state.current_mode
    if mode in st.session_state.mode_messages:
        st.session_state.mode_messages[mode].append({
            "role": role, "content": content
        })

def clear_current_messages():
    mode = st.session_state.current_mode
    if mode in st.session_state.mode_messages:
        st.session_state.mode_messages[mode] = []

def filter_foreign_chars(text):
    text = re.sub(r'[\u4e00-\u9fff]', '', text)
    text = re.sub(r'[\u3040-\u309f]', '', text)
    text = re.sub(r'[\u30a0-\u30ff]', '', text)
    text = re.sub(r'[\u0e00-\u0e7f]', '', text)
    text = re.sub(r' +', ' ', text)
    return text.strip()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🤖 Groq API (단계별 프롬프트 적용)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def get_groq_response(messages):
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        
        # 대화 단계 파악
        stage = get_conversation_stage(messages)
        stage_prompt = STAGE_PROMPTS.get(stage, "")
        
        # 시스템 프롬프트에 단계 추가
        enhanced_prompt = KANBU_IDENTITY_PROMPT + "\n\n" + stage_prompt
        
        system_message = {"role": "system", "content": enhanced_prompt}
        full_messages = [system_message] + messages
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=full_messages,
            temperature=0.7,  # 다양성 증가
            max_tokens=1024,
        )
        
        result = response.choices[0].message.content
        result = filter_foreign_chars(result)
        return result
    except Exception as e:
        return f"🤝 ⚠️ 연결에 문제가 생겼어요. 잠시 후 다시 시도해주세요.\n\n(오류: {str(e)})"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🎨 UI 컴포넌트
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def render_header():
    st.markdown("""
    <div class="kanbu-header">
        <div class="kanbu-title">🤝 깐부 KANBU v2.0</div>
        <div class="kanbu-subtitle">흔들릴 때 잠깐 멈춰주는 현실 정렬 코치</div>
    </div>
    """, unsafe_allow_html=True)

def render_function_cards():
    functions = [
        {
            "icon": "😰", "title": "불안 점검", "desc": "이 불안, 현실일까 비교일까?",
            "mode": "anxiety",
            "first_msg": "😰 불안 점검이야.\n\n요즘 뭐가 불안하거나 조급해?\n그게 진짜 상황 때문인지, 아니면 남들이랑 비교해서 그런 건지 같이 나눠보자."
        },
        {
            "icon": "🔀", "title": "선택 정리", "desc": "결정 압박, 정리해볼까?",
            "mode": "choice",
            "first_msg": "🔀 선택 정리야.\n\n지금 뭔가 결정해야 할 것 같아서 머리 아파?\n일단 선택지 정리하고, 지금 당장 결정해야 하는 건지 같이 생각해보자."
        },
        {
            "icon": "🐢", "title": "속도 조절", "desc": "지금, 멈춰도 괜찮을까?",
            "mode": "pace",
            "first_msg": "🐢 속도 조절이야.\n\n뭔가 계속 해야 할 것 같은 느낌 있어?\n잠깐 멈춰도 큰일 안 나. 나만의 속도 찾아보자."
        },
        {
            "icon": "💭", "title": "생각 정리", "desc": "머릿속이 복잡할 때",
            "mode": "reflect",
            "first_msg": "💭 생각 정리야.\n\n머릿속이 복잡해? 정리가 안 돼?\n하나씩 꺼내보자. 말로 하다 보면 정리돼."
        },
        {
            "icon": "💬", "title": "자유 대화", "desc": "그냥 이야기하고 싶을 때",
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
                        "role": "assistant", "content": func['first_msg']
                    })
                st.rerun()

def render_chat_interface():
    messages = get_current_messages()
    
    # 진행 단계 표시
    stage = get_conversation_stage(messages)
    stage_names = {
        "초기_공감": "🎧 공감 단계",
        "중간_정리": "📋 정리 단계",
        "심화_통찰": "💡 통찰 단계",
        "실행_제안": "🎯 실행 단계"
    }
    
    st.markdown(f"""
    <div class="stage-indicator">
        <small style="color: {COLORS['dark']};">현재 단계: <strong>{stage_names.get(stage, '대화 중')}</strong></small>
    </div>
    """, unsafe_allow_html=True)
    
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
        page_title="KANBU v2.0 - AI 시대 현실 정렬 코치",
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
            <div style="color: #7986CB; font-size: 1.5rem; font-weight: bold;">KANBU v2.0</div>
            <div style="color: #999; font-size: 0.9rem;">현실 인생 정렬 코치</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.markdown("""
        ### 🛡️ KANBU란?
        
        **상담/치료 ❌**  
        **생각 정리 ⭕**
        
        흔들릴 때 잠깐 멈춰주고  
        결정 전에 생각을 정리해주는 AI
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
        
        st.markdown("""
        ### 🆘 도움이 필요할 때
        
        **정신건강위기상담**  
        ☎️ 1577-0199
        
        **자살예방상담**  
        ☎️ 1393
        """)
    
    # 메인 영역
    with st.container():
        render_header()
        
        if not st.session_state.conversation_started:
            render_function_cards()
            
            st.markdown(f"""
            <div style="text-align: center; margin-top: 1.5rem; padding: 2rem; background: white; border-radius: 16px; box-shadow: 0 2px 10px rgba(0,0,0,0.05);">
                <h3 style="color: {COLORS['text']};">👋 안녕!</h3>
                <p style="color: #666; line-height: 1.8;">
                    나는 <strong style="color: {COLORS['main']};">깐부(KANBU) v2.0</strong>이야.<br>
                    상담사나 치료사 아니고, 옆에서 같이 생각해주는 AI야.<br><br>
                    불안한 거 이상한 거 아니야.<br>
                    <strong>요즘 세상이 너무 빨라서 그래.</strong>
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            render_chat_interface()

if __name__ == "__main__":
    main()
