
# Ontario Hospital Command Centre
# Healthcare Operations & Patient Flow Analytics

import streamlit as st
import pandas as pd

# Configure the website
st.set_page_config(
    page_title="Ontario Hospital Command Centre",
    page_icon="🏥",
    layout="wide"
)

# Dashboard title
st.title("🏥 Ontario Hospital Command Centre")

st.subheader("Emergency Department Performance")

st.write(
    "An interactive healthcare management dashboard "
    "using publicly reported Ontario Health data."
)

# Load our cleaned Ontario Health dataset
df = pd.read_csv("ontario_ed_dashboard_data.csv")


# Interactive reporting month selector
selected_month = st.selectbox(
    "Select a reporting month",
    df["Month_Label"].tolist(),
    index=len(df) - 1
)

# Find the waiting time for the selected month
selected_row = df[
    df["Month_Label"] == selected_month
].iloc[0]

selected_wait = selected_row["Average_Wait_Hours"]


# Step 1.30: Compare waiting times with the previous month

# Find the selected month's position
month_list = df["Month_Label"].tolist()
selected_index = month_list.index(selected_month)

# Check if a previous month exists
if selected_index > 0:

    # Get the previous month's waiting time
    previous_wait = df.iloc[
        selected_index - 1
    ]["Average_Wait_Hours"]

    # Calculate the difference
    monthly_change = selected_wait - previous_wait

    # Display waiting time and change
    st.metric(
        label=f"Provincial Average Wait — {selected_month}",
        value=f"{selected_wait:.1f} hours",
        delta=f"{monthly_change:+.1f} hours vs previous month",
        delta_color="inverse"
    )

else:
    # First month has no previous month to compare
    st.metric(
        label=f"Provincial Average Wait — {selected_month}",
        value=f"{selected_wait:.1f} hours"
    )

    st.caption("No previous month available for comparison.")

# Display the historical trend
st.subheader("Emergency Department Wait-Time Trends")

st.line_chart(
    df.set_index("Month_Label")["Average_Wait_Hours"]
)

# Display source data
st.subheader("Ontario Health Dataset")
st.dataframe(df, hide_index=True)

st.caption(
    "Source: Ontario Health / CIHI NACRS. "
    "Provincial monthly averages for first assessment "
    "by a doctor. Historical data, not live wait times."
)
