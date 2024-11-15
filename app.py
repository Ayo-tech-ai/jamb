import streamlit as st
import joblib
import numpy as np

# Load the trained model and encoder
model = joblib.load('jamb.joblib')  # your trained model
encoder = joblib.load('jamb_faculty_encoder.joblib')  # your label encoder

# Streamlit App Title with updated color
st.markdown(
    "<h1 style='color: darkgreen;'>JAMB/UTME Faculty Match</h1>",
    unsafe_allow_html=True
)

# Description of the app with updated color
st.markdown(
    "<p style='color: darkgreen;'>An AI-powered App that predicts Jambites Faculty based on their UTME scores.</p>",
    unsafe_allow_html=True
)

# Arrange subjects in columns of two each with increased font size
col1, col2 = st.columns(2)
with col1:
    Use_of_English = st.number_input(
        "Use of English", min_value=0, step=1, key="use_of_english"
    )
    Physics = st.number_input(
        "Physics", min_value=0, step=1, key="physics"
    )
with col2:
    Chemistry = st.number_input(
        "Chemistry", min_value=0, step=1, key="chemistry"
    )
    Biology = st.number_input(
        "Biology", min_value=0, step=1, key="biology"
    )

# Separate field for Mathematics
Mathematics = st.number_input(
    "Mathematics", min_value=0, step=1, key="mathematics"
)

# Automatically calculate the Total Score
subject_scores = [Use_of_English, Physics, Chemistry, Biology, Mathematics]
Total_Score = sum(subject_scores)

# Display Total Score (auto-updated)
st.markdown(
    f"<p style='font-size: 20px; color: white;'>Total Score: <strong>{Total_Score}</strong></p>",
    unsafe_allow_html=True
)

# Center-align the Predict button
button_centered = st.columns([1, 1, 1])
with button_centered[1]:
    predict_button = st.button('Predict')

# Display the result only when the Predict button is clicked
if predict_button:
    # Count how many subjects have non-zero scores
    non_zero_subjects = sum(1 for score in subject_scores if score > 0)

    # Check if exactly 4 subjects have scores
    if non_zero_subjects == 4:
        if Use_of_English == 0:
            st.write("Please include Use of English as it is compulsory when selecting 4 subjects.")
        else:
            if Total_Score < 150:
                st.markdown(
                    "<p style='font-size: 20px; color: white;'><strong>Predicted Faculty: Not offered admission</strong></p>",
                    unsafe_allow_html=True
                )
            else:
                input_array = np.array(subject_scores + [Total_Score]).reshape(1, -1)
                prediction = model.predict(input_array)
                prediction_label = encoder.inverse_transform(prediction)
                st.markdown(
                    f"<p style='font-size: 20px; color: white;'><strong>Predicted Faculty: {prediction_label[0]}</strong></p>",
                    unsafe_allow_html=True
                )
    elif non_zero_subjects < 4:
        st.write("You must provide scores for at least 4 subjects.")
    else:
        st.write("Please limit the input to exactly 4 subjects.")

# Set background image at the end
st.markdown(
    """
    <style>
    .stApp {
        background-image: url('https://raw.githubusercontent.com/Ayo-tech-ai/jamb/main/background.jpg');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    .stNumberInput label {
        font-size: 20px;  /* Increase font size for subjects */
        color: white;
    }
    </style>
    """, unsafe_allow_html=True
)
