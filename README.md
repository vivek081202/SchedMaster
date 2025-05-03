# ⏱️ SchedMaster

> **Intelligent Scheduling & Optimization Simulation tool using Machine Intelligence**

![image](https://github.com/user-attachments/assets/4f8acabf-6c87-41ba-b700-abc5831804fc)

In modern operating systems, efficient resource management and process scheduling play a crucial role in maintaining system performance, responsiveness, and stability. However, traditional scheduling techniques often rely on static algorithms that fail to adapt dynamically to varying workloads, resource availability, or process behavior.

SchedMaster is an intelligent simulation and optimization tool designed to overcome these limitations by integrating the principles of Design and Analysis of Algorithms (DAA) and basic Machine Learning (ML) techniques. It provides an interactive environment where users can visualize, analyze, and optimize CPU scheduling, disk scheduling, and resource allocation strategies.

The uniqueness of SchedMaster lies in its hybrid approach — combining classical scheduling algorithms with optimization techniques like Greedy Algorithms, Dynamic Programming, and Backtracking. Additionally, it leverages simple ML models to predict process behavior, detect anomalies in resource usage, and recommend the most suitable scheduling strategy for given conditions. This project aims to not only simulate existing scheduling methods but also empower users to experiment, analyze time & space complexities, and explore adaptive scheduling solutions that reflect real-world scenarios more effectively.

## 🚀 Features

### 1. CPU Scheduling Module
- **Algorithms Implemented**:
  - First Come First Serve (FCFS)
  - Priority Scheduling (Premptive)
  - Round Robin (RR)
  - Shortest Remaining Time First (SRTF)
- **ML Techniques**:
  - Supervised Learning for execution time prediction
  - Greedy algorithm optimization
  - Performance pattern analysis using clustering
  - Linear Regression
 
  ![image](https://github.com/user-attachments/assets/123295d8-2cec-475d-888f-96f3009ae46a)


### 2. Disk Scheduling Module
- **Algorithms Implemented**:
  - First Come First Serve (FCFS)
  - Shortest Seek Time First (SSTF)
  - SCAN
  - C-SCAN
  - LOOK
  - C-LOOK
- **ML Techniques**:
  - Pattern recognition for disk access prediction
  - Dynamic programming for optimal path finding
  - Time series analysis for access pattern prediction
 
  ![image](https://github.com/user-attachments/assets/5e86c592-6e33-4925-902a-650a9f8b8d58)

### 3. Process Synchronization Module
- **Problems Solved**:
  - Producer-Consumer Problem
  - Reader-Writer Problem
  - Dining Philosophers Problem
- **ML Techniques**:
  - Resource usage prediction
  - Deadlock prevention using pattern recognition
  - Performance optimization through learning
 
  ![image](https://github.com/user-attachments/assets/ad2dad77-c564-41d2-a792-8d6ca75b9b87)


### 4. Anomaly Detection Module
- **Features**:
  - Real-time anomaly detection
  - Performance analysis
  - Resource usage monitoring
- **ML Techniques**:
  - Unsupervised learning for anomaly detection (Isolation Forest)
  - Time series analysis
  - Pattern recognition in resource usage
 
  ![image](https://github.com/user-attachments/assets/9df53536-35c2-452a-8055-9a56aa12c4d3)


### 5. Comparative Analysis Module
- **Features**:
  - Side-by-side algorithm comparison
  - Performance metrics visualization
  - Interactive parameter tuning
- **ML Techniques**:
  - Performance prediction models
  - Algorithm selection optimization
  - Pattern recognition in performance metrics
 
  ![image](https://github.com/user-attachments/assets/f5e2c56d-31a2-4119-8c38-8c190a66a378)
  <br>
  ![image](https://github.com/user-attachments/assets/62b1d57b-3fae-409a-be13-036c30ab131b)

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- Git
- pip (Python package installer)

### Step-by-Step Installation

1. **Clone the Repository**
```bash
# Clone using HTTPS
git clone https://github.com/yourusername/SchedMaster.git

# Or clone using SSH
git clone git@github.com:yourusername/SchedMaster.git

# Navigate to project directory
cd SchedMaster
```

2. **Create and Activate Virtual Environment (Recommended)**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

3. **Install Dependencies**
```bash
# Install required packages
pip install -r requirements.txt

# Verify installation
pip list
```

4. **Run the Application**
```bash
# Start the Streamlit app
streamlit run pages/app.py
```

5. **Access the Application**
- Open your web browser
- Navigate to `http://localhost:8501`
- The application should be running and ready to use

### Troubleshooting

If you encounter any issues during installation:

1. **Python Version Issues**
```bash
# Check Python version
python --version

# If version is below 3.8, install a newer version
```

2. **Dependency Conflicts**
```bash
# Create a fresh virtual environment
python -m venv venv --clear

# Reinstall dependencies
pip install -r requirements.txt
```

3. **Streamlit Issues**
```bash
# Update Streamlit
pip install --upgrade streamlit

# Clear Streamlit cache
streamlit cache clear
```

## 🚀 Usage

```bash
# Run the Streamlit app
streamlit run pages/app.py
```

Open your web browser and navigate to `http://localhost:8501`

## 📁 Project Structure

```
SchedMaster/
├── data/               # Data files and datasets
├── images/            # Static images and icons
├── modules/           # Core algorithm implementations
├── pages/             # Streamlit pages
│   ├── app.py         # Main application entry point
│   ├── Home.py        # Home page
│   ├── CPU_Scheduling.py
│   ├── Disk_Scheduling.py
│   ├── Process_Sync.py
│   ├── Anomaly_Detection.py
│   └── Comparative_Analysis.py
└── requirements.txt   # Python dependencies
```

## 📦 Dependencies

- streamlit
- numpy
- pandas
- plotly
- scikit-learn
- streamlit-extras
- matplotlib
- seaborn

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Streamlit for the amazing web application framework
- Scikit-learn for machine learning capabilities
- Plotly for interactive visualizations
- All contributors who have helped shape this project

### Designed and Developed by:
> **Vivek Kumar Singh**
> [LinkedIn](https://www.linkedin.com/in/vivek-singh-858941201/)
