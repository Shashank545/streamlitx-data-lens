import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import openai
from openai import OpenAI
import numpy as np
from datetime import datetime, timedelta
import random


OPENAI_API_KEY = "ENTER_YOUR_OPENAI_KEY"

client = OpenAI(api_key=OPENAI_API_KEY)

# Load the sample CSV
@st.cache_data
def load_data():
    return pd.read_csv('data.csv')

# Function to call OpenAI API
def get_gpt4_response(prompt, data):
    # openai.api_key = OPENAI_API_KEY
    # print(data)
    response = client.chat.completions.create(
    messages=[
            {"role": "system", "content": "You are a helpful data anlytics assistant."},
            {"role": "user", "content": f"{prompt} Data: {data}"}
        ],
    model="gpt-4",
    max_tokens= 200,
    temperature= 0.1
    )

    print(response)
    
    # response = openai.ChatCompletion.create(
    #     model="gpt-4",
    #     messages=[
    #         {"role": "system", "content": "You are a helpful assistant."},
    #         {"role": "user", "content": prompt}
    #     ]
    # )
    # return response.choices[0].message['content'].strip()
    return response.choices[0].message.content

# Streamlit app
def main():
    st.title("LLM App with Streamlit")
    
    # # Load data
    # data = load_data()
    # Create a mock dataset
    data = {
        'post_id': np.arange(1, 101),
        'username': [f'user_{i}' for i in range(1, 101)],
        'tweet_content': [f'This is tweet number {i}' for i in range(1, 101)],
        'num_likes': np.random.randint(0, 500, size=100),
        'num_retweets': np.random.randint(0, 300, size=100),
        'date': [datetime.now() - timedelta(days=random.randint(0, 365)) for _ in range(100)],
        'is_retweet': np.random.choice([True, False], size=100)
    }
    
    # Display data
    st.subheader("Sample Data")
    st.dataframe(data)
    
    # Interactive visualization
    st.subheader("Interactive Visualization")
    fig, ax = plt.subplots()
    ax.bar(data['username'], data['num_likes'])
    st.pyplot(fig)
    
    # OpenAI GPT-4 Inference
    st.subheader("GPT-4 Inference")
    user_input = st.text_area("Enter your prompt for GPT-4:", "Analyze the data below and provide insights.")
    if st.button("Get GPT-4 Response"):
        with st.spinner("Generating response..."):
            response = get_gpt4_response(user_input, data)
            st.text_area("GPT-4 Response:", response, height=200)

if __name__ == "__main__":
    main()
