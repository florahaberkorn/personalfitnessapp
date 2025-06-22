import streamlit as st
import pandas as pd

# Load workout plan
df = pd.read_excel("RISE_Vol_72_All_Workouts_Cleaned.xlsx")

# Sidebar filters
day = st.sidebar.selectbox("Select Day", sorted(df['Day'].unique()))
block = st.sidebar.multiselect("Select Block", sorted(df['Block'].unique()))

# Filtered view
filtered = df[(df["Day"] == day) & (df["Block"].isin(block) if block else df["Block"])]

st.title(f"RISE Vol.72 – Day {day} Workout")

for _, row in filtered.iterrows():
    with st.expander(f"{row['Block']}: {row['Primary Exercise']}"):
        st.write(f"**Sets x Reps:** {row['Sets x Reps']}")
        st.write(f"**RPE:** {row['RPE']}")
        st.write(f"**Alt 1:** {row['Alt 1']}")
        st.write(f"**Alt 2:** {row['Alt 2']}")
        st.write(f"**Alt 3:** {row['Alt 3']}")
        st.text_input("Weight Used", key=f"weight_{row['Block']}")
        st.text_area("Notes", key=f"notes_{row['Block']}")
        st.checkbox("✅ Mark Complete", key=f"done_{row['Block']}")
