import streamlit as st
import requests
import base64

# Setting the page configuration, including title and icon
st.set_page_config(page_title='CCF_Detection', page_icon=":credit_card:")

# Adding a background image
def add_background(image_file):
    with open(image_file, "rb") as file:
        img_data = file.read()
    encoded_image = base64.b64encode(img_data).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/jpeg;base64,{encoded_image});
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Function to preprocess input features for prediction
def card_pred(atd, trans_amt, is_declined, tdd, is_foreignT, hrc, dCB, mCB, cBf):
    is_declined = 1 if is_declined == "Yes" else 0
    is_foreignT = 1 if is_foreignT == "Yes" else 0
    hrc = 1 if hrc == "Yes" else 0
    
    # Define your features here
    features = {
        "atd": atd,
        "trans_amt": trans_amt,
        "is_declined": is_declined,
        "tdd": tdd,
        "is_foreignT": is_foreignT,
        "hrc": hrc,
        "dCB": dCB,
        "mCB": mCB,
        "cBf": cBf
    }
    return features

# Main function to create the Streamlit web app
def main():
    
    add_background("background.jpg")  # Add your background image file here
    
    # Sidebar for explanations
    st.sidebar.title("Feature Explanations")
    st.sidebar.write("""
    - **Average Amount/transaction/day (atd):** The daily average amount spent in transactions.
    - **Transaction Amount (trans_amt):** The amount involved in the current transaction.
    - **Declined Transaction (is_declined):** Whether the transaction was declined before (Yes/No).
    - **Total Declines per Day (tdd):** The total number of declined transactions in a day.
    - **Foreign Transaction (is_foreignT):** Indicates if the transaction is foreign (Yes/No).
    - **High-risk Country (hrc):** Indicates if the transaction is from a high-risk country (Yes/No).
    - **Daily Cashback Average Amount (dCB):** The daily average cashback received.
    - **6 Months Cashback Average (mCB):** The average cashback received over the last 6 months.
    - **6 Months Cashback Frequency (cBf):** How often cashback was received in the last 6 months.
    """)

    st.title("Credit Card Fraud Detection")
    st.write("Enter credit card transaction details for prediction:")

    # Input fields for user to provide data
    atd = st.number_input('Average Amount/transaction/day', value=0, step=1, format="%d")
    trans_amt = st.number_input('Enter transaction amount', value=0, step=1, format="%d")
    option = ('Yes', 'No')
    is_declined = st.selectbox('Declined Transaction', option)
    tdd = st.number_input('Total declines per day', value=0, step=1, format="%d")
    is_foreignT = st.selectbox("Foreign Transaction", ('Yes', 'No'))
    hrc = st.selectbox("High-risk Country", ('Yes', 'No'))
    dCB = st.number_input('Daily cashback average amount', value=0, step=1, format="%d")
    mCB = st.number_input('6 months average cashback amount', value=0, step=1, format="%d")
    cBf = st.number_input('6 months cashback frequency', value=0, step=1, format="%d")

    # Button to trigger the prediction
    if st.button("Predict"):
        try:
            # Prepare the features for prediction
            features = card_pred(atd, trans_amt, is_declined, tdd, is_foreignT, hrc, dCB, mCB, cBf)
            data = {"features": features}  # Create a JSON payload with the features

            # Send a POST request to the prediction API
            response = requests.post("https://flaskaa.pythonanywhere.com/predict", json=data)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Parse the JSON response
                result = response.json()

                # Get the prediction from the result
                prediction = result.get("prediction")
                # Display the prediction to the user
                st.write(f"Prediction: {'Fraudulent' if prediction == 1 else 'Not Fraudulent'}")

            else:
                # Display an error message if the request was not successful
                st.write(f"Error {response.text}")

        except Exception as e:
            # Display an error message if an exception occurs
            st.write(f"Error {e}")

if __name__ == "__main__":
    # Call the main function to run the Streamlit app
    main()
