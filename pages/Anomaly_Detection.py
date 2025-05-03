import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

def detect_anomalies(data, contamination=0.1):
    # Prepare data
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(data.reshape(-1, 1))
    
    # Train isolation forest
    iso_forest = IsolationForest(contamination=contamination, random_state=42)
    predictions = iso_forest.fit_predict(scaled_data)
    
    # Convert predictions to boolean (True for anomalies)
    anomalies = predictions == -1
    
    return anomalies, iso_forest.score_samples(scaled_data)

def divide_and_conquer_analysis(data, window_size=5):
    n = len(data)
    segments = []
    anomalies = []
    
    # Divide data into segments
    for i in range(0, n, window_size):
        segment = data[i:min(i + window_size, n)]
        segments.append(segment)
        
        # Detect anomalies in segment
        segment_anomalies, scores = detect_anomalies(segment)
        anomalies.extend(segment_anomalies)
    
    return np.array(anomalies)

def show_anomaly_detection():
    st.title("🧠 AI Based Anomaly Detection System Simulation")
    st.markdown("### 🖥 Resource Usage Monitoring and Anomaly Management")
    
    # Input Section
    st.subheader("Resource Usage Data")
    
    # Generate sample data or allow user input
    data_source = st.radio(
        "Choose Data Source",
        ["Generate Sample Data", "Upload Custom Data"]
    )
    
    if data_source == "Generate Sample Data":
        num_samples = st.number_input("Number of Samples", min_value=10, max_value=1000, value=100)
        noise_level = st.slider("Noise Level", 0.0, 1.0, 0.1)
        
        # Generate sample data with some anomalies
        t = np.linspace(0, 10, num_samples)
        base_signal = np.sin(t) + np.cos(2*t)
        noise = np.random.normal(0, noise_level, num_samples)
        
        # Add some anomalies
        anomaly_indices = np.random.choice(num_samples, size=int(num_samples*0.1), replace=False)
        anomalies = np.random.normal(3, 1, len(anomaly_indices))
        
        data = base_signal + noise
        data[anomaly_indices] = anomalies
        
    else:
        uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            data = df.iloc[:, 0].values  # Use first column as data
        else:
            st.warning("Please upload a CSV file")
            return
    
    # Display original data
    st.subheader("Resource Usage Pattern")
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        y=data,
        mode='lines',
        name='Resource Usage'
    ))
    
    fig.update_layout(
        title="Resource Usage Over Time",
        xaxis_title="Time",
        yaxis_title="Usage",
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Anomaly Detection Parameters
    st.subheader("Detection Parameters")
    col1, col2 = st.columns(2)
    with col1:
        contamination = st.slider("Contamination Factor", 0.01, 0.5, 0.1)
    with col2:
        window_size = st.slider("Window Size", 5, 50, 10)
    
    if st.button("Detect Anomalies"):
        # Perform anomaly detection
        anomalies = divide_and_conquer_analysis(data, window_size)
        
        # Display results
        st.subheader("Anomaly Detection Results")
        
        # Plot data with anomalies highlighted
        fig = go.Figure()
        
        # Plot normal points
        normal_indices = ~anomalies
        fig.add_trace(go.Scatter(
            x=np.where(normal_indices)[0],
            y=data[normal_indices],
            mode='lines',
            name='Normal Usage'
        ))
        
        # Plot anomalies
        anomaly_indices = np.where(anomalies)[0]
        fig.add_trace(go.Scatter(
            x=anomaly_indices,
            y=data[anomalies],
            mode='markers',
            marker=dict(size=10, color='red'),
            name='Anomalies'
        ))
        
        fig.update_layout(
            title="Detected Anomalies",
            xaxis_title="Time",
            yaxis_title="Usage",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Display statistics
        num_anomalies = np.sum(anomalies)
        anomaly_percentage = (num_anomalies / len(data)) * 100
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Number of Anomalies", num_anomalies)
        with col2:
            st.metric("Anomaly Percentage", f"{anomaly_percentage:.2f}%")
        
        # Anomaly Details
        if num_anomalies > 0:
            st.subheader("Anomaly Details")
            anomaly_data = []
            for idx in anomaly_indices:
                anomaly_data.append({
                    "Time": idx,
                    "Value": data[idx],
                    "Deviation": abs(data[idx] - np.mean(data))
                })
            
            anomaly_df = pd.DataFrame(anomaly_data)
            st.dataframe(anomaly_df)
            
            # Recommendations
            st.subheader("Recommendations")
            if anomaly_percentage > 20:
                st.warning("High number of anomalies detected. Consider system maintenance.")
            elif anomaly_percentage > 10:
                st.info("Moderate number of anomalies. Monitor system closely.")
            else:
                st.success("System appears to be operating normally.")
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

# Run the main function
show_anomaly_detection() 