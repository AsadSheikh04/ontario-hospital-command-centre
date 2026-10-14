
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


# Step 1.31: Historical performance summary

# Calculate the mean of the monthly averages
historical_average = df["Average_Wait_Hours"].mean()

# Find the lowest and highest monthly values
historical_min = df["Average_Wait_Hours"].min()
historical_max = df["Average_Wait_Hours"].max()

# Add a section heading
st.subheader("Historical Performance Summary")

# Create two side-by-side KPI cards
col1, col2 = st.columns(2)

with col1:
    st.metric(
        label="13-Month Average",
        value=f"{historical_average:.2f} hours"
    )

with col2:
    st.metric(
        label="13-Month Range",
        value=f"{historical_min:.1f}–{historical_max:.1f} hours"
    )

st.caption(
    "Historical reference: August 2025–August 2026. "
    "The 13-month average is an unweighted mean of "
    "published provincial monthly averages, not a "
    "patient-weighted average or performance target."
)


# Step 1.32: Automated management performance insight

# Compare the selected month with the historical average
difference_hours = selected_wait - historical_average

# Convert the difference into minutes
difference_minutes = abs(difference_hours * 60)

# Describe the direction of the difference
if difference_hours > 0:
    comparison = "above"
elif difference_hours < 0:
    comparison = "below"
else:
    comparison = "equal to"

# Display an automated summary
st.subheader("Management Performance Insight")

st.info(
    f"In {selected_month}, the provincial average wait "
    f"for first doctor assessment was {selected_wait:.1f} hours. "
    f"This was {difference_minutes:.0f} minutes {comparison} "
    f"the 13-month reference average of "
    f"{historical_average:.2f} hours."
)

st.caption(
    "This descriptive comparison does not establish "
    "the causes of waiting-time changes or indicate "
    "whether an official performance target was met."
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



# Step 1.34: Interactive hospital comparison

st.divider()

st.header("🏥 Hospital Performance Comparison")

st.write(
    "Compare average emergency department waiting times "
    "across selected Ontario hospital sites for August 2026."
)

# Load our hospital-level dataset
hospital_comparison = pd.read_csv(
    "ontario_hospital_comparison_aug2026.csv"
)

# Separate the Ontario benchmark from hospital sites
provincial_average = hospital_comparison.loc[
    hospital_comparison["Hospital"] == "Ontario (Provincial)",
    "Average_Wait_Hours"
].iloc[0]

hospital_sites = hospital_comparison[
    hospital_comparison["Hospital"] != "Ontario (Provincial)"
].copy()

# Allow visitors to choose hospitals
selected_hospitals = st.multiselect(
    "Select hospitals to compare",
    options=hospital_sites["Hospital"].tolist(),
    default=hospital_sites["Hospital"].tolist()
)

# Filter the data to selected hospitals
filtered_hospitals = hospital_sites[
    hospital_sites["Hospital"].isin(selected_hospitals)
]

# Display our interactive chart
if not filtered_hospitals.empty:

    st.bar_chart(
        filtered_hospitals.set_index("Hospital")[
            "Average_Wait_Hours"
        ],
        horizontal=True
    )

else:
    st.warning("Please select at least one hospital.")

# Display the provincial reference
st.metric(
    "Ontario Provincial Average (August 2026)",
    f"{provincial_average:.1f} hours"
)

st.caption(
    "Source: Ontario Health / CIHI NACRS, August 2026. "
    "Indicator: average time to first assessment by a doctor. "
    "Hospital comparisons are descriptive and are not "
    "adjusted for patient characteristics, urgency, "
    "hospital size, or service complexity."
)


# Step 1.35: Hospital vs provincial benchmark

st.subheader("Hospital vs Ontario Benchmark")

# Let visitors choose one hospital
selected_hospital = st.selectbox(
    "Choose a hospital for comparison",
    options=hospital_sites["Hospital"].tolist()
)

# Find the selected hospital's waiting time
hospital_wait = hospital_sites.loc[
    hospital_sites["Hospital"] == selected_hospital,
    "Average_Wait_Hours"
].iloc[0]

# Calculate the difference in minutes
difference_minutes = (
    hospital_wait - provincial_average
) * 60

# Display two KPI cards
col1, col2 = st.columns(2)

with col1:
    st.metric(
        label="Selected Hospital Average",
        value=f"{hospital_wait:.1f} hours"
    )

with col2:
    st.metric(
        label="Difference from Ontario Average",
        value=f"{difference_minutes:+.0f} minutes",
        delta="Compared with provincial average",
        delta_color="off"
    )

# Explain the result
if difference_minutes > 0:
    comparison_text = "longer than"
elif difference_minutes < 0:
    comparison_text = "shorter than"
else:
    comparison_text = "equal to"

st.info(
    f"In August 2026, {selected_hospital} reported "
    f"an average wait of {hospital_wait:.1f} hours. "
    f"This was {abs(difference_minutes):.0f} minutes "
    f"{comparison_text} the Ontario provincial "
    f"average of {provincial_average:.1f} hours."
)

st.caption(
    "Descriptive comparison of published averages only. "
    "Differences are not risk-adjusted and do not "
    "establish hospital quality or management effectiveness."
)



# Step 1.36: Downloadable hospital benchmark report

st.subheader("Download Hospital Performance Report")

# Prepare a report containing all six hospital sites
comparison_report = hospital_sites[
    ["Hospital", "Average_Wait_Hours", "Reporting_Month"]
].copy()

# Add the Ontario provincial reference
comparison_report["Ontario_Average_Hours"] = provincial_average

# Calculate each hospital's difference in minutes
comparison_report["Difference_Minutes"] = (
    (comparison_report["Average_Wait_Hours"] -
     comparison_report["Ontario_Average_Hours"]) * 60
).round().astype(int)

# Convert the report into downloadable CSV data
csv_report = comparison_report.to_csv(
    index=False
).encode("utf-8-sig")

# Create the download button
st.download_button(
    label="📥 Download Hospital Comparison Report",
    data=csv_report,
    file_name="ontario_hospital_benchmark_report.csv",
    mime="text/csv"
)

st.caption(
    "Report contains six selected hospital sites for "
    "August 2026. Source: Ontario Health / CIHI NACRS. "
    "Comparisons are unadjusted and should not be used "
    "alone to rank hospital performance."
)
