import streamlit as st
import joblib
import numpy as np

# Load the trained model and encoder
model = joblib.load('jamb.joblib')  # your trained model
encoder = joblib.load('jamb_faculty_encoder.joblib')  # your label encoder

# Helper function to style text with borders around each character
def style_with_border(text, color):
    styled_text = ''.join(
        [f"<span style='border: 2px solid {color}; margin: 2px; padding: 2px;'>{char}</span>" for char in text]
    )
    return f"<div style='display: inline-block;'>{styled_text}</div>"

# Streamlit App Title with updated styling (white border around each character)
st.markdown(
    style_with_border("JAMB/UTME Faculty Match", "white"),
    unsafe_allow_html=True
)

# Description of the app with updated styling (white border around each character)
st.markdown(
    style_with_border("An AI-powered App that predicts Jambites Faculty based on their UTME scores.", "white"),
    unsafe_allow_html=True
)

# Arrange subjects in columns of two each
col1, col2 = st.columns(2)
with col1:
    Use_of_English = st.number_input(style_with_border("Use of English", "green"), min_value=0, step=1)
    Physics = st.number_input(style_with_border("Physics", "green"), min_value=0, step=1)
with col2:
    Chemistry = st.number_input(style_with_border("Chemistry", "green"), min_value=0, step=1)
    Biology = st.number_input(style_with_border("Biology", "green"), min_value=0, step=1)

# Separate field for Mathematics
st.write("")  # Empty space for better layout
Mathematics = st.number_input(style_with_border("Mathematics", "green"), min_value=0, step=1)

# Automatically calculate the Total Score
subject_scores = [Use_of_English, Physics, Chemistry, Biology, Mathematics]
Total_Score = sum(subject_scores)

# Display Total Score (auto-updated)
st.markdown(
    style_with_border(f"Total Score: {Total_Score}", "green"),
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
        # Ensure that Use of English is one of the selected subjects
        if Use_of_English == 0:
            st.write("Please include Use of English as it is compulsory when selecting 4 subjects.")
        else:
            # Check if the total score is less than 150, and if so, predict "Not offered admission"
            if Total_Score < 150:
                st.markdown(
                    style_with_border("Predicted Faculty: Not offered admission", "darkgreen"),
                    unsafe_allow_html=True
                )
            else:
                # Convert the input features into a numpy array (reshape to match model input)
                input_array = np.array(subject_scores + [Total_Score]).reshape(1, -1)

                # Use the model to make a prediction
                prediction = model.predict(input_array)

                # If an encoder is used, transform the predicted label back to the original class
                prediction_label = encoder.inverse_transform(prediction)

                # Display the result with dark green border
                st.markdown(
                    style_with_border(f"Predicted Faculty: {prediction_label[0]}", "darkgreen"),
                    unsafe_allow_html=True
                )

                # Display additional faculty information based on the prediction
                faculty_info = {
                    "Agriculture": "Departments: Agronomy, Animal Science, Crop Science, Soil Science.",
                    "Science": "Departments: Chemistry, Physics, Biology, Mathematics, Computer Science.",
                    "Clinical Sciences": "Departments: Medicine, Surgery, Dentistry, Pediatrics."
                    # Add more faculties as needed
                }

                # Check if the predicted faculty has additional information
                if prediction_label[0] in faculty_info:
                    st.markdown(f"<p style='color: white;'>{faculty_info[prediction_label[0]]}</p>", unsafe_allow_html=True)
    elif non_zero_subjects < 4:
        st.write("You must provide scores for at least 4 subjects.")
    else:
        st.write("Please limit the input to exactly 4 subjects.")

# Set background image at the end
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url('https://raw.githubusercontent.com/Ayo-tech-ai/jamb/main/background.jpg');
        background-size: cover;  /* Fills the screen but may crop */
        background-position: center;
        background-attachment: fixed;  /* Keeps the background fixed while scrolling */
    }}
    </style>
    """, unsafe_allow_html=True
                    )
