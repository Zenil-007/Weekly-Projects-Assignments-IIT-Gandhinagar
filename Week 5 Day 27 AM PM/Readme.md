# ZeptoFresh — Exploratory Data Analysis (EDA) Project

**Course:** PG Diploma in AI-ML & Agentic AI Engineering
**Institution:** IIT Gandhinagar
**Assignment:** Week 05 · Day 27 (AM/PM)
**Topic:** Exploratory Data Analysis for Late Delivery Risk Prediction

---

## 📌 Project Overview

ZeptoFresh operates a 15-minute delivery model across multiple Indian cities. The company wants to understand delivery patterns and customer behavior before building a predictive model to estimate **late delivery risk**.

This project performs Exploratory Data Analysis (EDA) on 110,000+ order records to uncover data quality issues, patterns, and operational insights.

---

## 🎯 Objectives

* Identify and fix data quality issues.
* Understand distributions and outliers in delivery time, order value, and customer metrics.
* Analyze correlations between delivery performance and refunds, ratings, and weather.
* Explore delivery time patterns across cities.
* Engineer useful features for late-delivery prediction.

---

## 📂 Repository Structure

```
zeptofresh-eda/
│
├── data/
│   └── zepto_orders.csv           # Raw dataset
│
├── notebooks/
│   └── eda.ipynb                  # EDA notebook
│
├── src/
│   ├── cleaning.py                # Data cleaning functions
│   ├── feature_engineering.py     # Feature creation utilities
│
├── README.md                      # Project documentation
└── requirements.txt               # Python dependencies
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone <your-repo-link>
cd zeptofresh-eda
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate      # Mac/Linux
venv\Scripts\activate         # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Notebook

Open Jupyter:

```bash
jupyter notebook
```

Then open:

```
notebooks/eda.ipynb
```

---

## 📊 Dataset Features

Key fields include:

* `delivery_time_mins`
* `order_value_Rs`
* `prep_time_mins`
* `rider_distance_km`
* `customer_rating`
* `rain_flag`
* `refund_issued`
* `tip_amount_Rs`
* `order_hour`
* `is_weekend`

---

## 🔍 Key EDA Findings

### Data Quality Issues Identified

* Invalid delivery times (`0` minutes).
* Negative preparation times.
* Missing or invalid customer ratings (`0`, nulls).
* Extreme order value outliers.

### Distribution Insights

* Delivery time is right-skewed.
* Bimodal delivery time pattern in Tier-1 cities.

### Correlation Observations

* Strong positive correlation between `delivery_time_mins` and `refund_issued`.
* Weather and tips influence customer ratings and delivery performance.

---

## 🧠 Feature Engineering

Examples of new features created:

* `delivery_speed = rider_distance_km / delivery_time_mins`
* `delay_ratio = delivery_time_mins / prep_time_mins`
* `high_value_order = order_value_Rs > threshold`

---

## 🧪 Modeling Readiness

This project prepares the dataset for downstream machine learning tasks such as:

* Late delivery risk prediction
* Customer churn modeling
* Operational optimization

---

## 🧾 Grading Alignment

This project follows the evaluation rubric:

* ✔ Mandatory EDA tasks completed
* ✔ Clean, modular, and documented code
* ✔ Clear Git structure and README
* ✔ Feature engineering included

---

## 👨‍💻 Author

**Name:** <Zenil Roy>
**Program:** PG Diploma in AI-ML & Agentic AI Engineering
