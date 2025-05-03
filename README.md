# ⏱️ SchedMaster

> **Intelligent Scheduling & Optimization Simulation tool using Machine Intelligence**

SchedMaster is an advanced simulation tool designed to optimize CPU scheduling, disk scheduling, and resource allocation by applying cutting-edge Design and Analysis of Algorithms (DAA) techniques. This project leverages powerful methods such as Dynamic Programming (DP), Greedy Algorithms, and Backtracking to solve resource scheduling challenges efficiently.

## 🌐 Live Demo

Try out SchedMaster online: [Live Demo](https://your-schedmaster-url.com)

## 🚀 Features

### 1. CPU Scheduling Module
- **Algorithms Implemented**:
  - First Come First Serve (FCFS)
  - Shortest Job First (SJF) (Premptive)
  - Priority Scheduling (Premptive)
  - Round Robin (RR)
  - Shortest Remaining Time First (SRTF)
- **ML Techniques**:
  - Supervised Learning for execution time prediction
  - Greedy algorithm optimization
  - Performance pattern analysis using clustering
  - Linear Regression

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

### 3. Process Synchronization Module
- **Problems Solved**:
  - Producer-Consumer Problem
  - Reader-Writer Problem
  - Dining Philosophers Problem
- **ML Techniques**:
  - Resource usage prediction
  - Deadlock prevention using pattern recognition
  - Performance optimization through learning

### 4. Anomaly Detection Module
- **Features**:
  - Real-time anomaly detection
  - Performance analysis
  - Resource usage monitoring
- **ML Techniques**:
  - Unsupervised learning for anomaly detection (Isolation Forest)
  - Time series analysis
  - Pattern recognition in resource usage

### 5. Comparative Analysis Module
- **Features**:
  - Side-by-side algorithm comparison
  - Performance metrics visualization
  - Interactive parameter tuning
- **ML Techniques**:
  - Performance prediction models
  - Algorithm selection optimization
  - Pattern recognition in performance metrics

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