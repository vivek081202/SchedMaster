import streamlit as st
from streamlit_extras.colored_header import colored_header
from streamlit_extras.let_it_rain import rain
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_lottie import st_lottie
import requests

st.title("⏱️SchedMaster")
st.subheader("Intelligent Scheduling & Optimization Simulation tool using with Machine Intelligence")

@st.cache_data
def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_animation = load_lottie_url("https://lottie.host/9d68283a-de3f-4a55-80bf-e0f36f24d249/nohGByfBxR.json")

if lottie_animation:
    st_lottie(lottie_animation, speed=1, width=700, height=500, key="cpu_scheduling")


st.markdown(
    """
    **SchedMaster** is an advanced simulation tool designed to optimize CPU scheduling, disk scheduling, and resource allocation by applying cutting-edge Design and Analysis of Algorithms (DAA) techniques. This project leverages powerful methods such as Dynamic Programming (DP), Greedy Algorithms, and Backtracking to solve resource scheduling challenges efficiently.Incorporating Machine Learning (ML) techniques like Supervised Learning and Anomaly Detection, SchedMaster enhances the adaptability and intelligence of scheduling decisions, making it a smart tool for modern systems. 

📌 **Why use SchedMaster?**  
        🔹 **Visualizes CPU & Disk Scheduling** with step-by-step execution.  
        🔹 **Interactive Simulations** for process scheduling.  
        🔹 **Compares Algorithms** to analyze performance.  
        🔹 **Detects Anomalies** like deadlocks & starvation.  
        🔹 **User-friendly UI** with GIFs and images for better understanding. 
    """
)


colored_header(label="Key Features", description="Essential modules of SchedMaster", color_name="blue-70")

#col1, col2, col3  = st.columns(3)
col1, spacer, col2, spacer2, col3 = st.columns([1, 0.5, 1, 0.5, 1]) 

with col1:
    st.image("../images/time-management.png", width=80)
    st.markdown("**CPU Scheduling**")
    st.write("CPU Scheduling using Greedy Algorithms & ML Predictions : Implements Shortest Job Next (SJN) and Priority Scheduling using a Greedy strategy, where the process with the least execution time or highest priority is selected first.")
    st.markdown("<br>", unsafe_allow_html=True)
    st.image("../images/detection.png", width=80)
    st.markdown("**Anomaly detection**")
    st.write("Anomaly Detection using Divide & Conquer, Greedy Strategies & ML Models : Uses Divide & Conquer to segment large resource usage data and detect anomalies efficiently.")
    
with col2:
    st.image("../images/schedule.png", width=80)
    st.markdown("**Disk Scheduling**")
    st.write("Disk Scheduling Optimization using Dynamic Programming & LSTM Models : Uses Memorization to store previously computed seek times, preventing redundant calculations.")
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.image("../images/comparison.png", width=80)
    st.markdown("**Comparative Analysis**")
    st.write("Comparative Analysis of Scheduling Algorithms using ML : Uses Supervised Learning & DP to analyze different CPU and disk scheduling algorithms.")

with col3:
    st.image("../images/resource-allocation.png", width=80)
    st.markdown("**Process synchronization and resource allocation**")
    st.write("Process Synchronization & Resource Allocation using Backtracking & RL : Implements Banker's Algorithm for deadlock avoidance, using backtracking to explore safe resource allocations.")
   


st.markdown(
    """
    ---
    <div style="text-align: center">
     <p><strong>🎯Get Started Today!</strong> Select a module from the navigation panel and explore SchedMaster's functionalities.</p>
   </div>
    """, unsafe_allow_html=True
)

st.markdown("---")
st.markdown("""
<div style="text-align: center; font-size: 14px; padding: 10px; color: #666;">
    <p><strong>SchedMaster ⚙️</strong></p>
    <p>
        Intelligent Scheduling & Optimization Simulation using Design and Analysis of Algorithms with Machine Intelligence.
    </p>
    <p>© 2025 | Developed with ❤️ and responsibility by SchedMaster Team.</p>
</div>
""", unsafe_allow_html=True)