"""Streamlit Time Series Anomalies Detection App."""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.ensemble import IsolationForest


# Title and description
st.title("Interactive Time Series Anomaly Detection App")

# Explanation section
st.markdown("""
### How Anomalies are Detected

This app uses the **Isolation Forest** algorithm for anomaly detection. Isolation Forest is a tree-based model that works by identifying anomalies as data points that are isolated from the majority of the data. Here’s a simple breakdown of how the algorithm works:

- The algorithm creates an ensemble of trees to partition the dataset.
- Anomalies are data points that are located far from the bulk of the data, requiring fewer splits to isolate.
- The model is sensitive to the parameter called **contamination**, which controls the proportion of data points that are considered anomalies. In this case, we have set the contamination rate to 5%.

The red dots in the plot represent the detected anomalies. You can also filter the table to show only the anomalous data points by selecting the option below the plot.

Feel free to upload your own time series data to detect anomalies, ensuring that the data contains 'Time' and 'Value' columns.
""")


# Generate example time series data
np.random.seed(42)
time_series_length = 500
time = np.arange(time_series_length)
data = np.sin(0.05 * time) + np.random.normal(scale=0.3, size=time_series_length)

# Add some anomalies
data[100] = 3
data[300] = -3

# Create a DataFrame
df = pd.DataFrame({"Time": time, "Value": data})


# Anomaly Detection function
def detect_anomalies(dataframe, contamination=0.05):
    model = IsolationForest(contamination=contamination)
    dataframe["Anomaly"] = model.fit_predict(dataframe[["Value"]])
    dataframe["Anomaly"] = dataframe["Anomaly"].map({1: 0, -1: 1})
    return dataframe


# Detect anomalies
df = detect_anomalies(df)

# Plot time series data with anomalies using Plotly
fig = px.line(df, x="Time", y="Value", title="Time Series Data with Anomalies")
anomalies = df[df["Anomaly"] == 1]
fig.add_scatter(
    x=anomalies["Time"],
    y=anomalies["Value"],
    mode="markers",
    marker=dict(color="red", size=10),
    name="Anomaly",
)

# Display the Plotly figure in Streamlit
st.plotly_chart(fig, use_container_width=True)

# Add a checkbox to filter anomalies in the table
show_anomalies_only = st.checkbox("Show only anomalies in the table")

# Display the DataFrame, filtering anomalies if checkbox is selected
if show_anomalies_only:
    st.write("### Anomaly Data Table")
    st.write(df[df["Anomaly"] == 1])
else:
    st.write("### Full Data Table")
    st.write(df)

# Allow users to upload their own CSV file
st.write("### Upload Your CSV File for Analysis")
uploaded_file = st.file_uploader("Choose a file", type="csv")

if uploaded_file is not None:
    user_data = pd.read_csv(uploaded_file)

    # Check if the CSV contains the right columns
    if "Time" in user_data.columns and "Value" in user_data.columns:
        st.write("### Uploaded Data")
        st.write(user_data.head())

        # Detect anomalies in uploaded data
        user_data = detect_anomalies(user_data)

        # Plot uploaded time series data with anomalies
        fig = px.line(
            user_data,
            x="Time",
            y="Value",
            title="Uploaded Time Series Data with Anomalies",
        )
        uploaded_anomalies = user_data[user_data["Anomaly"] == 1]
        fig.add_scatter(
            x=uploaded_anomalies["Time"],
            y=uploaded_anomalies["Value"],
            mode="markers",
            marker=dict(color="red", size=10),
            name="Anomaly",
        )

        # Display the Plotly figure in Streamlit
        st.plotly_chart(fig, use_container_width=True)

        # Add a checkbox to filter anomalies in the table
        show_anomalies_only_uploaded = st.checkbox(
            "Show only anomalies in the uploaded data table"
        )

        # Display the DataFrame for uploaded data
        if show_anomalies_only_uploaded:
            st.write("### Uploaded Anomaly Data Table")
            st.write(user_data[user_data["Anomaly"] == 1])
        else:
            st.write("### Full Uploaded Data Table")
            st.write(user_data)

    else:
        st.error("Uploaded CSV file must contain 'Time' and 'Value' columns.")
