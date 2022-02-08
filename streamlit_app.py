# imports

import streamlit as st
import pandas as pd
import pickle
import numpy as np

model = pickle.load(open('lr.pkl','rb'))
poly = pickle.load(open('poly.pkl','rb'))
ss = pickle.load(open('ss.pkl','rb'))


def predictions (gender, age, hypertension, heart_disease, ever_married, residence_type, avg_glucose_level, bmi, senior, smoking_status_formerly_smoked, smoking_status_never_smoked, smoking_status_smokes, work_type_Never_worked, work_type_Private, work_type_Self_employed, work_type_children):

    if gender == 'Male':
        gender = 1
    elif gender == 'Female':
        gender = 0
    else:
        gender = -1

    if age >= 65:
        senior = 1
    else:
        senior = 0

    if ever_married == 'Yes':
        ever_married = 1
    else:
        ever_married = 0

    if residence_type == 'Urban':
        residence_type = 1
    else:
        residence_type = 0

    if smoking_status == 'formerly_smoked':
        smoking_status_formerly_smoked = 1
    elif smoking_status == 'never_smoked':
        smoking_status_never_smoked = 1
    elif smoking_status == 'smokes':
        smoking_status_smokes = 1

    if work_type == 'Private':
        work_type_Private = 1
    elif work_type == 'Self_employed':
        work_type_Self_employed = 1
    elif work_type == 'children':
        work_type_children = 1
    elif work_type == 'Never_worked':
        work_type_Never_worked =1

    polyfeatures = poly.transform([[gender, age, hypertension, heart_disease, ever_married, residence_type, avg_glucose_level, bmi, senior, smoking_status_formerly_smoked, smoking_status_never_smoked, smoking_status_smokes, work_type_Never_worked, work_type_Private, work_type_Self_employed, work_type_children]])

    scaled = ss.transform(polyfeatures)

    prediction = model.predict_proba(scaled)[:,1]

    score = np.round(prediction * 100, 1)

    return score


st.title('Stroke Prediction')
st.write('By: Shuya Chen')

webpage = st.selectbox('Choose Your Page', ('Overview', 'Stroke Prediction'))

if webpage == 'Overview':
    st.title('Stroke Overview')
    st.write('Stroke is a disease that affects the arteries leading to and within the brain. It is the number five leading cause of death and disability in the United States. A stroke occurs when a blood vessel that carries oxygen and nutrients to the brain is either blocked by a clot or bursts. When that happens, part of the brain cannot get the blood and oxygen it needs, so it and brain cells die. Many people think a stroke happens in the heart, but it happens in the brain')

elif webpage == 'Stroke Prediction':

    st.title('How Likely Will You Get a Stroke?')

    gender = st.selectbox('GENDER', ('Male', 'Female', 'Other'))

    age = st.number_input('AGE')

    senior = 0

    hypertension = st.selectbox('HYPERTENSION? ( 0 for No and 1 for Yes )', (0, 1))

    heart_disease = st.selectbox('HEART DISEASE? ( 0 for No and 1 for Yes )', (0, 1))

    ever_married = st.selectbox('MARITAL STATUS', ('No', 'Yes'))

    work_type = st.selectbox('WORK TYPE', ('Private', 'Self_employed', 'Govt_job', 'children', 'Never_worked'))

    work_type_Private, work_type_Self_employed, work_type_children, work_type_Never_worked = 0, 0, 0, 0

    residence_type = st.selectbox('RESIDENCE TYPE', ('Urban', 'Rural'))

    avg_glucose_level= st.number_input('AVERAGE GLUCOSE LEVEL')

    bmi = st.number_input('BMI')

    smoking_status = st.selectbox('SMOKING STATUS', ('formerly_smoked', 'never_smoked', 'smokes', 'Unknown'))

    smoking_status_formerly_smoked, smoking_status_never_smoked, smoking_status_smokes = 0, 0, 0

    if st.button('Let Me Know'):
        results = predictions(gender, age, hypertension, heart_disease, ever_married, residence_type, avg_glucose_level, bmi, senior, smoking_status_formerly_smoked, smoking_status_never_smoked, smoking_status_smokes, work_type_Never_worked, work_type_Private, work_type_Self_employed, work_type_children)
        st.success('Your Chances of Having a Stroke is {} %'.format(results) )
