# FINAL FULL MULTI-DISEASE PREDICTION APP WITH UI POLISH + BACK BUTTON

import streamlit as st
import joblib
import base64
from fpdf import FPDF

# Load Models
heart_model = joblib.load('heart_model.pkl')
diabetes_model = joblib.load('diabetes_model.pkl')
liver_model = joblib.load('liver_model.pkl')

# Session State Init
if "page" not in st.session_state:
    st.session_state.page = "landing"

# PDF Generator
class CustomPDF(FPDF):
    def header(self):
        self.set_fill_color(240, 248, 255)
        self.rect(0, 0, 210, 297, 'F')
        self.set_font("Arial", 'B', 16)
        self.set_text_color(0, 102, 204)
        self.cell(0, 10, "Health Prediction Report", ln=True, align='C')
        self.ln(10)

    def section_body(self, label, value):
        self.set_font("Arial", '', 12)
        self.set_text_color(0, 0, 0)
        self.cell(60, 10, f"{label}:", ln=False)
        self.set_text_color(80, 0, 80)
        self.cell(0, 10, str(value), ln=True)

def generate_health_report(name, age, disease, result, filename="report.pdf"):
    pdf = CustomPDF()
    pdf.add_page()
    pdf.section_body("Patient Name", name)
    pdf.section_body("Age", age)
    pdf.section_body("Disease Type", disease)
    clean_result = result.encode('latin-1', 'ignore').decode('latin-1')
    pdf.section_body("Prediction Result", clean_result)
    pdf.ln(10)
    pdf.set_font("Arial", '', 10)
    pdf.set_text_color(100, 100, 100)
    pdf.multi_cell(0, 10, "Note: This is a machine-generated prediction. Please consult a medical professional for confirmation.")
    pdf.output(filename)
    return filename

def download_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        pdf_display = f'<a href="data:application/octet-stream;base64,{base64_pdf}" download="{file_path}">📄 Download Report</a>'
        st.markdown(pdf_display, unsafe_allow_html=True)

# Custom UI CSS
st.markdown("""
    <style>
    body {
        background: linear-gradient(to right, #f0f9ff, #e0f7fa);
    }
    header, footer {visibility: hidden;}
    .block-container { padding-top: 1rem !important; }
    .card {
        background-color: #ffffff;
        padding: 2rem;
        border-radius: 1rem;
        box-shadow: 0 4px 16px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
    }
    .big-title {
        text-align: center;
        font-size: 32px;
        font-weight: bold;
        color: #cc0000;
        margin-bottom: 10px;
    }
    .positive-quote {
        text-align: center;
        font-size: 18px;
        color: #009966;
        margin-bottom: 25px;
    }
    .stButton > button {
        background-color: #cc0000;
        color: white;
        padding: 12px 24px;
        border-radius: 10px;
        border: none;
        font-size: 16px;
        transition: 0.3s;
    }
    .stButton > button:hover {
        background-color: #990000;
        transform: scale(1.03);
    }
    .stTextInput > div > input, .stNumberInput > div > input, .stSelectbox > div {
        border: 1px solid #ddd;
        border-radius: 10px !important;
        padding: 10px;
        transition: 0.3s;
    }
    .stTextInput > div > input:hover, .stNumberInput > div > input:hover, .stSelectbox > div:hover {
        border-color: #1f77b4;
        box-shadow: 0 0 5px rgba(31, 119, 180, 0.3);
    }
    </style>
""", unsafe_allow_html=True)

# Landing Page
if st.session_state.page == "landing":
    st.markdown("<h1 style='text-align: center; color: #004d99;'>🧠 Welcome to Multi-Disease Prediction App</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #333;'>\"Prevention is better than cure – take a step toward better health.\"</h3>", unsafe_allow_html=True)
    st.write("This app uses machine learning to predict chances of **Heart Disease, Diabetes, and Liver Disease** based on your health inputs.")
    if st.button("🚀 Start Health Check"):
        st.session_state.page = "select_disease"

# Disease Selector
elif st.session_state.page == "select_disease":
    st.title("🔬 Choose Disease to Predict")
    disease = st.selectbox("Select a Disease", ["Heart Disease", "Diabetes", "Liver Disease"])
    if st.button("Continue"):
        st.session_state.page = disease

# Heart Disease Page
elif st.session_state.page == "Heart Disease":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="big-title">❤️ Heart Disease Prediction</div>', unsafe_allow_html=True)
    st.markdown('<div class="positive-quote">“You are taking a great step towards your well-being”</div>', unsafe_allow_html=True)
    name = st.text_input("👤 Enter your name")
    age_input = st.number_input("🎂 Enter your age", min_value=1, key="heartage")
    sex = st.selectbox("👫 Sex", ["Male", "Female"])
    cp = st.selectbox("💓 Chest Pain Type", ["typical angina", "atypical angina", "non-anginal", "asymptomatic"])
    trestbps = st.number_input("🩺 Resting Blood Pressure")
    chol = st.number_input("🧪 Cholesterol")
    fbs = st.selectbox("🍬 Fasting Blood Sugar > 120", ["Yes", "No"])
    restecg = st.selectbox("🧠 Resting ECG", ["normal", "ST-T abnormality", "left ventricular hypertrophy"])
    thalach = st.number_input("🏃 Max Heart Rate Achieved")
    exang = st.selectbox("💥 Exercise Induced Angina", ["Yes", "No"])
    oldpeak = st.number_input("📉 ST Depression")
    slope = st.selectbox("📈 Slope", ["up", "flat", "down"])
    if st.button("🔍 Predict Heart Health"):
        sex = 1 if sex == "Male" else 0
        cp = {"typical angina": 0, "atypical angina": 1, "non-anginal": 2, "asymptomatic": 3}[cp]
        fbs = 1 if fbs == "Yes" else 0
        restecg = {"normal": 0, "ST-T abnormality": 1, "left ventricular hypertrophy": 2}[restecg]
        exang = 1 if exang == "Yes" else 0
        slope = {"up": 0, "flat": 1, "down": 2}[slope]
        result = heart_model.predict([[age_input, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope]])[0]
        diagnosis = "❤️ Positive for Heart Disease" if result == 1 else "💚 No Heart Disease Detected"
        st.success(diagnosis)
        if name:
            pdf_file = generate_health_report(name, age_input, "Heart Disease", diagnosis, filename="heart_report.pdf")
            download_pdf(pdf_file)
    if st.button("⬅️ Back"):
        st.session_state.page = "select_disease"
    st.markdown('</div>', unsafe_allow_html=True)

# Diabetes Page
elif st.session_state.page == "Diabetes":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="big-title">🩸 Diabetes Prediction</div>', unsafe_allow_html=True)
    st.markdown('<div class="positive-quote">“Your health is your greatest wealth”</div>', unsafe_allow_html=True)
    name = st.text_input("👤 Enter your name")
    age_input = st.number_input("🎂 Enter your age", min_value=1, key="diabage")
    Pregnancies = st.number_input("🤰 Pregnancies", min_value=0)
    Glucose = st.number_input("🧪 Glucose")
    BloodPressure = st.number_input("🩸 Blood Pressure")
    SkinThickness = st.number_input("📏 Skin Thickness")
    Insulin = st.number_input("💉 Insulin")
    BMI = st.number_input("⚖️ BMI")
    DPF = st.number_input("🧬 Diabetes Pedigree Function")
    Age = st.number_input("📆 Age", min_value=1)
    if st.button("🔍 Predict Diabetes"):
        result = diabetes_model.predict([[Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DPF, Age]])[0]
        diagnosis = "🩸 Positive for Diabetes" if result == 1 else "💚 No Diabetes Detected"
        st.success(diagnosis)
        if name:
            pdf_file = generate_health_report(name, age_input, "Diabetes", diagnosis, filename="diabetes_report.pdf")
            download_pdf(pdf_file)
    if st.button("⬅️ Back"):
        st.session_state.page = "select_disease"
    st.markdown('</div>', unsafe_allow_html=True)

# Liver Disease Page
elif st.session_state.page == "Liver Disease":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="big-title">🧪 Liver Disease Prediction</div>', unsafe_allow_html=True)
    st.markdown('<div class="positive-quote">“Health is the first step toward happiness”</div>', unsafe_allow_html=True)
    name = st.text_input("👤 Enter your name")
    age_input = st.number_input("🎂 Enter your age", min_value=1, key="livage")
    Age = age_input
    Gender = st.selectbox("👫 Gender", ["Male", "Female"])
    Total_Bilirubin = st.number_input("🧪 Total Bilirubin")
    Direct_Bilirubin = st.number_input("🧪 Direct Bilirubin")
    Alkaline_Phosphotase = st.number_input("🧫 Alkaline Phosphotase")
    Alamine_Aminotransferase = st.number_input("🧬 Alamine Aminotransferase")
    Aspartate_Aminotransferase = st.number_input("🧬 Aspartate Aminotransferase")
    Total_Proteins = st.number_input("🧃 Total Proteins")
    Albumin = st.number_input("🧃 Albumin")
    A_G_ratio = st.number_input("🔁 Albumin and Globulin Ratio")
    if st.button("🔍 Predict Liver Health"):
        Gender = 1 if Gender == "Male" else 0
        result = liver_model.predict([[Age, Gender, Total_Bilirubin, Direct_Bilirubin, Alkaline_Phosphotase,
                                       Alamine_Aminotransferase, Aspartate_Aminotransferase, Total_Proteins,
                                       Albumin, A_G_ratio]])[0]
        diagnosis = "🧪 Liver Disease Detected" if result == 1 else "💚 No Liver Disease Detected"
        st.success(diagnosis)
        if name:
            pdf_file = generate_health_report(name, age_input, "Liver Disease", diagnosis, filename="liver_report.pdf")
            download_pdf(pdf_file)
    if st.button("⬅️ Back"):
        st.session_state.page = "select_disease"
    st.markdown('</div>', unsafe_allow_html=True)
