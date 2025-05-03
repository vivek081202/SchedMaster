import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

def generate_workload_data(num_samples=1000):
    # Generate synthetic workload data
    np.random.seed(42)
    
    # Features
    num_processes = np.random.randint(5, 50, num_samples)
    avg_burst_time = np.random.uniform(1, 10, num_samples)
    priority_variance = np.random.uniform(0, 5, num_samples)
    io_intensity = np.random.uniform(0, 1, num_samples)
    
    # Generate performance metrics for different algorithms
    sjn_performance = 100 - (0.3 * num_processes + 0.2 * avg_burst_time + 0.1 * priority_variance)
    priority_performance = 100 - (0.2 * num_processes + 0.3 * avg_burst_time + 0.2 * priority_variance)
    fcfs_performance = 100 - (0.4 * num_processes + 0.1 * avg_burst_time + 0.3 * priority_variance)
    
    # Determine best algorithm
    performances = np.column_stack((sjn_performance, priority_performance, fcfs_performance))
    best_algorithm = np.argmax(performances, axis=1)
    
    # Create dataset
    data = pd.DataFrame({
        'num_processes': num_processes,
        'avg_burst_time': avg_burst_time,
        'priority_variance': priority_variance,
        'io_intensity': io_intensity,
        'best_algorithm': best_algorithm
    })
    
    return data

def train_algorithm_selector(data):
    # Prepare features and target
    X = data[['num_processes', 'avg_burst_time', 'priority_variance', 'io_intensity']]
    y = data['best_algorithm']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train models
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    svm_model = SVC(probability=True, random_state=42)
    
    rf_model.fit(X_train_scaled, y_train)
    svm_model.fit(X_train_scaled, y_train)
    
    return rf_model, svm_model, scaler

def show_comparative_analysis():
    st.title("📊 Comparative Analysis of Scheduling Algorithms using ML")
    st.markdown("### 🧠 Dynamic Selection of Optimal Scheduling Strategies")
    
    # Generate or load data
    data_source = st.radio(
        "Choose Data Source",
        ["Generate Sample Data", "Upload Custom Data"]
    )
    
    if data_source == "Generate Sample Data":
        num_samples = st.number_input("Number of Samples", min_value=100, max_value=10000, value=1000)
        data = generate_workload_data(num_samples)
    else:
        uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])
        if uploaded_file is not None:
            data = pd.read_csv(uploaded_file)
        else:
            st.warning("Please upload a CSV file")
            return
    
    # Display data statistics
    st.subheader("Workload Data Statistics")
    st.dataframe(data.describe())
    
    # Train models
    rf_model, svm_model, scaler = train_algorithm_selector(data)
    
    # Algorithm Performance Analysis
    st.subheader("Algorithm Performance Analysis")
    
    # Calculate average performance for each algorithm
    algorithm_names = ['SJN', 'Priority', 'FCFS']
    performance_data = []
    
    for i in range(3):
        performance_data.append({
            'Algorithm': algorithm_names[i],
            'Average Performance': data[data['best_algorithm'] == i].shape[0] / len(data) * 100
        })
    
    performance_df = pd.DataFrame(performance_data)
    
    # Plot performance distribution
    fig = go.Figure(data=[
        go.Bar(
            x=performance_df['Algorithm'],
            y=performance_df['Average Performance'],
            text=performance_df['Average Performance'].round(2),
            textposition='auto',
        )
    ])
    
    fig.update_layout(
        title="Algorithm Performance Distribution",
        xaxis_title="Algorithm",
        yaxis_title="Performance (%)",
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Algorithm Selection
    st.subheader("Algorithm Selection")
    
    col1, col2 = st.columns(2)
    with col1:
        num_processes = st.number_input("Number of Processes", min_value=1, value=10)
        avg_burst_time = st.number_input("Average Burst Time", min_value=0.1, value=5.0)
    with col2:
        priority_variance = st.number_input("Priority Variance", min_value=0.0, value=2.0)
        io_intensity = st.slider("I/O Intensity", 0.0, 1.0, 0.5)
    
    if st.button("Predict Best Algorithm"):
        # Prepare input data
        input_data = np.array([[num_processes, avg_burst_time, priority_variance, io_intensity]])
        input_scaled = scaler.transform(input_data)
        
        # Get predictions from both models
        rf_pred = rf_model.predict_proba(input_scaled)[0]
        svm_pred = svm_model.predict_proba(input_scaled)[0]
        
        # Combine predictions (ensemble)
        ensemble_pred = (rf_pred + svm_pred) / 2
        
        # Display results
        st.subheader("Prediction Results")
        
        # Create prediction dataframe
        pred_data = []
        for i, algo in enumerate(algorithm_names):
            pred_data.append({
                'Algorithm': algo,
                'Confidence': ensemble_pred[i] * 100
            })
        
        pred_df = pd.DataFrame(pred_data)
        
        # Plot prediction confidence
        fig = go.Figure(data=[
            go.Bar(
                x=pred_df['Algorithm'],
                y=pred_df['Confidence'],
                text=pred_df['Confidence'].round(2),
                textposition='auto',
            )
        ])
        
        fig.update_layout(
            title="Algorithm Selection Confidence",
            xaxis_title="Algorithm",
            yaxis_title="Confidence (%)",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Display recommendation
        best_algo = algorithm_names[np.argmax(ensemble_pred)]
        confidence = np.max(ensemble_pred) * 100
        
        st.success(f"Recommended Algorithm: {best_algo} (Confidence: {confidence:.2f}%)")
        
        # Feature importance
        st.subheader("Feature Importance")
        feature_importance = pd.DataFrame({
            'Feature': ['Number of Processes', 'Average Burst Time', 'Priority Variance', 'I/O Intensity'],
            'Importance': rf_model.feature_importances_
        })
        
        fig = go.Figure(data=[
            go.Bar(
                x=feature_importance['Feature'],
                y=feature_importance['Importance'],
                text=feature_importance['Importance'].round(3),
                textposition='auto',
            )
        ])
        
        fig.update_layout(
            title="Feature Importance in Algorithm Selection",
            xaxis_title="Feature",
            yaxis_title="Importance",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True) 
    
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
show_comparative_analysis() 