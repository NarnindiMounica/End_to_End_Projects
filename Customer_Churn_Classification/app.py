import streamlit as st
import numpy as np
import pandas as pd
import tensorflow as tf

from tensorflow.keras.models import load_model
import pickle

from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder

st.title("Customer Churn Classification")

#loading model

model = load_model("model.keras")

#loading encoding and scaler objects

with open('standard_scaler.pkl', 'rb') as file_obj:
    scaler = pickle.load(file_obj)

with open('onehot_encoder.pkl', 'rb') as file_obj:
    onehot_encoder = pickle.load(file_obj)

with open('label_encoder.pkl', 'rb') as file_obj:
    label_encoder = pickle.load(file_obj)        

#user inputs

#CreditScore,Geography,Gender,Age,Tenure,Balance,NumOfProducts,HasCrCard,IsActiveMember,EstimatedSalary

credit_score = st.number_input("Credit Score")
geography = st.selectbox("Geography", onehot_encoder.categories_[0])
gender = st.selectbox("Gender", label_encoder.classes_)
age = st.slider("Age", 18, 95)
tenure = st.slider("Tenure", 0, 10)
balance = st.number_input("Balance")
num_of_products = st.slider("Number of Products", 0, 4)
has_crcard = st.selectbox("Has Credit Card", [0, 1])
isactive_member = st.selectbox("Is Active Member", [0, 1])
estimated_salary = st.number_input("Estimated Salary")

input_data = {
    "CreditScore": credit_score, 
    "Geography": geography,
    "Gender": label_encoder.transform([gender]),
    "Age": age,
    "Tenure": tenure,
    "Balance": balance,
    "NumOfProducts": num_of_products,
    "HasCrCard": has_crcard,
    "IsActiveMember": isactive_member,
    "EstimatedSalary": estimated_salary

}

input_df = pd.DataFrame(input_data, index=[0])

#encoding categorical data
geography_df = pd.DataFrame(data=onehot_encoder.transform([[input_data['Geography']]]).toarray(), columns=onehot_encoder.get_feature_names_out())

input_df = pd.concat([input_df.drop(columns=['Geography']).reset_index(drop=True), geography_df.reset_index(drop=True)], axis=1)

#scaling data
input_arr = scaler.transform(input_df)

#predict churn

prediction = model.predict(input_arr)[0][0]

st.write(f"Prediction_Probability: {prediction}")

if prediction > 0.5:
    st.write("Customer is likely to churn")
else:
    st.write("Customer is not likely to churn")    






