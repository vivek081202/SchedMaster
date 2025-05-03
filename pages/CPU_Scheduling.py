import streamlit as st
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import plotly.graph_objects as go
import plotly.express as px

def predict_execution_time(historical_data):
    if len(historical_data) < 2:
        return None
    
    X = np.array(range(len(historical_data))).reshape(-1, 1)
    y = np.array(historical_data)
    model = LinearRegression()
    model.fit(X, y)
    next_time = model.predict([[len(historical_data)]])[0]
    return max(0, next_time)

def fcfs_scheduling(processes):
    n = len(processes)
    waiting_time = [0] * n
    turnaround_time = [0] * n
    completion_time = [0] * n
    current_time = 0
    
    # Sort processes by arrival time
    processes = sorted(processes, key=lambda x: x[1])
    
    for i in range(n):
        if processes[i][1] > current_time:
            current_time = processes[i][1]
        
        waiting_time[i] = max(0, current_time - processes[i][1])
        completion_time[i] = current_time + processes[i][2]
        turnaround_time[i] = completion_time[i] - processes[i][1]
        current_time = completion_time[i]
    
    return waiting_time, turnaround_time, completion_time

def round_robin_scheduling(processes, time_quantum):
    n = len(processes)
    waiting_time = [0] * n
    turnaround_time = [0] * n
    completion_time = [0] * n
    remaining_time = [p[2] for p in processes]  # Copy burst times
    arrival_time = [p[1] for p in processes]
    current_time = 0
    queue = []
    gantt_data = []  # To store process execution timeline
    
    # Sort processes by arrival time
    sorted_indices = sorted(range(n), key=lambda x: arrival_time[x])
    processes = [processes[i] for i in sorted_indices]
    remaining_time = [remaining_time[i] for i in sorted_indices]
    arrival_time = [arrival_time[i] for i in sorted_indices]
    
    # Initialize queue with processes that have arrived
    for i in range(n):
        if arrival_time[i] <= current_time:
            queue.append(i)
    
    while True:
        if not queue:
            # If queue is empty but processes are remaining
            if any(rt > 0 for rt in remaining_time):
                # Find next process to arrive
                next_arrival = min([arrival_time[i] for i in range(n) if remaining_time[i] > 0 and arrival_time[i] > current_time])
                current_time = next_arrival
                # Add processes that have arrived
        for i in range(n):
                    if arrival_time[i] <= current_time and remaining_time[i] > 0 and i not in queue:
                        queue.append(i)
                else:
                break
        
        if not queue:
            break
    
        # Get next process from queue
        current_process = queue.pop(0)
        
        # Calculate execution time for this quantum
        exec_time = min(time_quantum, remaining_time[current_process])
        
        # Record process execution in Gantt chart
        gantt_data.append({
            'Process': f'P{current_process + 1}',
            'Start': current_time,
            'Finish': current_time + exec_time
        })
        
        # Update remaining time
        remaining_time[current_process] -= exec_time
        
        # Update waiting time for other processes in queue
        for process in queue:
            waiting_time[process] += exec_time
        
        # Update current time
        current_time += exec_time
        
        # Add newly arrived processes to queue
        for i in range(n):
            if arrival_time[i] <= current_time and remaining_time[i] > 0 and i not in queue and i != current_process:
                queue.append(i)
        
        # If process still has remaining time, add it back to queue
        if remaining_time[current_process] > 0:
            queue.append(current_process)
        else:
            # Process completed
            completion_time[current_process] = current_time
            turnaround_time[current_process] = completion_time[current_process] - arrival_time[current_process]
            # Waiting time is already calculated during execution
    
    return waiting_time, turnaround_time, completion_time, gantt_data

def sjn_scheduling(processes):
    n = len(processes)
    processes = sorted(processes, key=lambda x: x[1])  # Sort by arrival time
    waiting_time = [0] * n
    turnaround_time = [0] * n
    completion_time = [0] * n
    current_time = 0
    remaining_processes = processes.copy()
    
    while remaining_processes:
        # Find processes that have arrived
        arrived_processes = [p for p in remaining_processes if p[1] <= current_time]
        
        if not arrived_processes:
            # If no processes have arrived, move time to next arrival
            next_arrival = min(p[1] for p in remaining_processes)
            current_time = next_arrival
            continue
        
        # Find the process with shortest burst time among arrived processes
        next_process = min(arrived_processes, key=lambda x: x[2])
        process_index = processes.index(next_process)
        
        waiting_time[process_index] = max(0, current_time - next_process[1])
        completion_time[process_index] = current_time + next_process[2]
        turnaround_time[process_index] = completion_time[process_index] - next_process[1]
        current_time = completion_time[process_index]
        
        remaining_processes.remove(next_process)
    
    return waiting_time, turnaround_time, completion_time

def priority_scheduling(processes):
    n = len(processes)
    waiting_time = [0] * n
    turnaround_time = [0] * n
    completion_time = [0] * n
    current_time = 0
    remaining_processes = processes.copy()
    
    while remaining_processes:
        # Find processes that have arrived
        arrived_processes = [p for p in remaining_processes if p[1] <= current_time]
        
        if not arrived_processes:
            # If no processes have arrived, move time to next arrival
            next_arrival = min(p[1] for p in remaining_processes)
            current_time = next_arrival
            continue
        
        # Find the process with highest priority (lowest priority number) among arrived processes
        next_process = min(arrived_processes, key=lambda x: x[3])
        process_index = processes.index(next_process)
        
        waiting_time[process_index] = max(0, current_time - next_process[1])
        completion_time[process_index] = current_time + next_process[2]
        turnaround_time[process_index] = completion_time[process_index] - next_process[1]
        current_time = completion_time[process_index]
        
        remaining_processes.remove(next_process)
    
    return waiting_time, turnaround_time, completion_time

def validate_scheduling_results(processes, waiting_time, turnaround_time, completion_time):
    """Validate scheduling results for accuracy."""
    n = len(processes)
    errors = []
    
    # Validate waiting time
    for i in range(n):
        if waiting_time[i] < 0:
            errors.append(f"Process {processes[i][0]} has negative waiting time: {waiting_time[i]}")
        
        # Check if waiting time is reasonable
        if waiting_time[i] > completion_time[i] - processes[i][1]:
            errors.append(f"Process {processes[i][0]} has invalid waiting time: {waiting_time[i]}")
    
    # Validate turnaround time
    for i in range(n):
        if turnaround_time[i] < processes[i][2]:
            errors.append(f"Process {processes[i][0]} has turnaround time less than burst time")
        
        # Check if turnaround time matches completion - arrival
        if turnaround_time[i] != completion_time[i] - processes[i][1]:
            errors.append(f"Process {processes[i][0]} has incorrect turnaround time calculation")
    
    # Validate completion time
    for i in range(n):
        if completion_time[i] < processes[i][1] + processes[i][2]:
            errors.append(f"Process {processes[i][0]} has completion time less than arrival + burst time")
    
    return errors

def compare_algorithms(processes, time_quantum=2):
    """Compare different scheduling algorithms for the same set of processes."""
    results = {}
    
    # Run FCFS
    waiting_time, turnaround_time, completion_time = fcfs_scheduling(processes)
    results['FCFS'] = {
        'avg_waiting': sum(waiting_time) / len(waiting_time),
        'avg_turnaround': sum(turnaround_time) / len(turnaround_time),
        'waiting_times': waiting_time,
        'turnaround_times': turnaround_time
    }
    
    # Run SJN
    waiting_time, turnaround_time, completion_time = sjn_scheduling(processes)
    results['SJN'] = {
        'avg_waiting': sum(waiting_time) / len(waiting_time),
        'avg_turnaround': sum(turnaround_time) / len(turnaround_time),
        'waiting_times': waiting_time,
        'turnaround_times': turnaround_time
    }
    
    # Run Priority
    waiting_time, turnaround_time, completion_time = priority_scheduling(processes)
    results['Priority'] = {
        'avg_waiting': sum(waiting_time) / len(waiting_time),
        'avg_turnaround': sum(turnaround_time) / len(turnaround_time),
        'waiting_times': waiting_time,
        'turnaround_times': turnaround_time
    }
    
    # Run Round Robin
    waiting_time, turnaround_time, completion_time, _ = round_robin_scheduling(processes, time_quantum)
    results['Round Robin'] = {
        'avg_waiting': sum(waiting_time) / len(waiting_time),
        'avg_turnaround': sum(turnaround_time) / len(turnaround_time),
        'waiting_times': waiting_time,
        'turnaround_times': turnaround_time
    }
    
    return results

def show_algorithm_comparison(processes, time_quantum=2):
    """Display comparison of different scheduling algorithms."""
    results = compare_algorithms(processes, time_quantum)
    
    # Create comparison charts
    fig = go.Figure()
    
    # Add waiting time comparison
    fig.add_trace(go.Bar(
        name='Average Waiting Time',
        x=list(results.keys()),
        y=[results[algo]['avg_waiting'] for algo in results],
        text=[f"{results[algo]['avg_waiting']:.2f}" for algo in results],
        textposition='auto',
    ))
    
    # Add turnaround time comparison
    fig.add_trace(go.Bar(
        name='Average Turnaround Time',
        x=list(results.keys()),
        y=[results[algo]['avg_turnaround'] for algo in results],
        text=[f"{results[algo]['avg_turnaround']:.2f}" for algo in results],
        textposition='auto',
    ))
    
    fig.update_layout(
        title='Algorithm Comparison',
        xaxis_title='Scheduling Algorithm',
        yaxis_title='Time Units',
        barmode='group',
        height=400
    )
    
    return fig

def show_cpu_scheduling():
    st.title("🖥️ CPU Scheduling Optimization with Greedy Algorithms & ML")
    st.markdown("### ⚡ Shortest Job Next (SJN) and Priority Scheduling using Greedy Strategy")
    
    # Algorithm Selection
    algorithm = st.selectbox(
        "Select Scheduling Algorithm",
        ["First Come First Serve (FCFS)", "Round Robin", "Shortest Job Next (SJN)", "Priority Scheduling"]
    )
    
    # Process Input
    st.subheader("Process Details")
    num_processes = st.number_input("Number of Processes", min_value=1, max_value=10, value=3)
    
    # Time Quantum for Round Robin
    time_quantum = 1
    if algorithm == "Round Robin":
        time_quantum = st.number_input("Time Quantum", min_value=1, value=2)
    
    processes = []
    for i in range(num_processes):
        if algorithm == "Priority Scheduling":
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                pid = st.text_input(f"Process ID {i+1}", value=f"P{i+1}")
            with col2:
                arrival_time = st.number_input(f"Arrival Time {i+1}", min_value=0, value=0)
            with col3:
                burst_time = st.number_input(f"Burst Time {i+1}", min_value=1, value=1)
            with col4:
                priority = st.number_input(f"Priority {i+1}", min_value=0, value=i)
            processes.append([pid, arrival_time, burst_time, priority])
        else:
            col1, col2, col3 = st.columns(3)
            with col1:
                pid = st.text_input(f"Process ID {i+1}", value=f"P{i+1}")
            with col2:
                arrival_time = st.number_input(f"Arrival Time {i+1}", min_value=0, value=0)
            with col3:
                burst_time = st.number_input(f"Burst Time {i+1}", min_value=1, value=1)
            processes.append([pid, arrival_time, burst_time, 0])  # Default priority 0 for other algorithms
    
    if st.button("Calculate Schedule"):
        # Run selected algorithm
        if algorithm == "First Come First Serve (FCFS)":
            waiting_time, turnaround_time, completion_time = fcfs_scheduling(processes)
        elif algorithm == "Round Robin":
            waiting_time, turnaround_time, completion_time, gantt_data = round_robin_scheduling(processes, time_quantum)
        elif algorithm == "Shortest Job Next (SJN)":
            waiting_time, turnaround_time, completion_time = sjn_scheduling(processes)
        else:
            waiting_time, turnaround_time, completion_time = priority_scheduling(processes)
        
        # Validate results
        errors = validate_scheduling_results(processes, waiting_time, turnaround_time, completion_time)
        if errors:
            st.error("Validation Errors Found:")
            for error in errors:
                st.error(error)
        
        # Display Results
        st.subheader("Scheduling Results")
        
        # Create DataFrame for results
        results = []
        for i in range(len(processes)):
            results.append({
                "Process": processes[i][0],
                "Arrival Time": processes[i][1],
                "Burst Time": processes[i][2],
                "Priority": processes[i][3],
                "Waiting Time": waiting_time[i],
                "Turnaround Time": turnaround_time[i],
                "Completion Time": completion_time[i]
            })
        
        df = pd.DataFrame(results)
        st.dataframe(df)
        
        # Calculate and display metrics
        avg_waiting_time = sum(waiting_time) / len(waiting_time)
        avg_turnaround_time = sum(turnaround_time) / len(turnaround_time)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Average Waiting Time", f"{avg_waiting_time:.2f}")
        with col2:
            st.metric("Average Turnaround Time", f"{avg_turnaround_time:.2f}")
        
        # Enhanced Gantt Chart
        st.subheader("Process Execution Timeline (Gantt Chart)")
        
        # Create a simple Gantt chart using plotly.graph_objects
        fig = go.Figure()
        
        # Add bars for each process
        for i in range(len(processes)):
            # Add waiting period if any
            if waiting_time[i] > 0:
                fig.add_trace(go.Bar(
                    name=f"{processes[i][0]} (Waiting)",
                    x=[waiting_time[i]],
                    y=[processes[i][0]],
                    base=[processes[i][1]],  # Start from arrival time
                    marker_color='lightgray',
                    showlegend=True
                ))
            
            # Add execution period
            fig.add_trace(go.Bar(
                name=f"{processes[i][0]} (Execution)",
                x=[processes[i][2]],  # Burst time
                y=[processes[i][0]],
                base=[completion_time[i] - processes[i][2]],  # Start of execution
                marker_color=px.colors.qualitative.Set1[i % len(px.colors.qualitative.Set1)],
                showlegend=True
            ))
        
        # Update layout
        fig.update_layout(
            title="Process Execution Timeline",
            xaxis_title="Time Units",
            yaxis_title="Process",
            barmode='stack',
            height=400,
            showlegend=True,
            xaxis=dict(
                tickmode='linear',
                tick0=0,
                dtick=1,
                range=[0, max(completion_time) + 1]
            ),
            yaxis=dict(
                autorange="reversed"
            )
        )
        
        # Add annotations for waiting and turnaround times
        for i in range(len(processes)):
            fig.add_annotation(
                x=completion_time[i],
                y=processes[i][0],
                text=f'WT: {waiting_time[i]}<br>TT: {turnaround_time[i]}',
                showarrow=False,
                font=dict(size=10),
                xanchor='left',
                yanchor='middle'
            )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Algorithm Comparison
        st.subheader("Algorithm Comparison")
        comparison_fig = show_algorithm_comparison(processes, time_quantum)
        st.plotly_chart(comparison_fig, use_container_width=True)
        
        # Process Timeline Visualization
        st.subheader("Detailed Process Timeline")
        fig_timeline = go.Figure()
        
        for i in range(len(processes)):
            # Waiting period
            fig_timeline.add_trace(go.Bar(
                name=f"{processes[i][0]} (Waiting)",
                x=[processes[i][1]],
                y=[1],
                width=[waiting_time[i]],
                marker_color='lightgray',
                showlegend=True
            ))
            
            # Execution period
            fig_timeline.add_trace(go.Bar(
                name=f"{processes[i][0]} (Execution)",
                x=[completion_time[i] - processes[i][2]],
                y=[1],
                width=[processes[i][2]],
                marker_color=px.colors.qualitative.Set1[i % len(px.colors.qualitative.Set1)],
                showlegend=True
            ))
        
        fig_timeline.update_layout(
            title="Process Timeline (Including Waiting and Execution Times)",
            xaxis_title="Time Units",
            yaxis_title="",
            height=300,
            barmode='stack',
            bargap=0.1,
            bargroupgap=0.1
        )
        st.plotly_chart(fig_timeline, use_container_width=True)
        
        # ML Prediction Section
        st.subheader("ML-based Execution Time Prediction")
        historical_data = [p[2] for p in processes]  # Using burst times as historical data
        predicted_time = predict_execution_time(historical_data)
        
        if predicted_time is not None:
            st.metric("Predicted Next Process Execution Time", f"{predicted_time:.2f}")
            
            # Plot historical and predicted values
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=list(range(len(historical_data))),
                y=historical_data,
                mode='lines+markers',
                name='Historical Data'
            ))
            fig.add_trace(go.Scatter(
                x=[len(historical_data)],
                y=[predicted_time],
                mode='markers',
                marker=dict(size=10, color='red'),
                name='Predicted'
            ))
            
            fig.update_layout(
                title="Execution Time Trend",
                xaxis_title="Process Number",
                yaxis_title="Execution Time",
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


show_cpu_scheduling()