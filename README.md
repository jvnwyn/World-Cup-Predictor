# ⚽ MyFootballCompanion – FIFA World Cup Prediction System

A machine learning-powered football analytics application that predicts international match outcomes and simulates FIFA World Cup tournaments using historical match data, Elo ratings, team form, and performance statistics.

## 📖 Overview

MyFootballCompanion is designed to analyze international football teams and forecast match results through a data-driven approach. The system leverages historical match records, team performance metrics, and Elo ratings to train a predictive model capable of estimating match outcomes and simulating entire World Cup group stages.

The project demonstrates the application of machine learning, feature engineering, and sports analytics in football prediction.

---

## 🚀 Features

* Predicts football match outcomes (Home Win, Draw, Away Win)
* Uses Elo ratings to measure team strength
* Incorporates recent team form and goal statistics
* Generates team performance metrics automatically
* Simulates FIFA World Cup group-stage matches
* Produces tournament standings and rankings
* Trained using historical international football match data
* Reusable machine learning pipeline for future tournaments

---

## 🛠️ Technologies Used

* Python
* Pandas
* NumPy
* Scikit-learn
* Logistic Regression
* Pickle
* CSV Data Processing

---

## 📂 Project Structure

```text
WorldCupPredictor/
│
├── data/
│   ├── results.csv
│   ├── latest_elo.csv
│   ├── team_stats.csv
│   ├── worldcup_elo.csv
│   └── worldcup_team_stats.csv
│
├── models/
│   ├── logistic_model.pkl
│   └── scaler.pkl
│
├── src/
│   ├── train_model.py
│   ├── predict_match.py
│   ├── group_stage_simulator.py
│   └── generate_worldcup_team_stats.py
│
└── main.py
```

---

## ⚙️ How It Works

### 1. Data Collection

Historical international football match results are collected and processed to build the training dataset.

Data includes:

* Match dates
* Home and away teams
* Goals scored
* Match venues
* Historical results

---

### 2. Feature Engineering

The model generates predictive features from historical performance data.

#### Elo Rating Difference

Measures the relative strength of two teams using a custom Elo rating system.

#### Recent Form Difference

Calculates performance based on the team's most recent matches.

#### Goal Performance Difference

Compares average goals scored and conceded between competing teams.

---

### 3. Model Training

The system trains a Logistic Regression classifier using engineered features.

#### Input Features

| Feature         | Description                        |
| --------------- | ---------------------------------- |
| Elo Difference  | Team strength comparison           |
| Form Difference | Recent performance comparison      |
| Goal Difference | Offensive and defensive comparison |

#### Predicted Outcomes

| Class | Outcome  |
| ----- | -------- |
| 0     | Away Win |
| 1     | Draw     |
| 2     | Home Win |

---

### 4. Match Prediction

The trained model generates outcome probabilities for any selected matchup.

Example:

```text
Japan vs Netherlands

Prediction: Netherlands Win

Probabilities:
Japan Win: 22.1%
Draw: 24.5%
Netherlands Win: 53.4%
```

---

### 5. Tournament Simulation

The simulator:

* Generates group-stage fixtures
* Predicts all matches
* Awards points
* Produces final standings

Scoring System:

```text
Win  = 3 Points
Draw = 1 Point
Loss = 0 Points
```

---

## 📊 Machine Learning Pipeline

```text
Historical Match Data
          ↓
Feature Engineering
          ↓
Elo Rating Calculation
          ↓
Data Scaling
          ↓
Logistic Regression Training
          ↓
Outcome Prediction
          ↓
Tournament Simulation
```

---

## 💻 Installation

### Clone the Repository

```bash
git clone https://github.com/yourusername/MyFootballCompanion.git
cd MyFootballCompanion
```

### Create a Virtual Environment

```bash
python -m venv venv
```

Activate the environment:

**Windows**

```bash
venv\Scripts\activate
```

**Mac/Linux**

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Project

### Train the Model

```bash
python src/train_model.py
```

### Predict a Match

```bash
python src/predict_match.py
```

### Simulate a World Cup Group Stage

```bash
python src/group_stage_simulator.py
```

---

## 📈 Future Improvements

* Support for knockout-stage simulations
* Advanced machine learning models (XGBoost, Random Forest, Neural Networks)
* Live API integration for real-time team data
* Interactive dashboard and visualizations
* Player-level analytics
* Expected Goals (xG) metrics
* Full FIFA World Cup tournament simulation

---

## 🎯 Learning Outcomes

This project demonstrates:

* Machine Learning Classification
* Sports Analytics
* Data Preprocessing
* Feature Engineering
* Model Evaluation
* Python Software Development
* Predictive Modeling

---

## 👨‍💻 Author

**Jovan Wayne B. Andrade**

Bachelor of Science in Computer Science

Interested in Machine Learning, Data Analytics, Sports Analytics, and Software Development.

---

## 📄 License

This project is intended for educational, research, and portfolio purposes.
