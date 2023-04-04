import streamlit as st
import pandas as pd
import datetime as dt
import pickle
from google.oauth2 import service_account
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from googleapiclient.errors import Error

# Load the trained model
with open('model.pkl', 'rb') as file:
    model = pickle.load(file)

# Set up the streamlit app
st.set_page_config(page_title="Assignment Dumps", page_icon=":books:")
st.title("Assignment Dumps 📚")
st.sidebar.success("Select a page below.")

# Set up the sidebar
st.sidebar.title("Navigation 🧭")
nav = st.sidebar.radio("Go to", ("Due Date Prediction 🧠", "View Calendar 📆"))



if nav == "Due Date Prediction 🧠":
    difficulty = st.slider("Select the difficulty of the assignment (1 = easy, 5 = difficult)", 1, 5)
    workload = st.slider("Select the workload of the student (number of assignments left)", 1, 10)
    assign_date = st.date_input("Select the assignment start date")

    # Calculate the due date using the trained model
    if assign_date and difficulty and workload:
        days_to_complete = model.predict([[difficulty, workload]])[0]
        due_date = assign_date + dt.timedelta(days=int(days_to_complete))

        # Format the due date as a string
        due_date_str = f"{due_date.month}/{due_date.day}/{due_date.year}"

        # Display the due date and allow the user to accept or reject it
        accepted = st.button("Accept")
        rejected = st.button("Reject")
        if accepted:
            # If the user accepts the due date, add it to the calendar
            # Here you would add the code to add the task to your calendar API
            st.write(f"The due date for the task is {due_date_str}")
            st.write("Task added to calendar")
            
        elif rejected:
            # If the user rejects the due date, allow them to manually enter a due date
            manual_date = st.date_input("Enter a due date")
            submitted = st.button("Submit")
            if submitted and manual_date:
                # Here you would add the code to add the task to your calendar API using the manually entered date
                st.write("Task added to calendar")
                st.write(f"The due date for the task is {manual_date.month}/{manual_date.day}/{manual_date.year}")
    else:
        st.write("Please input all the required fields to get the due date")

elif nav == "View Calendar 📆":
    # Here you would add the code to retrieve tasks from your calendar API and display them
    st.write("Calendar view not implemented yet")
