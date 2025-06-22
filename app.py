import streamlit as st
import pandas as pd

# Load the Excel file
df = pd.read_excel("vol72.xlsx", engine="openpyxl")

# Clean up
df = df[df['Day'].notna()]
df['Day'] = df['Day'].astype(int)

# Split warm-up and cool-down into a separate DataFrame
warmup_cooldown_blocks = ['W1', 'W2', 'W3', 'W4', 'W5', 'W6', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8']
df_main = df[~df['Block'].isin(warmup_cooldown_blocks)]
df_warmcool = df[df['Block'].isin(warmup_cooldown_blocks)]

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Workouts", "Warm-Up & Cool Down"])

# ─────────────────────────────────────────────
# PAGE 1: WORKOUT TRACKER
# ─────────────────────────────────────────────
if page == "Workouts":
    st.title("🏋️ RISE Vol.72 Workout Tracker")

    selected_day = st.sidebar.selectbox("Select Day", sorted(df_main['Day'].unique()))
    selected_blocks = st.sidebar.multiselect(
        "Select Block(s)", 
        sorted(df_main[df_main["Day"] == selected_day]["Block"].unique())
    )

    filtered = df_main[(df_main["Day"] == selected_day)]
    if selected_blocks:
        filtered = filtered[filtered["Block"].isin(selected_blocks)]

    for _, row in filtered.iterrows():
        with st.expander(f"{row['Block']}: {row['Primary Exercise']}"):
            st.write(f"**Sets x Reps:** {row['Sets x Reps']}")
            st.write(f"**RPE:** {row['RPE']}")
            st.write(f"**Alt 1:** {row['Alt 1']}")
            st.write(f"**Alt 2:** {row['Alt 2']}")
            st.write(f"**Alt 3:** {row['Alt 3']}")
            st.text_input("Weight Used", key=f"weight_{row['Block']}_{row['Primary Exercise']}")
            st.text_area("Notes", key=f"notes_{row['Block']}_{row['Primary Exercise']}")
            st.checkbox("✅ Done", key=f"done_{row['Block']}_{row['Primary Exercise']}")

# ─────────────────────────────────────────────
# PAGE 2: WARM-UP & COOL DOWN
# ─────────────────────────────────────────────
elif page == "Warm-Up & Cool Down":
    st.title("🧘 Warm-Up & Cool Down")

    selected_day = st.selectbox("Select Day", sorted(df_warmcool['Day'].unique()))

    filtered = df_warmcool[df_warmcool["Day"] == selected_day]

    warm = filtered[filtered['Block'].str.startswith("W")]
    cool = filtered[filtered['Block'].str.startswith("C")]

    st.subheader("🔥 Warm-Up")
    for _, row in warm.iterrows():
        st.markdown(f"**{row['Block']}** — {row['Primary Exercise']} ({row['Sets x Reps']})")
        if row['Alt 1']: st.markdown(f"Alt: {row['Alt 1']}")
        if row['Alt 2']: st.markdown(f"Alt: {row['Alt 2']}")

    st.subheader("❄️ Cool Down")
    for _, row in cool.iterrows():
        st.markdown(f"**{row['Block']}** — {row['Primary Exercise']} ({row['Sets x Reps']})")
        if row['Alt 1']: st.markdown(f"Alt: {row['Alt 1']}")
        if row['Alt 2']: st.markdown(f"Alt: {row['Alt 2']}")
