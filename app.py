import streamlit as st
import joblib
import numpy as np

# Load the trained model and encoder
model = joblib.load('jamb.joblib')  # your trained model
encoder = joblib.load('jamb_faculty_encoder.joblib')  # your label encoder

# Streamlit App Title with white border styling
st.markdown(
    """
    <h1 style='color: darkgreen; text-shadow: -1px -1px 0 white, 1px -1px 0 white, -1px 1px 0 white, 1px 1px 0 white;'>
    JAMB/UTME Faculty Match
    </h1>
    """,
    unsafe_allow_html=True
)

# Description with white border styling
st.markdown(
    """
    <p style='color: darkgreen; text-shadow: -1px -1px 0 white, 1px -1px 0 white, -1px 1px 0 white, 1px 1px 0 white;'>
    An AI-powered App that predicts Jambites Faculty based on their UTME scores.
    </p>
    """,
    unsafe_allow_html=True
)

# CSS for green borders around the subject names and total score
st.markdown(
    """
    <style>
        .green-border {
            border: 2px solid green;
            border-radius: 5px;
            padding: 5px;
            margin: 5px 0;
        }
        .dark-green-border {
            border: 2px solid darkgreen;
            border-radius: 5px;
            padding: 10px;
            margin: 10px 0;
            font-weight: bold;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Arrange subjects in columns of two each with green border styling
col1, col2 = st.columns(2)
with col1:
    Use_of_English = st.number_input("Use of English", min_value=0, step=1, key="english")
    st.markdown("<div class='green-border'>Use of English</div>", unsafe_allow_html=True)

    Physics = st.number_input("Physics", min_value=0, step=1, key="physics")
    st.markdown("<div class='green-border'>Physics</div>", unsafe_allow_html=True)

with col2:
    Chemistry = st.number_input("Chemistry", min_value=0, step=1, key="chemistry")
    st.markdown("<div class='green-border'>Chemistry</div>", unsafe_allow_html=True)

    Biology = st.number_input("Biology", min_value=0, step=1, key="biology")
    st.markdown("<div class='green-border'>Biology</div>", unsafe_allow_html=True)

# Separate field for Mathematics with green border styling
Mathematics = st.number_input("Mathematics", min_value=0, step=1, key="mathematics")
st.markdown("<div class='green-border'>Mathematics</div>", unsafe_allow_html=True)

# Automatically calculate and display the Total Score with green border styling
subject_scores = [Use_of_English, Physics, Chemistry, Biology, Mathematics]
Total_Score = sum(subject_scores)
st.markdown(f"<div class='green-border'>Total Score: <strong>{Total_Score}</strong></div>", unsafe_allow_html=True)

# Predict button
button_centered = st.columns([1, 1, 1])
with button_centered[1]:
    predict_button = st.button('Predict')

# Display the result when the Predict button is clicked
if predict_button:
    # Count how many subjects have non-zero scores
    non_zero_subjects = sum(1 for score in subject_scores if score > 0)

    # Check if exactly 4 subjects have scores
    if non_zero_subjects == 4:
        if Use_of_English == 0:
            st.write("Please include Use of English as it is compulsory when selecting 4 subjects.")
        else:
            if Total_Score < 150:
                st.markdown("<div class='dark-green-border'>Predicted Faculty: Not offered admission</div>", unsafe_allow_html=True)
            else:
                input_array = np.array(subject_scores + [Total_Score]).reshape(1, -1)
                prediction = model.predict(input_array)
                prediction_label = encoder.inverse_transform(prediction)

                # Display the prediction with dark green border
                st.markdown(f"<div class='dark-green-border'>Predicted Faculty: {prediction_label[0]}</div>", unsafe_allow_html=True)

                # Additional faculty information
                faculty_info = {
                    "Agriculture": "Departments: Agronomy, Animal Science, Crop Science, Soil Science.",
                    "Science": "Departments: Chemistry, Physics, Biology, Mathematics, Computer Science.",
                    "Clinical Sciences": "Departments: Medicine, Surgery, Dentistry, Pediatrics."
                    # Add more faculties as needed
                }

                if prediction_label[0] in faculty_info:
                    st.markdown(f"<div class='dark-green-border'>{faculty_info[prediction_label[0]]}</div>", unsafe_allow_html=True)
    elif non_zero_subjects < 4:
        st.write("You must provide scores for at least 4 subjects.")
    else:
        st.write("Please limit the input to exactly 4 subjects.")

# Set background image
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url('https://raw.githubusercontent.com/Ayo-tech-ai/jamb/main/background.jpg');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    </style>
    """, unsafe_allow_html=True)
