%%writefile app.py
import streamlit as st
import gspread
from google.auth import default
from datetime import datetime

# Connect to Google Sheets
creds, _ = default()
gc = gspread.authorize(creds)

SHEET_NAME = "Home Inventory"

try:
    sh = gc.open(SHEET_NAME)
    worksheet = sh.get_worksheet(0)
except:
    st.error(f"Could not find a sheet named '{SHEET_NAME}'.")

st.title("🏡 Home & Shed Inventory")

# Main location selection
main_location = st.selectbox("Where are you?", ["The House", "Shed 1", "Shed 2", "Shed 3"])

# House vs Shed zones
if main_location == "The House":
    zone = st.selectbox("Which Room?", [
        "Area Behind Door (Right)", "Dining Room (Straight Ahead)",
        "Kitchen (To the Left)", "Living Room (Past Dining)",
        "Pantry 1", "Pantry 2", "Bathroom (Landmark)",
        "Dressing Room", "Master Bedroom (Sleeping)"
    ])
    shelf_label = "Specific Spot"
else:
    zone = st.selectbox("Which Color Section?", ["Green Section", "Yellow Section", "Pink Section", "Blue Section"])
    shelf_label = "Shelf Number"

# Inputs
shelf_val = st.text_input(shelf_label)
item_name = st.text_input("What are you storing?")

# Save button
if st.button("Save to Inventory"):
    if item_name:
        new_row = [main_location, zone, shelf_val, item_name, str(datetime.now().date())]
        worksheet.append_row(new_row)
        st.success(f"✅ Saved '{item_name}'!")

# Photo capture
st.divider()
st.subheader("📸 Receipt / Item Photo")
picture = st.camera_input("Take a photo")

