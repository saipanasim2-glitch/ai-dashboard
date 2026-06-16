import streamlit as st
def check_export_access(user: dict) -> bool:
    return user["plan"] == "pro"
def show_upgrade_prompt():
    st.warning("🔒 This feature is only available for Pro subscribers")
    st.markdown("""
        **What do you get by upgrading?**
        -✅ Export data (CSV / Excel)
        -✅ 100 operations per month
        -✅ Priority processing
    """)
    if st.button("⭐ Upgrade to Pro Now", use_container_width=True):
        st.info("Payment gateway - Will be integrated in 5 (Stripe/Paddle)")