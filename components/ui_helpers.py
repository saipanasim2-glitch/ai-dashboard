import streamlit as st
from core.credits import PLAN_LIMITS
def show_header(user: dict):
    plan = user["plan"]
    credits = user["credits"]
    limit = PLAN_LIMITS.get(plan, 3)
    plan_label = "⭐Pro" if plan == "pro" else "Free"
    col1, col2, col3 = st.columns([3, 2, 1])
    with col1:
        st.markdown(f"### 🤖 AI Dashboard")
        st.caption(f"Welcome, {user['email']}")
    with col2:
        st.markdown(f"**Plan:** {plan_label}")
        progress = credits / limit if limit > 0 else 0
        st.progress(progress, text=f"Credits: {credits}/{limit}")
    with col3:
        if st.button("Logout", use_container_width=True):
            st.session_state.user = None
            st.rerun()
    st.divider()
def show_tool_card(title: str, description: str, icon: str, key: str) -> bool:
    with st.container(border=True):
        st.markdown(f"## {icon}")
        st.markdown(f"**{title}**")
        st.caption(description)
        return st.button(
            "Launch",
            key=key,
            use_container_width=True
        )