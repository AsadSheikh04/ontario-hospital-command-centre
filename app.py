
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

# Show a performance metric
latest_wait = df["Average_Wait_Hours"].iloc[-1]

st.metric(
    label="Latest Provincial Average Wait",
    value=f"{latest_wait:.1f} hours"
)

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
