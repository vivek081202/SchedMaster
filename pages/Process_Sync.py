import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

st.title("🔄 Process Synchronization & Resource Allocation")
st.subheader("Implement Banker's Algorithm for deadlock avoidance")

def is_safe_state(available, max_need, allocation):
    n = len(allocation)
    m = len(available)
    work = np.array(available.copy())
    finish = [False] * n
    safe_sequence = []
    
    # Calculate need matrix
    need = np.zeros((n, m))
    for i in range(n):
        need[i] = max_need[i] - allocation[i]
    
    # Safety algorithm
    while True:
        found = False
        for i in range(n):
            if not finish[i] and all(need[i] <= work):
                work += allocation[i]
                finish[i] = True
                safe_sequence.append(i)
                found = True
        
        if not found:
            break
    
    return all(finish), safe_sequence, need

def validate_request(available, max_need, allocation, process_idx, request):
    # Check if request exceeds maximum need
    if any(request > (max_need[process_idx] - allocation[process_idx])):
        return False, "Request exceeds maximum need"
    
    # Check if request exceeds available resources
    if any(request > available):
        return False, "Request exceeds available resources"
    
    return True, "Request is valid"

def bankers_algorithm(available, max_need, allocation, process_idx=None, request=None):
    n = len(allocation)
    m = len(available)
    
    # Calculate need matrix
    need = np.zeros((n, m))
    for i in range(n):
        need[i] = max_need[i] - allocation[i]
    
    # Check if current state is safe
    is_safe, safe_sequence, _ = is_safe_state(available, max_need, allocation)
    
    # If a request is made, validate it
    if request is not None and process_idx is not None:
        is_valid, message = validate_request(available, max_need, allocation, process_idx, request)
        if not is_valid:
            return need, is_safe, safe_sequence, False, message
        
        # Simulate granting the request
        new_available = available - request
        new_allocation = allocation.copy()
        new_allocation[process_idx] += request
        new_max_need = max_need.copy()
        
        # Check if new state is safe
        new_is_safe, new_safe_sequence, _ = is_safe_state(new_available, new_max_need, new_allocation)
        
        return need, is_safe, safe_sequence, new_is_safe, new_safe_sequence
    
    return need, is_safe, safe_sequence, None, None

def show_process_sync():
    st.markdown("""
    ### Banker's Algorithm for Deadlock Avoidance
    This module implements the Banker's Algorithm to prevent deadlocks in operating systems.
    
    The algorithm works by:
    1. Checking if the current state is safe
    2. Validating resource requests against maximum needs and available resources
    3. Simulating the request to ensure the system remains in a safe state
    
    You can input the number of processes, resource types, and their respective allocations and maximum needs.
    """)
    
    # Input Section
    st.subheader("System Configuration")
    
    col1, col2 = st.columns(2)
    with col1:
        num_processes = st.number_input("Number of Processes", min_value=1, max_value=10, value=3)
    with col2:
        num_resources = st.number_input("Number of Resource Types", min_value=1, max_value=5, value=3)
    
    # Available Resources
    st.subheader("Available Resources")
    available = np.zeros(num_resources)
    for i in range(num_resources):
        available[i] = st.number_input(f"Resource {i+1} Available", min_value=0, value=10, key=f"available_{i}")
    
    # Maximum Need Matrix
    st.subheader("Maximum Need Matrix")
    max_need = np.zeros((num_processes, num_resources))
    
    for i in range(num_processes):
        st.markdown(f"**Process {i+1}**")
        cols = st.columns(num_resources)
        for j in range(num_resources):
            with cols[j]:
                max_need[i, j] = st.number_input(
                    f"Max Need for Resource {j+1}",
                    min_value=0,
                    value=5,
                    key=f"max_need_{i}_{j}"
                )
    
    # Allocation Matrix
    st.subheader("Allocation Matrix")
    allocation = np.zeros((num_processes, num_resources))
    
    for i in range(num_processes):
        st.markdown(f"**Process {i+1}**")
        cols = st.columns(num_resources)
        for j in range(num_resources):
            with cols[j]:
                max_allocation = int(max_need[i, j])
                default_value = min(2, max_allocation) if max_allocation > 0 else 0
                allocation[i, j] = st.number_input(
                    f"Allocated Resource {j+1}",
                    min_value=0,
                    max_value=max_allocation,
                    value=default_value,
                    key=f"allocation_{i}_{j}"
                )
    
    # Request Resources
    st.subheader("Request Resources")
    request_process = st.selectbox("Select Process", [f"Process {i+1}" for i in range(num_processes)])
    process_idx = int(request_process.split()[1]) - 1
    
    request = np.zeros(num_resources)
    cols = st.columns(num_resources)
    for j in range(num_resources):
        with cols[j]:
            request[j] = st.number_input(
                f"Request for Resource {j+1}",
                min_value=0,
                max_value=int(max_need[process_idx, j] - allocation[process_idx, j]),
                value=1,
                key=f"request_{j}"
            )
    
    # Run Banker's Algorithm
    if st.button("Check Safety"):
        # Calculate need matrix and check safety
        need, is_safe, safe_sequence, new_is_safe, new_safe_sequence = bankers_algorithm(
            available, max_need, allocation, process_idx, request
        )
        
        # Display results
        st.subheader("Algorithm Results")
        
        # Display Need Matrix
        st.markdown("**Need Matrix**")
        need_df = pd.DataFrame(
            need,
            index=[f"Process {i+1}" for i in range(num_processes)],
            columns=[f"Resource {i+1}" for i in range(num_resources)]
        )
        st.dataframe(need_df)
        
        # Display current state safety
        if is_safe:
            st.success("✅ Current System State: Safe")
            st.write("A safe sequence exists where all processes can complete:")
            st.write("Safe sequence:", [f"Process {i+1}" for i in safe_sequence])
        else:
            st.error("❌ Current System State: Unsafe")
            st.write("No safe sequence exists. The system is in a deadlock-prone state.")
        
        # Display request validation results
        if new_is_safe is not None:
            st.subheader("Request Analysis")
            
            # Display the specific request details
            st.write(f"**Request Details:**")
            request_details = pd.DataFrame(
                [request],
                columns=[f"Resource {i+1}" for i in range(num_resources)],
                index=[f"Process {process_idx+1} Request"]
            )
            st.dataframe(request_details)
            
            if new_is_safe:
                st.success("✅ Request Status: Can be granted")
                st.write("The request can be safely granted. New safe sequence:", [f"Process {i+1}" for i in new_safe_sequence])
            else:
                st.error("❌ Request Status: Cannot be granted")
                
                # Check why the request cannot be granted
                if any(request > (max_need[process_idx] - allocation[process_idx])):
                    st.error("Reason: Request exceeds maximum need")
                    st.write("Maximum remaining need:", max_need[process_idx] - allocation[process_idx])
                elif any(request > available):
                    st.error("Reason: Not enough available resources")
                    st.write("Available resources:", available)
                else:
                    st.error("Reason: Granting this request would lead to an unsafe state")
                
                # Show the order of requests that cannot be granted
                st.write("\n**Request Order Analysis:**")
                st.write("1. Current request from Process", process_idx + 1, "cannot be granted")
                st.write("2. This would prevent the following safe sequence:", [f"Process {i+1}" for i in safe_sequence])
                
                # Show what would happen if the request was granted
                st.write("\n**If granted, the system would:**")
                st.write("- Enter an unsafe state")
                st.write("- Potentially lead to deadlock")
                st.write("- Not guarantee all processes can complete")
        
        # Visualization
        st.subheader("Resource Allocation Visualization")
        
        # Create a stacked bar chart for resource allocation
        fig = go.Figure()
        
        # Add allocated resources
        for i in range(num_processes):
            fig.add_trace(go.Bar(
                name=f"Process {i+1} Allocated",
                x=[f"Resource {j+1}" for j in range(num_resources)],
                y=allocation[i],
                text=allocation[i],
                textposition='auto',
            ))
        
        # Add available resources
        fig.add_trace(go.Bar(
            name="Available",
            x=[f"Resource {j+1}" for j in range(num_resources)],
            y=available,
            text=available,
            textposition='auto',
        ))
        
        fig.update_layout(
            title="Resource Allocation and Availability",
            xaxis_title="Resource Type",
            yaxis_title="Amount",
            barmode='stack',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Create a pie chart for resource distribution
        fig = go.Figure()
        
        # Calculate total allocated and available resources
        total_allocated = np.sum(allocation, axis=0)
        total_available = available
        
        fig.add_trace(go.Pie(
            labels=[f"Resource {i+1}" for i in range(num_resources)],
            values=total_allocated + total_available,
            hole=.3,
            name="Total Resources"
        ))
        
        fig.update_layout(
            title="Resource Distribution",
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
show_process_sync() 