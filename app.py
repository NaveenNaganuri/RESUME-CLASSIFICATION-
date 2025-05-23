import streamlit as st

import pickle
import fitz  # For PDF
from io import StringIO

# Cache vectorizer and model
@st.cache_resource
def load_vectorizer_and_model():
    with open("vector.pkl", "rb") as f:
        vectorizer = pickle.load(f)
    with open("modelDT.pkl", "rb") as f:
        model = pickle.load(f)
    return vectorizer, model

vectorizer, model = load_vectorizer_and_model()

# Streamlit UI
st.title("📄 Resume Classifier")
st.write("Upload your `.txt` or `.pdf` resume to predict the job domain.")

st.markdown('<div class="title">📄 Resume Classifier</div>', unsafe_allow_html=True)
st.write("Upload your resume file (`.txt` or `.pdf`) to predict the job domain.")

uploaded_file = st.file_uploader("Choose a resume file", type=["txt", "pdf"])

def extract_text_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

if uploaded_file is not None:
    # Extract resume text
    if uploaded_file.name.endswith(".txt"):
        resume_text = uploaded_file.read().decode("utf-8")
    elif uploaded_file.name.endswith(".pdf"):
        resume_text = extract_text_from_pdf(uploaded_file)
    else:
        st.error("Unsupported file type.")
        st.stop()

    # Display preview
    st.subheader("📝 Resume Preview")
    st.text_area("Text extracted from your resume:", resume_text[:3000], height=250)

    # Prediction animation
    with st.spinner("🔍 Analyzing resume..."):
        sleep(2)
        features = vectorizer.transform([resume_text])
        prediction = model.predict(features)[0]

    st.markdown(f'<div class="result">✅ Predicted Job Role: <b>{prediction}</b></div>', unsafe_allow_html=True)

# TeaM menbers

st.markdown("---")
with st.expander("👨‍💻 Click to View Team Members"):
    st.write("**Venkata Siva Kumar Paruvada** – venkatesh5082931@gmail.com – 6302076588")
    st.write("**Naveen Nagappa Naganuri** – naganurinaveen8@gmail.com – 7676845025")
    st.write("**Kumara Sai Charan** – sai9392c@gmail.com – 9392352553")
    st.write("**Shaikh Asad Aftab** – kingasad4917@gmail.com – 9730619102")
    st.write("**Doddala Vivek** – viv6302201544@gmail.com – 6302201544")
    st.write("**P. Shashidhar Babu** – pshashidhar29@gmail.com – 7995363904")
    
    
