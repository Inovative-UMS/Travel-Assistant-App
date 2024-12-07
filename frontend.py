import streamlit as st
import google.generativeai as genai
import os

# Set your Gemini API key
os.environ["GEMINI_API_KEY"] = "AIzaSyAQtS24w3Y-6paRAB91BlrQMZ1Sl-G2mKY"  # Replace with your actual API key
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

st.title("One-Day Tour Planning Assistant")

# Collect User Preferences
st.sidebar.title("Enter Your Preferences")
user = st.sidebar.text_input("Enter Your Name")
city = st.sidebar.text_input("City to Visit")
budget = st.sidebar.number_input("Budget ($)", min_value=0)
interests = st.sidebar.multiselect("Select Interests", ["Culture", "Adventure", "Food", "Shopping", "Business", "Education", "History"])
start_time = st.sidebar.time_input("Start Time")
end_time = st.sidebar.time_input("End Time")

if st.sidebar.button("Save Preferences"):
    preferences = {
        "user": user,
        "city": city,
        "budget": budget,
        "interests": interests,
        "timings": {"start_time": str(start_time), "end_time": str(end_time)}
    }
    # Save preferences to backend or database
    st.sidebar.success("Preferences saved successfully!")

# Generate Itinerary
if st.button("Generate Itinerary"):
    prompt = (
        f"Plan a one-day trip in {city} with a budget of ${budget}. "
        f"Interests include: {', '.join(interests)}. "
        f"Start time: {start_time}, End time: {end_time}."
    )
    model = genai.GenerativeModel('gemini-1.5-flash')  # Choose the appropriate model version
    response = model.generate_content(prompt)
    st.write("### Generated Itinerary")
    st.write(response.text)