import streamlit as st
from streamlit_extras.colored_header import colored_header

st.set_page_config(
    page_title="Welcome to SchedMaster! - Intelligent Scheduling & Optimization Simulation",
    page_icon="⏱️",
    layout="wide",
    initial_sidebar_state="expanded"
)

pages = {
    "App Navigations": [
        st.Page("Home.py", title="Home", icon='🏠' ,default=True),
    ],
    "Modules": [
        st.Page("CPU_Scheduling.py", title="CPU Scheduling", icon='🖥️'),
        st.Page("Disk_Scheduling.py", title="Disk Scheduling",  icon='💾'),
        st.Page("Process_Sync.py", title="Process Sync & Resource Allocation",  icon='🔄'),
        st.Page("Anomaly_Detection.py", title="Anomaly Detection",  icon='🚨'),
        st.Page("Comparative_Analysis.py", title="Comparative Analysis",  icon='📊')
    ]
}

with st.sidebar:
    st.markdown("### ℹ️ About SchedMaster")
    st.markdown("""
    **SchedMaster** is an intelligent CPU, Disk, and Resource Scheduling Simulation platform.  
    It integrates classic algorithms (Greedy, DP, Backtracking) with Machine Learning to predict, optimize, and visualize system scheduling in dynamic environments.

    - 🖥️ CPU Scheduling
    - 💾 Disk Scheduling
    - 🔄 Process Sync & Resource Allocation
    - 🚨 Anomaly Detection
    - 📊 Comparative Analysis
    """)
    st.markdown("---")
    st.caption("🔵 Developed with ❤️ using Python & Streamlit")


pg = st.navigation(pages)
pg.run()
