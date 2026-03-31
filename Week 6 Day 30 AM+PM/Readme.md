# 🚗 SUV Purchase Prediction using Logistic Regression

## 📌 Project Overview
This project focuses on building a **Logistic Regression model** to predict whether a customer will purchase an SUV based on demographic and financial features.

The goal is to apply **end-to-end Machine Learning workflow** including data preprocessing, visualization, model building, and evaluation.

---

## 📊 Dataset Description
The dataset contains the following features:

- **Gender** (Categorical)
- **Age** (Numeric)
- **Estimated Salary** (Numeric)
- **Purchased** (Target Variable: 0 or 1)

---

## ⚙️ Steps Performed

### 1. Data Preprocessing
- Converted categorical variable **Gender** using **One-Hot Encoding**
- Handled boolean values (True/False → 1/0)
- Defined feature matrix `X` and target variable `y`

---

### 2. Exploratory Data Analysis (EDA)
- Compared salary distribution across gender using:
  - **Box Plot**
  - **Violin Plot**
- Understood spread, median, and distribution patterns

---

### 3. Train-Test Split
- Split dataset into:
  - **80% Training**
  - **20% Testing**

---

### 4. Feature Scaling
- Applied **StandardScaler**
- Ensured features are on the same scale for better model performance

---

### 5. Model Training
- Used **Logistic Regression**
- Trained model on scaled training data

---

### 6. Model Evaluation
Evaluated model using:

- Accuracy Score
- Confusion Matrix
- Classification Report

---

### 📈 Results

| Metric            | Score   |
|------------------|--------|
| Train Accuracy   | 0.81   |
| Test Accuracy    | 0.88   |
| Cross Validation | 0.8125 |

---

## 🧠 Key Learnings

### 🔹 1. Encoding Matters
- Label Encoding can introduce **false ordinal relationships**
- One-Hot Encoding is preferred for **nominal data like Gender**

---

### 🔹 2. Model Evaluation is More Than Accuracy
- Accuracy alone is misleading
- Must compare:
  - Train Accuracy
  - Test Accuracy
  - Cross Validation Score

---

### 🔹 3. Overfitting vs Underfitting
- Train ≈ CV → Good generalization
- Test > Train → Possible lucky split
- No overfitting observed in this model

---

### 🔹 4. Importance of Cross Validation
- Provides **reliable estimate** of model performance
- Helps avoid dependency on a single data split

---

### 🔹 5. Feature Scaling is Crucial
- Logistic Regression is sensitive to feature scale
- Scaling improves convergence and performance

---

### 🔹 6. Model Limitations
- Logistic Regression is a **linear model**
- May underperform if data is **non-linear**

---

## 🚀 Future Improvements

- Hyperparameter tuning (Regularization)
- Try advanced models:
  - Random Forest
  - XGBoost
- Feature engineering:
  - Age groups
  - Salary bins
- ROC-AUC and threshold tuning

---

## 🛠️ Tech Stack

- Python 🐍
- Pandas
- NumPy
- Matplotlib / Seaborn
- Scikit-learn

---

## 📌 Conclusion

The model demonstrates **stable and reliable performance (~81%)** with no signs of overfitting. Cross-validation confirms that the model generalizes well, though there is room for improvement using more advanced techniques.

---
