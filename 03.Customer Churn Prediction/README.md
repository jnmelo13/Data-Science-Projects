# 📉 Customer Churn Prediction

This project aims to predict customer churn using historical usage data and service characteristics. By identifying at-risk customers, businesses can proactively improve retention and reduce acquisition costs.

---

## 📌 Project Overview

- **Problem**: Predict whether a customer will churn based on behavior and service features.  
- **Goal**: Build a robust classification model and identify business-actionable insights.  
- **Approach**: Data preprocessing → Exploratory Data Analysis → Model training → Evaluation  

---

## 🧪 Dataset

The dataset contains customer-level information, including:

- Usage metrics (e.g., `total_day_minutes`, `number_customer_service_calls`)  
- Plan indicators (e.g., `international_plan`, `voice_mail_plan`)  
- Target variable: `churn` (1 = customer left, 0 = customer retained)  

---

## 🔍 Exploratory Data Analysis (EDA)

EDA was performed to identify trends and relationships between features and churn, including:

- Churn distribution  
- Impact of international and voice mail plans  
- Call behavior patterns (daytime usage, support calls)  
- Visualizations with `seaborn` and `matplotlib`  

---

## ⚙️ Modeling Workflow

- Data cleaning and transformation  
- Class balancing using **SMOTE**  
- Model training and comparison:
  - Logistic Regression  
  - Naive Bayes  
  - Random Forest (with and without hyperparameter tuning)  
  - XGBoost (with and without tuning)  
- Evaluation using:
  - Accuracy, Precision, Recall, AUC  
  - ROC Curves  
- Final summary table with performance comparison  

---

## 🏁 Results & Insights

- **XGBoost with hyperparameter tuning** delivered the best performance, especially in AUC and recall.  
- **Random Forest** is a solid secondary option with strong metrics and higher interpretability.  
- Key churn drivers include international plan usage and frequent customer service calls.  
- Data balancing and model optimization improved overall generalization performance.  

---

## 💡 Future Enhancements

- Add SHAP or permutation importance to explain feature contributions  
- Convert pipeline to deployable API using FastAPI  
- Integrate monitoring and feedback loop for retraining  
- Explore segment-based models (e.g., by region or customer type)  
