import streamlit as st
import pandas as pd

# Load the Excel file
df = pd.read_excel("vol72.xlsx", engine="openpyxl")
# Clean Day column
df['Day'] = pd.to_numeric(df['Day'], errors='coerce')
df = df.dropna(subset=['Day'])
df['Day'] = df['Day'].astype(int)

# Separate warmup/cooldown if needed later
warmcool_blocks = ['W1', 'W2', 'W3', 'W4', 'W5', 'W6', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8']
df_main = df[~df["Block"].isin(warmcool_blocks)]

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["🏋️ Workouts"])

# ─────────────────────────────────────────────
# PAGE: Workouts
# ─────────────────────────────────────────────
if page == "🏋️ Workouts":
    st.title("🏋️ RISE Vol.72 Workout Tracker")

    selected_day = st.sidebar.selectbox("Select Day", sorted(df_main['Day'].unique()))
    day_df = df_main[df_main["Day"] == selected_day]

    # Get all unique groups for this day (e.g., A, B1, C2)
    groups = day_df["Group"].unique()

    for group in groups:
        group_df = day_df[day_df["Group"] == group]
        exercise_options = group_df["Primary Exercise"].tolist()

        st.markdown(f"### {group}")
        selected_exercise = st.selectbox(f"Choose exercise for {group}", exercise_options, key=f"exercise_{group}_{selected_day}")
        exercise_row = group_df[group_df["Primary Exercise"] == selected_exercise].iloc[0]

        st.write(f"**Sets x Reps:** {exercise_row['Sets x Reps']}")
        st.write(f"**RPE:** {exercise_row['RPE']}")
        st.write(f"**Notes from Coach:** {exercise_row['Notes']}")

        weight = st.text_input("💪 Weight Used", key=f"weight_{group}_{selected_day}")
        reps = st.text_input("🔁 Reps", key=f"reps_{group}_{selected_day}")
        user_notes = st.text_area("🗒️ Your Notes", key=f"usernotes_{group}_{selected_day}")
        st.checkbox("✅ Mark Done", key=f"done_{group}_{selected_day}")
