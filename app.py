import streamlit as st
import joblib
import numpy as np

# Load the trained model and encoder
model = joblib.load('jamb.joblib')  # your trained model
encoder = joblib.load('jamb_faculty_encoder.joblib')  # your label encoder

# Streamlit App Title
st.title('JAMB/UTME Faculty Match')

# Description of the app
st.write("An AI-powered App that predicts Jambites Faculty based on their UTME scores.")

# Arrange subjects in columns of two each
col1, col2 = st.columns(2)
with col1:
    Use_of_English = st.number_input("Use of English", min_value=0, step=1)
    Physics = st.number_input("Physics", min_value=0, step=1)
with col2:
    Chemistry = st.number_input("Chemistry", min_value=0, step=1)
    Biology = st.number_input("Biology", min_value=0, step=1)

# Separate field for Mathematics
st.write("")  # Empty space for better layout
Mathematics = st.number_input("Mathematics", min_value=0, step=1)

# Arrange Total Score and Predict button centrally
Total_Score = st.number_input("Total Score", min_value=0, step=1)

# Center-align the Predict button
button_centered = st.columns([1, 1, 1])
with button_centered[1]:
    predict_button = st.button('Predict')

# Collect all the input features into a list
input_features = [
    Use_of_English,
    Physics,
    Chemistry,
    Biology,
    Mathematics,
    Total_Score
]

# Count how many subjects have non-zero scores
subject_scores = [Use_of_English, Physics, Chemistry, Biology, Mathematics]
non_zero_subjects = sum(1 for score in subject_scores if score > 0)

# CSS styling for central alignment, font size increase, text stroke, and bold text of the predicted result
st.markdown("""
    <style>
        /* Centralize text */
        .center-text {
            text-align: center;
        }
        /* Apply green text stroke and increase font size */
        .result, h1, h2, h3, p {
            font-size: calc(16px + 3vw); /* Increases font size */
            -webkit-text-stroke: 1px green;  /* Green text stroke */
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# Display the result only when the Predict button is clicked
if predict_button:
    # Check if exactly 4 subjects have scores
    if non_zero_subjects == 4:
        # Ensure that Use of English is one of the selected subjects
        if Use_of_English == 0:
            st.write("Please include Use of English as it is compulsory when selecting 4 subjects.")
        else:
            # Check if the sum of the individual subject scores equals the Total_Score
            calculated_total_score = sum(subject_scores)  # Only subjects
            if calculated_total_score != Total_Score:
                st.write(f"The sum of your subject scores ({calculated_total_score}) does not match the Total Score ({Total_Score}). Please check and input the correct Total Score.")
            else:
                # Check if the total score is less than 150, and if so, predict "Not offered admission"
                if Total_Score < 150:
                    st.markdown("<div class='center-text result'>Predicted Faculty: Not offered admission</div>", unsafe_allow_html=True)
                else:
                    # Convert the input features into a numpy array (reshape to match model input)
                    input_array = np.array(input_features).reshape(1, -1)

                    # Use the model to make a prediction
                    prediction = model.predict(input_array)

                    # If an encoder is used, transform the predicted label back to the original class
                    prediction_label = encoder.inverse_transform(prediction)

                    # Display the result centrally and in bold font
                    st.markdown(f"<div class='center-text result'>Predicted Faculty: {prediction_label[0]}</div>", unsafe_allow_html=True)

                    # Display additional faculty information based on the prediction
                    faculty_info = {
                        "Agriculture": "Departments: Agronomy, Animal Science, Crop Science, Soil Science.",
                        "Science": "Departments: Chemistry, Physics, Biology, Mathematics, Computer Science.",
                        "Clinical Sciences": "Departments: Medicine, Surgery, Dentistry, Pediatrics."
                        # Add more faculties as needed
                    }

                    # Check if the predicted faculty has additional information
                    if prediction_label[0] in faculty_info:
                        st.markdown(f"<div class='center-text'>{faculty_info[prediction_label[0]]}</div>", unsafe_allow_html=True)
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
    """, unsafe_allow_html=True)
