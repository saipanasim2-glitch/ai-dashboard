import streamlit as st
from core.database import init_db
from core.auth import register_user, login_user
from core.credits import consume_credit
from core.paywall import check_export_access, show_upgrade_prompt
from components.ui_helpers import show_header, show_tool_card
from services.ai_tools import generate_content, analyze_data, generate_leads
st.set_page_config(
    page_title="AI Dzshboard", 
    page_icon="🤖",
    layout="wide"
)
init_db()
if "user" not in st.session_state:
    st.session_state.user = None
if "last_result" not in st.session_state:
   st.session_state.last_result = None
def show_auth_page():
    col1,col2,col3 = st.columns([1, 2, 1])
    with col2:
        st.title("🤖 AI Dashboard")
        st.caption("One-Click AI Tools")
        st.divider()
        tab1, tab2, = st.tabs(["Login", "Sign Up"])
        with tab1:
            email = st.text_input("Email Address", key="login_email")
            password = st.text_input(
                "Password", type="password", key="login_pass"
            )
            if st.button("Login", use_container_width=True, type="primary"):
                result = login_user(email, password)
                if result["success"]:
                    st.session_state.user = result["user"]
                    st.rerun()
                else:
                    st.error(result["message"])
        with tab2:
            email = st.text_input("Email Address", key="reg_email")
            password = st.text_input(
                "Password", type="password", key="reg_pass"
            )
            if st.button("Create Account", use_container_width=True):
                result = register_user(email, password)
                if result["success"]:
                    st.success(result["message"])
                else:
                    st.error(result["message"])
def run_tool(tool_name: str, ai_func, **kwargs):
    """Unified function to run any AI tool"""
    user = st.session_state.user
    with st.spinner(f"⏳ {tool_name} processing..."):
        credit_result = consume_credit(user["id"])
        if not credit_result["success"]:
            st.error(credit_result["message"])
            return
        output = ai_func(**kwargs)
        st.session_state.last_result = {
            "tool": tool_name,
            "output": output
        }
        st.session_state.user["credits"] = credit_result["remaining"]
        st.rerun()
def show_dashboard():
    user = st.session_state.user
    show_header(user)
    st.subheader("AI Tools")
    col1, col2, col3 = st.columns(3)
    with col1:
        with st.container(border=True):
            st.markdown("## ✍️")
            st.markdown("**Content Generation**")
            st.caption("Create marketing content with one click")
            topic = st.text_input(
                "Topic", placeholder="e.g., Fitness App",
                key="content_topic"
            )
            if st.button("Run", key="tool_content", use_container_width=True):
                if topic:
                    run_tool("Content Generation", generate_content, topic=topic)
                else:
                    st.warning("Please enter a topic first")
    with col2:
        with st.container(border=True):
            st.markdown("## 📊")
            st.markdown("**Data Analaysis**")
            st.caption("Extract instant insights")
            data_desc = st.text_area(
                "Data or Description",
                placeholder="e.g., My sales increased by 20% in january...",
                key="data_input", height=80
            )
            if st.button("Run", key="tool_data", use_container_width=True):
                if data_desc:
                    run_tool("Data Analasis", analyze_data,
                            data_description=data_desc)
                else:
                    st.Warning("Please enter data first")
    with col3:
        with st.container(border=True):
            st.markdown("## 🎯")
            st.markdown("**Lead Generation**")
            st.caption("Potential customer strategies")
            industry = st.text_input(
                "Industry", placeholder="e.g., Tech",
                key="leads_industry"
            )
            target = st.text_input(
                "Target Audience", placeholder="e.g., Small Businesses",
                key="leads_target"
            )
            if st.button("Run", key="tool_leads, use_container_width=True"):
                if industry and target:
                    run_tool("Lead Generation", generate_leads,
                             industry=industry, target=target)
                else:
                    st.warning("Please enter both industry and target audience")
    st.divider()
    st.subheader("Results")
    if st.session_state.last_result:
        result = st.session_state.last_result
        with st.container(border=True):
            st.markdown(f"**Tool Used:** {result['tool']}")
            st.info(result["output"])
            st.markdown("**Export Result:**")
            if check_export_access(user):
                st.download_button(
                    "⬇️ Download Result",
                    data=result["output"],
                    file_name="ai_result.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            else:
                show_upgrade_prompt()
    else:
        st.caption("Click on any tool to see the results here")
if st.session_state.user is None:
    show_auth_page()
else:
    show_dashboard()