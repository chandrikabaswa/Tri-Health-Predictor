import os
import pickle
import streamlit as st

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(
    page_title="Tri Health Predictor 🧑‍⚕️",
    layout="wide",
    page_icon="🧑‍⚕️"
)

# -------------------------------
# Custom CSS for Modern UI
# -------------------------------
st.markdown("""
    <style>
    /* Background gradient for the app */
    .stApp {
        background: linear-gradient(to right, #e0f7fa, #ffffff);
        font-family: 'Segoe UI', sans-serif;
    }

    /* Headers */
    h1, h2, h3 {
        color: #003366;
        font-weight: bold;
    }

    /* Buttons */
    .stButton button {
        background: linear-gradient(to right, #2196f3, #21cbf3);
        color: white;
        border-radius: 10px;
        padding: 10px 25px;
        font-weight: bold;
        border: none;
        transition: transform 0.2s;
    }
    .stButton button:hover {
        transform: scale(1.05);
        background: linear-gradient(to right, #1976d2, #26c6da);
    }

    /* Result Cards */
    .result-card {
        border-radius: 15px;
        padding: 20px;
        margin: 20px 0;
        color: white;
        font-size: 18px;
        font-weight: bold;
        box-shadow: 0 8px 20px rgba(0,0,0,0.15);
    }
    .positive { background: linear-gradient(to right, #e53935, #ff6b6b); }
    .negative { background: linear-gradient(to right, #43a047, #66bb6a); }

    /* Tips text */
    .tips {
        font-size: 16px;
        color: #555555;
        margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# -------------------------------
# Load Models
# -------------------------------
working_dir = os.path.dirname(os.path.abspath(__file__))
diabetes_model = pickle.load(open(f'{working_dir}/saved_models/diabetes_model.sav', 'rb'))
heart_disease_model = pickle.load(open(f'{working_dir}/saved_models/heart_disease_model.sav', 'rb'))
parkinsons_model = pickle.load(open(f'{working_dir}/saved_models/parkinsons_model.sav', 'rb'))

# -------------------------------
# Result Card Function
# -------------------------------
def result_card(title, message, is_positive, tips=""):
    card_class = "positive" if is_positive else "negative"
    st.markdown(
        f"""
        <div class="result-card {card_class}">
            <h3>{title}</h3>
            <p>{message}</p>
            <p class="tips">{tips}</p>
        </div>
        """, unsafe_allow_html=True
    )

# -------------------------------
# Tabs Navigation
# -------------------------------
st.title("🧑‍⚕️ Tri Health Predictor")
tab1, tab2, tab3 = st.tabs(
    ["🩸 Diabetes Prediction", "❤️ Heart Disease Prediction", "🧠 Parkinson's Prediction"]
)

# -------------------------------
# Diabetes Prediction
# -------------------------------
with tab1:
    st.header("Diabetes Prediction")
    col1, col2, col3 = st.columns(3)

    with col1:
        Pregnancies = st.number_input('Pregnancies', 0, 20, 1)
        SkinThickness = st.number_input('Skin Thickness (mm)', 0.0, 100.0, 20.0)
        DiabetesPedigreeFunction = st.number_input('Pedigree Function', 0.0, 2.5, 0.5)
    with col2:
        Glucose = st.number_input('Glucose Level (mg/dL)', 0.0, 200.0, 100.0)
        Insulin = st.number_input('Insulin Level (IU/mL)', 0.0, 500.0, 50.0)
        Age = st.number_input('Age', 1, 100, 30)
    with col3:
        BloodPressure = st.number_input('Blood Pressure (mmHg)', 0.0, 180.0, 80.0)
        BMI = st.number_input('BMI', 10.0, 50.0, 25.0)

    if st.button('Predict Diabetes'):
        user_input = [Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]
        prediction = diabetes_model.predict([user_input])
        if prediction[0] == 1:
            result_card(
                "⚠️ Diabetes Detected",
                "Consult a doctor and follow a healthy lifestyle.",
                True,
                tips="💡 Tip: Eat low-sugar foods, exercise regularly, and monitor blood glucose levels."
            )
        else:
            result_card(
                "✅ No Diabetes",
                "Maintain a balanced diet and regular exercise.",
                False,
                tips="💡 Tip: Keep a healthy lifestyle to prevent diabetes."
            )

# -------------------------------
# Heart Disease Prediction
# -------------------------------
with tab2:
    st.header("Heart Disease Prediction")
    col1, col2, col3 = st.columns(3)

    with col1:
        age = st.number_input('Age', 1, 100, 50)
        trestbps = st.number_input('Resting BP (mmHg)', 80, 200, 120)
        restecg = st.selectbox('Resting ECG', [0, 1, 2])
        oldpeak = st.number_input('ST Depression', 0.0, 6.0, 1.0)
    with col2:
        sex = st.radio('Sex', ['Male', 'Female'])
        chol = st.number_input('Cholesterol (mg/dL)', 100, 400, 200)
        thalach = st.number_input('Max Heart Rate', 60, 220, 150)
        slope = st.selectbox('Slope of Peak Exercise ST', [0, 1, 2])
    with col3:
        cp = st.selectbox('Chest Pain Type', [0, 1, 2, 3])
        fbs = st.radio('Fasting Blood Sugar > 120 mg/dL', [0, 1])
        exang = st.radio('Exercise Induced Angina', [0, 1])
        ca = st.number_input('Number of Major Vessels', 0, 4, 1)
        thal = st.selectbox('Thalassemia Type', [0, 1, 2, 3])

    if st.button('Predict Heart Disease'):
        sex_val = 1 if sex == 'Male' else 0
        user_input = [age, sex_val, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]
        prediction = heart_disease_model.predict([user_input])
        if prediction[0] == 1:
            result_card(
                "⚠️ Heart Disease Detected",
                "Immediate consultation is recommended.",
                True,
                tips="💡 Tip: Avoid smoking, maintain healthy weight, exercise regularly, and monitor cholesterol."
            )
        else:
            result_card(
                "✅ Heart is Healthy",
                "Maintain a heart-healthy lifestyle.",
                False,
                tips="💡 Tip: Eat balanced diet and keep active to maintain heart health."
            )

# -------------------------------
# Parkinson's Prediction
# -------------------------------
with tab3:
    st.header("Parkinson's Disease Prediction")
    cols = st.columns(5)
    input_features = {
        'MDVP:Fo(Hz)': (88, 260),
        'MDVP:Fhi(Hz)': (102, 592),
        'MDVP:Flo(Hz)': (65, 239),
        'MDVP:Jitter(%)': (0.0016, 0.033),
        'MDVP:Jitter(Abs)': (0.000007, 0.00026),
        'MDVP:RAP': (0.00068, 0.0214),
        'MDVP:PPQ': (0.00092, 0.0195),
        'Jitter:DDP': (0.00204, 0.0643),
        'MDVP:Shimmer': (0.00954, 0.119),
        'MDVP:Shimmer(dB)': (0.085, 1.3),
        'Shimmer:APQ3': (0.00455, 0.056),
        'Shimmer:APQ5': (0.0057, 0.079),
        'MDVP:APQ': (0.00719, 0.137),
        'Shimmer:DDA': (0.0136, 0.169),
        'NHR': (0.00065, 0.315),
        'HNR': (8.44, 33.04),
        'RPDE': (0.256, 0.685),
        'DFA': (0.574, 0.825),
        'spread1': (-7.96, -2.43),
        'spread2': (0.006, 0.450),
        'D2': (1.42, 3.67),
        'PPE': (0.044, 0.527)
    }

    user_inputs = []
    for i, (feature, (min_val, max_val)) in enumerate(input_features.items()):
        with cols[i % 5]:
            user_inputs.append(st.slider(feature, float(min_val), float(max_val), float((min_val + max_val) / 2)))

    if st.button("Predict Parkinson's Disease"):
        prediction = parkinsons_model.predict([user_inputs])
        if prediction[0] == 1:
            result_card(
                "⚠️ Parkinson's Detected",
                "Consult a neurologist for further guidance.",
                True,
                tips="💡 Tip: Regular exercise and early diagnosis can improve quality of life."
            )
        else:
            result_card(
                "✅ No Parkinson's Detected",
                "Maintain a healthy lifestyle.",
                False,
                tips="💡 Tip: Maintain healthy habits and monitor symptoms regularly."
            )
