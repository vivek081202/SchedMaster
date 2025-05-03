import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

def calculate_seek_time(current_position, target_position):
    return abs(current_position - target_position)

def fcfs_scheduling(requests, initial_position):
    n = len(requests)
    seek_times = []
    current_position = initial_position
    total_seek_time = 0
    sequence = []
    
    for request in requests:
        seek_time = calculate_seek_time(current_position, request)
        sequence.append(request)
        seek_times.append(seek_time)
        total_seek_time += seek_time
        current_position = request
    
    return sequence, seek_times, total_seek_time

def sstf_scheduling(requests, initial_position):
    n = len(requests)
    seek_times = []
    current_position = initial_position
    total_seek_time = 0
    sequence = []
    remaining_requests = requests.copy()
    
    while remaining_requests:
        min_seek_time = float('inf')
        next_request = -1
        
        for i, request in enumerate(remaining_requests):
            seek_time = calculate_seek_time(current_position, request)
            if seek_time < min_seek_time:
                min_seek_time = seek_time
                next_request = i
        
        if next_request != -1:
            sequence.append(remaining_requests[next_request])
            seek_times.append(min_seek_time)
            total_seek_time += min_seek_time
            current_position = remaining_requests[next_request]
            remaining_requests.pop(next_request)
    
    return sequence, seek_times, total_seek_time

def scan_scheduling(requests, initial_position, disk_size=200):
    n = len(requests)
    seek_times = []
    current_position = initial_position
    total_seek_time = 0
    sequence = []
    
    # Sort requests
    sorted_requests = sorted(requests)
    
    # Split requests into two parts: before and after initial position
    left_requests = [r for r in sorted_requests if r <= initial_position]
    right_requests = [r for r in sorted_requests if r > initial_position]
    
    # First move towards 0
    for request in reversed(left_requests):
        seek_time = calculate_seek_time(current_position, request)
        sequence.append(request)
        seek_times.append(seek_time)
        total_seek_time += seek_time
        current_position = request
    
    # If there are requests beyond initial position, move to 0 and then to disk_size
    if right_requests:
        # Move to 0
        seek_time = calculate_seek_time(current_position, 0)
        total_seek_time += seek_time
        current_position = 0
        
        # Move towards disk_size
        for request in right_requests:
            seek_time = calculate_seek_time(current_position, request)
            sequence.append(request)
            seek_times.append(seek_time)
            total_seek_time += seek_time
            current_position = request
    
    return sequence, seek_times, total_seek_time

def cscan_scheduling(requests, initial_position, disk_size=200):
    n = len(requests)
    seek_times = []
    current_position = initial_position
    total_seek_time = 0
    sequence = []
    
    # Sort requests
    sorted_requests = sorted(requests)
    
    # Split requests into two parts: before and after initial position
    left_requests = [r for r in sorted_requests if r <= initial_position]
    right_requests = [r for r in sorted_requests if r > initial_position]
    
    # First move towards disk_size
    for request in right_requests:
        seek_time = calculate_seek_time(current_position, request)
        sequence.append(request)
        seek_times.append(seek_time)
        total_seek_time += seek_time
        current_position = request
    
    # Move to disk_size and then to 0
    if left_requests or right_requests:
        # Move to disk_size if not already there
        if current_position != disk_size:
            seek_time = calculate_seek_time(current_position, disk_size)
            total_seek_time += seek_time
            current_position = disk_size
        
        # Move to 0
        seek_time = calculate_seek_time(current_position, 0)
        total_seek_time += seek_time
        current_position = 0
        
        # Move through left requests
        for request in left_requests:
            seek_time = calculate_seek_time(current_position, request)
            sequence.append(request)
            seek_times.append(seek_time)
            total_seek_time += seek_time
            current_position = request
    
    return sequence, seek_times, total_seek_time

def look_scheduling(requests, initial_position):
    n = len(requests)
    seek_times = []
    current_position = initial_position
    total_seek_time = 0
    sequence = []
    
    # Sort requests
    sorted_requests = sorted(requests)
    
    # Find the position to start moving towards smaller values
    start_idx = 0
    for i, request in enumerate(sorted_requests):
        if request >= initial_position:
            start_idx = i
            break
    
    # Move towards smaller values
    for i in range(start_idx-1, -1, -1):
        seek_time = calculate_seek_time(current_position, sorted_requests[i])
        sequence.append(sorted_requests[i])
        seek_times.append(seek_time)
        total_seek_time += seek_time
        current_position = sorted_requests[i]
    
    # Move towards larger values
    for i in range(start_idx, len(sorted_requests)):
        seek_time = calculate_seek_time(current_position, sorted_requests[i])
        sequence.append(sorted_requests[i])
        seek_times.append(seek_time)
        total_seek_time += seek_time
        current_position = sorted_requests[i]
    
    return sequence, seek_times, total_seek_time

def clook_scheduling(requests, initial_position):
    n = len(requests)
    seek_times = []
    current_position = initial_position
    total_seek_time = 0
    sequence = []
    
    # Sort requests
    sorted_requests = sorted(requests)
    
    # Find the position to start moving towards larger values
    start_idx = 0
    for i, request in enumerate(sorted_requests):
        if request >= initial_position:
            start_idx = i
            break
    
    # Move towards larger values
    for i in range(start_idx, len(sorted_requests)):
        seek_time = calculate_seek_time(current_position, sorted_requests[i])
        sequence.append(sorted_requests[i])
        seek_times.append(seek_time)
        total_seek_time += seek_time
        current_position = sorted_requests[i]
    
    # Move from smallest to initial position
    for i in range(start_idx):
        seek_time = calculate_seek_time(current_position, sorted_requests[i])
        sequence.append(sorted_requests[i])
        seek_times.append(seek_time)
        total_seek_time += seek_time
        current_position = sorted_requests[i]
    
    return sequence, seek_times, total_seek_time

@st.cache_data
def predict_next_request(historical_data, window_size=5):
    if len(historical_data) < window_size:
        return None
    
    # Prepare data for prediction
    X = []
    y = []
    
    for i in range(len(historical_data) - window_size):
        X.append(historical_data[i:i+window_size])
        y.append(historical_data[i+window_size])
    
    if not X or not y:  # Check if we have any data to train on
        return None
        
    X = np.array(X)
    y = np.array(y)
    
    # Ensure X is 2D
    if len(X.shape) == 1:
        X = X.reshape(-1, 1)
    
    # Train a simple linear regression model
    model = LinearRegression()
    model.fit(X, y)
    
    # Predict next position
    last_window = historical_data[-window_size:]
    predicted_position = model.predict([last_window])[0]
    
    # Ensure prediction stays within disk bounds
    predicted_position = max(0, min(predicted_position, 200))
    
    return predicted_position

def show_disk_scheduling():
    st.title("💽 Disk Scheduling Optimization")
    st.markdown("### 🚀 built with Dynamic Programming & LSTM with Future Access Predictions")
    
    # Input Section
    st.subheader("Disk Request Configuration")
    
    col1, col2 = st.columns(2)
    with col1:
        initial_position = st.number_input("Initial Head Position", min_value=0, value=50)
        disk_size = st.number_input("Disk Size", min_value=100, value=200)
    with col2:
        algorithm = st.selectbox(
            "Select Scheduling Algorithm",
            ["First Come First Serve (FCFS)", "Shortest Seek Time First (SSTF)", 
             "SCAN (Elevator)", "C-SCAN (Circular SCAN)",
             "LOOK", "C-LOOK (Circular LOOK)"]
        )
    
    # Request Input
    st.write("Enter track positions separated by commas (e.g., 50, 100, 150)")
    request_input = st.text_input("Track Positions", value="50, 100, 150, 200, 199")
    
    try:
        requests = [int(x.strip()) for x in request_input.split(",")]
        if not all(0 <= x <= disk_size for x in requests):
            st.error(f"All track positions must be between 0 and {disk_size}")
            return
    except ValueError:
        st.error("Please enter valid numbers separated by commas")
        return
    
    if st.button("Calculate Schedule"):
        # Select algorithm and calculate schedule
        if algorithm == "First Come First Serve (FCFS)":
            sequence, seek_times, total_seek_time = fcfs_scheduling(requests, initial_position)
        elif algorithm == "Shortest Seek Time First (SSTF)":
            sequence, seek_times, total_seek_time = sstf_scheduling(requests, initial_position)
        elif algorithm == "SCAN (Elevator)":
            sequence, seek_times, total_seek_time = scan_scheduling(requests, initial_position, disk_size)
        elif algorithm == "C-SCAN (Circular SCAN)":
            sequence, seek_times, total_seek_time = cscan_scheduling(requests, initial_position, disk_size)
        elif algorithm == "LOOK":
            sequence, seek_times, total_seek_time = look_scheduling(requests, initial_position)
        else:  # C-LOOK
            sequence, seek_times, total_seek_time = clook_scheduling(requests, initial_position)
        
        # Display Results
        st.subheader("Scheduling Results")
        
        # Create DataFrame for results
        results = []
        for i in range(len(sequence)):
            results.append({
                "Request": i+1,
                "Position": sequence[i],
                "Seek Time": seek_times[i]
            })
        
        df = pd.DataFrame(results)
        st.dataframe(df)
        
        # Display metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Seek Time", f"{total_seek_time}")
        with col2:
            st.metric("Average Seek Time", f"{total_seek_time/len(sequence):.2f}")
        with col3:
            st.metric("Total Requests", f"{len(sequence)}")
        
        # Enhanced Visualization using Matplotlib
        st.subheader("Disk Head Movement Visualization")
        
        # Create figure and axis
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Set up the disk track
        ax.axhline(y=0.5, color='black', linewidth=2)
        
        # Add track markers
        track_markers = list(range(0, disk_size + 1, 20))
        for track in track_markers:
            ax.plot([track, track], [0.4, 0.6], color='gray', linewidth=1)
            ax.text(track, 0.3, str(track), ha='center', fontsize=8)
        
        # Plot initial position
        ax.plot(initial_position, 0.5, 'r*', markersize=15, label='Initial Position')
        ax.text(initial_position, 0.6, f'Start: {initial_position}', ha='center')
        
        # Create movement path
        x_points = [initial_position] + sequence
        y_points = [0.5] * (len(sequence) + 1)
        
        # Plot the movement path with color gradient based on seek times
        norm = plt.Normalize(0, max(seek_times) if seek_times else 1)
        cmap = plt.cm.RdYlGn_r
        
        # Add arrows for movement direction
        for i in range(len(x_points)-1):
            dx = x_points[i+1] - x_points[i]
            dy = y_points[i+1] - y_points[i]
            arrow = plt.arrow(x_points[i], y_points[i], dx, dy, 
                            head_width=0.05, head_length=5, 
                            fc='blue', ec='blue', alpha=0.5)
        
        # Plot the points with color based on seek time
        scatter = ax.scatter(sequence, [0.5] * len(sequence), 
                           c=seek_times, cmap=cmap, norm=norm,
                           s=100, zorder=5)
        
        # Add seek time labels
        for i, (x, y, seek) in enumerate(zip(sequence, [0.5] * len(sequence), seek_times)):
            ax.text(x, y + 0.1, f'Seek: {seek}', ha='center', fontsize=8)
        
        # Add circular movement path for C-SCAN and C-LOOK
        if algorithm in ["C-SCAN (Circular SCAN)", "C-LOOK (Circular LOOK)"]:
            # Draw the circular path
            ax.plot([sequence[-1], disk_size], [0.5, 0.5], 'purple', linestyle='--')
            ax.plot([disk_size, disk_size], [0.5, 0.7], 'purple', linestyle='--')
            ax.plot([disk_size, 0], [0.7, 0.7], 'purple', linestyle='--')
            ax.plot([0, sequence[0]], [0.5, 0.5], 'purple', linestyle='--')
            
            # Add arrow for circular movement
            ax.annotate('', xy=(disk_size, 0.6), xytext=(sequence[-1], 0.5),
                       arrowprops=dict(arrowstyle='->', color='purple', linestyle='--'))
            ax.annotate('', xy=(0, 0.6), xytext=(disk_size, 0.7),
                       arrowprops=dict(arrowstyle='->', color='purple', linestyle='--'))
        
        # Add colorbar
        cbar = plt.colorbar(scatter, ax=ax)
        cbar.set_label('Seek Time')
        cbar.set_ticks([0, max(seek_times)/2, max(seek_times)])
        cbar.set_ticklabels(['Low', 'Medium', 'High'])
        
        # Set axis properties
        ax.set_xlim(-10, disk_size + 10)
        ax.set_ylim(0, 1)
        ax.set_xlabel('Track Position')
        ax.set_title(f'Disk Head Movement Pattern - {algorithm}', pad=20)
        ax.grid(True, linestyle='--', alpha=0.7)
        
        # Remove y-axis ticks and labels
        ax.set_yticks([])
        
        # Add legend
        ax.legend(loc='upper right')
        
        # Adjust layout
        plt.tight_layout()
        
        # Display the plot
        st.pyplot(fig)
        
        # Add summary statistics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Seek Time", f"{total_seek_time}")
        with col2:
            st.metric("Average Seek Time", f"{total_seek_time/len(sequence):.2f}")
        with col3:
            st.metric("Total Requests", f"{len(sequence)}")
        
        # Seek Time Analysis
        st.subheader("Seek Time Analysis")
        fig_seek = go.Figure()
        
        fig_seek.add_trace(go.Bar(
            x=list(range(1, len(seek_times) + 1)),
            y=seek_times,
            text=seek_times,
            textposition='auto',
            name='Seek Time'
        ))
        
        fig_seek.add_hline(
            y=total_seek_time/len(sequence),
            line_dash="dash",
            line_color="red",
            annotation_text=f"Average: {total_seek_time/len(sequence):.2f}"
        )
        
        fig_seek.update_layout(
            title="Seek Time per Request",
            xaxis_title="Request Number",
            yaxis_title="Seek Time",
            height=300
        )
        st.plotly_chart(fig_seek, use_container_width=True)
        
        # ML Prediction Section
        st.subheader("Request Pattern Prediction")
        window_size = st.slider(
            "Prediction Window Size",
            min_value=2,
            max_value=10,
            value=5,
            key="prediction_window"
        )
        
        predicted_position = predict_next_request(requests, window_size)
        
        if predicted_position is not None:
            st.metric(
                "Predicted Next Request Position",
                f"{predicted_position:.2f}",
                delta=f"±{abs(predicted_position - requests[-1]):.2f} from last request"
            )
            
            # Plot historical and predicted values
            fig_pred = go.Figure()
            
            # Add disk boundaries
            fig_pred.add_shape(
                type="rect",
                x0=0, y0=0, x1=disk_size, y1=1,
                line=dict(color="black", width=2),
                fillcolor="rgba(200, 200, 200, 0.3)",
                layer="below"
            )
            
            # Add historical requests
            fig_pred.add_trace(go.Scatter(
                x=requests,
                y=[0.5] * len(requests),
                mode='markers',
                name='Historical Requests',
                marker=dict(size=10, color='blue')
            ))
            
            # Add predicted position
            fig_pred.add_trace(go.Scatter(
                x=[predicted_position],
                y=[0.5],
                mode='markers',
                name='Predicted Position',
                marker=dict(size=15, color='red', symbol='star')
            ))
            
            # Update layout
            fig_pred.update_layout(
                title="Request Pattern Visualization",
                xaxis_title="Disk Position",
                yaxis_title="",
                showlegend=True,
                height=300,
                yaxis=dict(showticklabels=False, range=[0, 1])
            )
            
            st.plotly_chart(fig_pred, use_container_width=True)
        else:
            st.warning("Not enough historical data to make a prediction. Please add more requests.")
    
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

show_disk_scheduling()