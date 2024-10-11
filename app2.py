import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import openai
from openai import OpenAI
import numpy as np
from datetime import datetime, timedelta
import random

# Your OpenAI API key
OPENAI_API_KEY = "ENTER_YOUR_OPENAI_KEY"

# Initialize the OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Load the sample CSV
@st.cache_data
def load_data():
    return pd.read_csv('data.csv')

# Function to call OpenAI API
def get_gpt_response(prompt, data, model):
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a helpful data analytics assistant."},
            {"role": "user", "content": f"{prompt} Data: {data}"}
        ],
        model=model,
        max_tokens=200,
        temperature=0.1
    )

    return response.choices[0].message.content

# Streamlit app
def main():
    st.title("LLM App with Streamlit")

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

    # OpenAI GPT Model Selection
    st.subheader("GPT Model Selection")
    model_options = ["gpt-3.5-turbo", "gpt-4"]  # Add more models if available
    selected_model = st.selectbox("Choose a model:", model_options)

    # GPT Inference
    st.subheader(f"{selected_model.upper()} Inference")
    user_input = st.text_area("Enter your prompt for the model:", "Analyze the data below and provide insights.")
    if st.button("Get Response"):
        with st.spinner("Generating response..."):
            response = get_gpt_response(user_input, data, selected_model)
            st.text_area(f"{selected_model.upper()} Response:", response, height=200)

if __name__ == "__main__":
    main()
