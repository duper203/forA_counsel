import streamlit as st
import os
from openai import OpenAI
# from get_context_2 import retrieve_relevant_info

# Replace with your actual OpenAI API key
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
st.title("💬 모리")
st.caption("🚀 ADHD 인들을 위한 AI 챗봇 모리")

# Initialize session state variables
if "step" not in st.session_state:
    st.session_state["step"] = 1
if "user_name" not in st.session_state:
    st.session_state["user_name"] = ""
if "sym_name_result" not in st.session_state:
    st.session_state["sym_name_result"] = []
if "checkbox_state" not in st.session_state:
    st.session_state["checkbox_state"] = {}
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Step 1: Basic Information Input
if st.session_state["step"] == 1:
    msg_one = {
        "role": "assistant",
        "content": "안녕하세요 ADHD 인들을 위한 AI 챗봇 모리 입니다. 상담을 시작하기 전 기본 정보 몇 가지만 물어보겠습니다.",
    }
    message = st.chat_message(msg_one["role"])

    with message:
        message.write(msg_one["content"])
        expander = message.expander("기본정보 입력해 주세요")
        st.session_state["user_name"] = expander.text_input("제가 어떤 닉네임으로 불러 드리면 될까요?", key="user_name_input")
        
        expander.radio("성별", ["여", "남", "기타"], key="gender")
        expander.number_input("태어난 연도를 알려주세요", min_value=1900, max_value=2025, key="birth_year")
        expander.selectbox(
            "어떤 일을 하고 계신가요?", ["학생", "직장인", "프리랜서", "전업주부", "구직 중", "기타"], key="job"
        )
        expander.radio(
            "ADHD 진단 받은 적이 있나요", ["예, 진단 받았습니다", "아니오, 진단 받지 않았습니다."], key="adhd_diagnosis"
        )
        expander.radio("복용 중인 약이 현재 있으실까요?", ["예, 복용 중입니다.", "아니오, 복용하고 있지 않습니다."], key="medication")
        
        
        expander.write(
            """
            ADHD는 종종 다른 건강 상태와 함께 나타나는 경우가 많습니다. 혹시 ADHD외에 아래의 건강 문제나 증상이 있으신지 여쭤봐도 괜찮을까요?
            걱정하지 마세요! 선택하신 내용은 당신에게 맞는 도움을 제공을 위해서만 활용 됩니다.
            """
        )

        symptoms = [
            "기분 장애 (우울증, 조울증 등)",
            "불안 장애",
            "수면 문제",
            "감정 조절 또는 분노 조절 문제",
            "자폐 스펙트럼 또는 사회적 어려움",
            "학습 장애 또는 언어 문제",
            "기타 신체적/정신적 건강 문제",
            "해당 없음",
        ]


        for sym in symptoms:
            if sym not in st.session_state["checkbox_state"]:
                st.session_state["checkbox_state"][sym] = False
            is_checked = expander.checkbox(
                sym, key=f"sym_{sym}", value=st.session_state["checkbox_state"][sym]
            )
            st.session_state["checkbox_state"][sym] = is_checked

        st.session_state["sym_name_result"] = [
            sym for sym, checked in st.session_state["checkbox_state"].items() if checked
        ]


        
        
        button_one = expander.button("제출")

    if button_one:
        st.session_state["step"] = 3





# Step 3: Final Message
if st.session_state["step"] == 3:
    msg_three = {
        "role": "assistant",
        "content": f"감사합니다! 이렇게 답변해주신 토대로 더 나은 대화를 이어갈 수 있도록 하겠습니다. 오늘 하루는 어떠셨나요? 저는 {st.session_state['user_name']}님의 상담 챗봇이니, 개인정보 유출 걱정 없이 편안하게 속마음을 털어주세요.",
    }
    message_three = st.chat_message(msg_three["role"])
    with message_three:
        message_three.write(msg_three["content"])

    # 초기화 메시지 추가 (Step 3 이후에만 실행)
    if not st.session_state["messages"]:
        st.session_state["messages"] = [
            {"role": "assistant", "content": "안녕하세요! ADHD 인들을 위한 AI 챗봇 모리입니다. 무엇을 도와드릴까요?"}
        ]

# Display chat history
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input handling
if prompt := st.chat_input(placeholder="메시지를 입력하세요..."):
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # prompting
    prompt_messages = [
        {
            "role": "system", 
            "content": f'''

            너의 이름은 '모리'이고 너는 ADHD를 지원하는 친근한 상담사 AI 챗봇이다. 너가 상담할 사람의 이름은 {st.session_state["user_name"]}
            
            다음의 지침을 반드시 따라야 한다:

            1. **공감적 태도**:
            - 사용자가 공유하는 감정과 경험에 대해 진심으로 공감하고, 비판하지 않으며, 그들의 이야기를 경청한다.
            - "그럴 수 있죠." "충분히 이해가 돼요." 같은 표현으로 공감을 표현하라.

            2. **부드럽고 따뜻한 어조**:
            - 대화 중 항상 부드럽고 따뜻한 어조를 유지하며, 사용자가 안전하고 편안하게 느낄 수 있도록 노력한다.
            - 예를 들어, "제가 도움을 드릴 수 있어 정말 기뻐요." 같은 표현을 사용한다.
            - 친구 같이 대해주고

            3. **문제를 해결할 수 있는 조언 제공**:
            - ADHD 관리, 감정 조절, 우울증 극복을 위한 간단하고 실용적인 팁을 제공하라.
            - 예를 들어, "작은 목표를 세우고, 하나씩 달성해 나가는 것이 도움이 될 수 있어요."와 같은 구체적인 조언을 준다.
            - "(이렇게) 해보는 것을 어떨까요" 이런 식의 문제 해결 답변을 줘.

            4. **위기 상황 처리**:
            - 만약 사용자가 극도로 불안해하거나 위기에 처해 있는 경우, "전문가와 상담하는 것이 가장 중요합니다. 가까운 상담 센터나 믿을 수 있는 사람에게 도움을 요청해 보세요."와 같은 적절한 안내를 제공한다.

            5. **긍정적인 강화**:
            - 사용자의 노력과 성취를 칭찬하며, 스스로를 믿고 도전할 수 있도록 용기를 북돋는다.
            - "이야기를 나눠 주셔서 감사합니다. 스스로를 돌보려는 당신의 태도가 정말 대단해요."

            6. **다양한 상담 시나리오 대응**:
            - ADHD와 우울증의 공통 증상(집중력 저하, 무기력감, 감정 기복 등)을 이해하고, 사용자 질문에 맞는 대답을 제공한다.
            - 질문 예시:
                - "최근 집중이 잘 안 돼요. 어떻게 하면 좋을까요?"
                - "너무 무기력해서 아무것도 하기 싫어요. 어떻게 극복할 수 있을까요?"

            7. **중립적이고 편견 없는 태도**:
            - 사용자의 성별, 나이, 직업, 문화적 배경에 상관없이 동일한 존중과 이해를 바탕으로 대화한다.


            

            '''
        },
        *st.session_state["messages"],  # 기존 대화 히스토리를 포함
    ]

    # OpenAI API 호출 (챕솟 프롬프팅 적용)
    client = OpenAI(
        api_key=OPENAI_API_KEY,
    )
    response = client.chat.completions.create(
        messages=prompt_messages,
        model="gpt-4o",
    )

    # 챗봇 응답 추가 및 표시
    msg = response.choices[0].message.content
    st.session_state["messages"].append({"role": "assistant", "content": msg})
    with st.chat_message("assistant"):
        st.write(msg)

