# student-performance-prediction
## 📌 Overview
The **Student Performance Prediction System** is a machine learning-based web application that predicts whether a student is likely to **pass or fail** based on academic and behavioral features.
This project uses a **real-world dataset** and provides:

* 📊 Data visualization
* 🤖 Machine learning predictions
* 🔍 Explainability using SHAP
* 📂 Batch prediction via CSV upload
* 🔐 User authentication system
## 🚀 Features
* 🔐 **User Authentication**
  * Register new users
  * Login/logout system using SQLite database
* 🤖 **Machine Learning Model**
  * Random Forest Classifier
  * Predicts student performance (Pass/Fail)
* 📊 **Data Visualization**
  * Gender vs performance
  * Parental education impact
  * Score trends
* 🔍 **Explainable AI**
  * SHAP (SHapley Additive Explanations)
  * Shows feature importance for predictions
* 📂 **Batch Prediction**
  * Upload CSV file
  * Get predictions for multiple students
  * Download result
## 📊 Dataset
This project uses the Kaggle dataset:
**Students Performance in Exams**
Features include:
* Gender
* Race/Ethnicity
* Parental Level of Education
* Lunch Type
* Test Preparation Course
* Math, Reading, Writing Scores
### 🎯 Target Variable
A new column is created:
* `pass = 1` if total score ≥ 150
* `pass = 0` otherwise
## 🛠️ Tech Stack
* **Programming Language:** Python
* **Libraries:**
  * pandas, numpy
  * scikit-learn
  * streamlit
  * matplotlib
  * shap
  * joblib
* **Database:** SQLite
* **Model:** Random Forest Classifier

---

## 📁 Project Structure

```
Student-Performance-Prediction/
│
├── data/
│   └── students.csv
├── models/
│   └── model.pkl
├── app.py
├── users.db
├── requirements.txt
└── README.md
## ⚙️ Installation & Setup
### 1️⃣ Clone the repository
git clone https://github.com/your-username/student-performance-prediction.git
cd student-performance-prediction
### 2️⃣ Install dependencies
pip install -r requirements.txt
### 3️⃣ Run the application
streamlit run app.py
## 🔐 Login Credentials

You can create a new account using the **Register** option.
## 📊 CSV Upload Format
For batch prediction, upload a CSV with the following columns`
gender,race/ethnicity,parental_level_of_education,lunch,test_preparation_course,math_score,reading_score,writing_score

## 🎯 How It Works

1. User logs into the system
2. Data is processed and encoded
3. Model predicts performance
4. SHAP explains feature impact
5. Results are displayed
## 📸 Screenshots (Add these)

* Login Page
* Dashboard
* Prediction Result
* SHAP Graph
* CSV Upload
<img width="1360" height="718" alt="student1" src="https://github.com/user-attachments/assets/7bce7017-1ff4-41b1-bb05-0b78451c38da" />
<img width="1366" height="656" alt="student2" src="https://github.com/user-attachments/assets/554ccd31-7c2d-4cd3-941b-1c2bdedd533c" />
<img width="1352" height="720" alt="student4" src="https://github.com/user-attachments/assets/2b51ba97-06ea-4ee3-8cbd-650062c8575f" />
<img width="1361" height="721" alt="student3" src="https://github.com/user-attachments/assets/f8d0c86c-c8da-4ec7-b5bc-2d23dbcb02e6" />
<img width="1359" height="708" alt="student5" src="https://github.com/user-attachments/assets/785c9502-19ab-4748-8ef2-d51fddb76840" />

## 🎯 Use Cases
* Schools & Colleges
* EdTech Platforms
* Student Performance Monitoring
* Early Risk Detection
## 💡 Future Improvements
* 🔒 Password hashing (security)
* ☁️ Cloud deployment (Streamlit Cloud / AWS)
* 📈 Advanced models (XGBoost)
* 📊 Real-time dashboards
* 👥 Role-based access (Admin/Teacher)

## 📌 Conclusion
This project demonstrates:
* End-to-end ML pipeline
* Real-world dataset usage
* Deployment-ready UI
* Explainable AI concepts
