# 🏋️ Fitness Retention Analytics Dashboard

A data-driven analytics dashboard to understand **user engagement, retention, and churn** in a fitness application.

---

## 🚀 Overview

This project helps analyze fitness app user behavior by answering key questions:

- Are users staying active?
- When do users drop off?
- Who appears likely to churn based on inactivity rules?
- Are there unusual usage patterns?

It transforms raw workout data into actionable insights using analytics and visualization.

---

## 🧩 Features

### 📥 Data Handling
- Upload your own dataset (CSV)
- Use sample dataset for quick demo
- Data validation and cleaning

### 📊 Analytics Dashboard
- Total Users
- Churn Rate
- Average Workouts per User
- Daily Activity Trends
- Workout Distribution

### 🔍 Filters
- Date range filtering
- User-level filtering
- Fully dynamic dashboard updates

### 📈 Advanced Analytics
- **Cohort Retention Analysis**
- **Anomaly Detection**
- **Heuristic Churn Labeling**

### 📤 Export
- Download processed dataset as CSV

---

## 🏗️ Project Structure
```text
.
├── dashboard/
│   └── app.py
├── scripts/
│   ├── clean_data.py
│   └── generate_data.py
├── src/
│   ├── anomaly.py
│   ├── churn.py
│   ├── data_cleaning.py
│   ├── data_preprocessing.py
│   ├── data_validation.py
│   ├── eda.py
│   ├── feature_engineering.py
│   ├── model.py
│   └── retention.py
├── data/
│   └── raw/ (generated after running scripts/generate_data.py)
└── README.md
```

---

## ⚙️ Tech Stack

- **Python**
- **Pandas** (data processing)
- **Streamlit** (dashboard UI)

---

## ▶️ How to Run

### 1. Clone the Repository
```bash
git clone https://github.com/kalviumcommunity/SW2627-Data-Product-Fitness-Retention-Analytics.git
cd SW2627-Data-Product-Fitness-Retention-Analytics
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Generate Sample Dataset
```bash
python scripts/generate_data.py
```

### 4. Run the App
```bash
streamlit run dashboard/app.py
```

---

### 📊 Key Concepts Used
- Cohort Analysis (Retention)
- Rule-based Anomaly Detection
- Heuristic Churn Labeling
- Data Cleaning & Feature Engineering
- Interactive Dashboards

### 🧠 Future Improvements
- ML-based churn prediction
- Real-time data processing
- Heatmaps for retention visualization
- User segmentation (beginner vs advanced)
- Notifications for high-risk users

### 👥 Team
- Sujaykiran
- Jevin Josh
- Manuel Jemimah Mary
- Sarvesh

---

## 📌 Conclusion

This project demonstrates how raw data can be transformed into meaningful insights that help improve user retention and engagement in fitness applications.

___