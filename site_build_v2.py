import sqlite3
import streamlit as st
import pandas as pd
import datetime as dt
import pickle
from google.oauth2 import service_account
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from googleapiclient.errors import Error
import streamlit_authenticator as stauth

with open('model.pkl', 'rb') as file:
    model = pickle.load(file)


# Security
# passlib,hashlib,bcrypt,scrypt
import hashlib


def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()


def check_hashes(password, hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False


# DB Management
conn = sqlite3.connect('data.db')
c = conn.cursor()
# DB  Functions


def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')


def add_userdata(username, password):
    c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',
              (username, password))
    conn.commit()


def login_user(username, password):
    c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',
              (username, password))
    data = c.fetchall()
    return data


def view_all_users():
    c.execute('SELECT * FROM userstable')
    data = c.fetchall()
    return data


def main():
    """Simple Login App"""

    # st.title("Simple Login App")

    menu = ["Home", "Login", "SignUp"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Home")

    elif choice == "Login":
        st.subheader("Login Section")

        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password", type='password')
        if st.sidebar.checkbox("Login"):
            # if password == '12345':
            create_usertable()
            hashed_pswd = make_hashes(password)

            result = login_user(username, check_hashes(password, hashed_pswd))
            if result:

                st.success("Logged In as {}".format(username))
                


                st.title("Assignment Dumps 📚")
                st.sidebar.success("Select a page below.")

                # Set up the sidebar
                st.sidebar.title("Navigation 🧭")
                nav = st.sidebar.radio("Go to", ("Teacher's Dashboard 👩‍🏫",
                                    "Student's Dashboard 🧑‍🎓", "Due Date Prediction 🧠", "View Calendar 📆"))

                if nav == "Due Date Prediction 🧠":
                    difficulty = st.slider(
                        "Select the difficulty of the assignment (1 = easy, 5 = difficult)", 1, 5)
                    workload = st.slider(
                        "Select the workload of the student (number of assignments left)", 1, 10)
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
                                st.write(
                                    f"The due date for the task is {manual_date.month}/{manual_date.day}/{manual_date.year}")
                    else:
                        st.write("Please input all the required fields to get the due date")

                elif nav == "View Calendar 📆":
                    # Here you would add the code to retrieve tasks from your calendar API and display them
                    st.write("Calendar view not implemented yet")

                elif nav == "Student's Dashboard 🧑‍🎓":
                    # Generate the HTML div containing the assignment details
                    assignment_div = '''
                        <style>
                            @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@100&display=swap');
                        </style>
                        <div style="background-color:#262730; border-radius: 50px; height: 50px; display: flex; align-items: center; justify-content: center;">
                            <h1 style="font-family: 'Poppins'; color: white; font-size: 24px;">Feed</h1>
                        </div>
                        <div style="flex-direction: row; margin-top: 50px;">
                            <div style="background-color:#262730; border-radius: 50px; height: 400px; margin-left: 0%; padding: 0px -200px 50px 100px;">
                                <h2 style="font-family: 'Poppins'; color: white; font-size: 25px;margin-left: 30px; margin-bottom: -20px;">Marked Assignment </h2>
                                <h4 style="font-family: 'Poppins'; color: white; font-size: 20px;margin-left: 30px; margin-bottom: 0px;">By Steve Appleseed</h4>
                                <h4 style="font-family: 'Poppins'; color: white; font-size: 20px;margin-left: 500px;margin-top: -70px;">24th March 2023</h4>
                                <h4 style="font-family: 'Poppins'; color: white; font-size: 20px;margin-left: 500px;margin-top: 0px">Due: 1st April 2023</p>
                                <h4 style="font-family: 'Poppins'; color: white; font-size: 18px;margin-left: 30px;margin-top: -40px">hh:mm</p>
                                <div style="height: 120px; width: 120px; border: 10px solid white; margin-bottom: 20px;border-radius:20px"></div>
                                <h4 style="font-family: 'Poppins'; color: white; font-size: 18px; margin-top:-20px;margin-left:30px">Topic: Sorting</h4>
                                <button style="background-color: red; color: white; font-size: 20px; border: none; padding: 0px 40px; border-radius: 10px;margin-left:500px;margin-top:-100px">Submit</button>
                            </div>
                        </div>
                        <div style="flex-direction: row; margin-top: 50px;">
                            <div style="background-color:#262730; border-radius: 50px; height: 400px; margin-left: 0%; padding: 0px -200px 50px 100px;">
                                <h2 style="font-family: 'Poppins'; color: white; font-size: 25px;margin-left: 30px; margin-bottom: -20px;">Unmarked Assignment</h2>
                                <h4 style="font-family: 'Poppins'; color: white; font-size: 15px;margin-left: 30px; margin-bottom: 0px;">ML Generated - QB Searching</h4>
                                <h4 style="font-family: 'Poppins'; color: white; font-size: 20px;margin-left: 500px;margin-top: -70px;">24th March 2023</h4>
                                <h4 style="font-family: 'Poppins'; color: white; font-size: 20px;margin-left: 500px;margin-top: 0px">Due: 1st April 2023</p>
                                <h4 style="font-family: 'Poppins'; color: white; font-size: 18px;margin-left: 30px;margin-top: -40px">hh:mm</p>
                                <div style="height: 120px; width: 120px; border: 10px solid white; margin-bottom: 20px;border-radius:20px"></div>
                                <h4 style="font-family: 'Poppins'; color: white; font-size: 18px; margin-top:-20px;margin-left:30px">Topic Name</h4>
                                <button style="background-color: red; color: white; font-size: 20px; border: none; padding: 0px 40px; border-radius: 10px;margin-left:500px;margin-top:-100px">Submit</button>
                            </div>
                        </div>
                    '''

                    # Display the HTML div
                    st.markdown(assignment_div, unsafe_allow_html=True)

                elif nav == "Teacher's Dashboard 👩‍🏫":
                    # Generate the HTML div containing the assignment details
                    assignment_div = '''
                        <style>
                            @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@100&display=swap');
                        </style>
                        <div style="background-color:#262730; border-radius: 50px; height: 50px; display: flex; align-items: center; justify-content: center;">
                            <h1 style="font-family: 'Poppins'; color: white; font-size: 24px;">Submissions</h1>
                        </div>
                        <div style="flex-direction: row; margin-top: 50px;">
                            <div style="background-color:#262730; border-radius: 50px; height: 400px; margin-left: 0%; padding: 0px -200px 50px 100px;">
                                <h2 style="font-family: 'Poppins'; color: white; font-size: 25px;margin-left: 30px; margin-bottom: -20px;">Marked Assignment Posted</h2>
                                <h4 style="font-family: 'Poppins'; color: white; font-size: 20px;margin-left: 30px; margin-bottom: 0px;">By Steve Appleseed</h4>
                                <h4 style="font-family: 'Poppins'; color: white; font-size: 20px;margin-left: 500px;margin-top: -70px;">24th March 2023</h4>
                                <h4 style="font-family: 'Poppins'; color: white; font-size: 20px;margin-left: 500px;margin-top: 0px">Due: 1st April 2023</p>
                                <h4 style="font-family: 'Poppins'; color: white; font-size: 18px;margin-left: 30px;margin-top: -40px">hh:mm</p>
                                <div style="height: 120px; width: 120px; border: 10px solid white; margin-bottom: 20px;border-radius:20px"></div>
                                <h4 style="font-family: 'Poppins'; color: white; font-size: 18px; margin-top:-20px;margin-left:30px">Topic: Sorting</h4>
                                <button style="background-color: red; color: white; font-size: 20px; border: none; padding: 0px 40px; border-radius: 10px;margin-left:500px;margin-top:-100px">Grade</button>
                            </div>
                        </div>
                        <div style="flex-direction: row; margin-top: 50px;">
                            <div style="background-color:#262730; border-radius: 50px; height: 400px; margin-left: 0%; padding: 0px -200px 50px 100px;">
                                <h2 style="font-family: 'Poppins'; color: white; font-size: 25px;margin-left: 30px; margin-bottom: -20px;">Unmarked Assignment Posted</h2>
                                <h4 style="font-family: 'Poppins'; color: white; font-size: 15px;margin-left: 30px; margin-bottom: 0px;">ML Generated - QB Searching</h4>
                                <h4 style="font-family: 'Poppins'; color: white; font-size: 20px;margin-left: 500px;margin-top: -70px;">24th March 2023</h4>
                                <h4 style="font-family: 'Poppins'; color: white; font-size: 20px;margin-left: 500px;margin-top: 0px">Due: 1st April 2023</p>
                                <h4 style="font-family: 'Poppins'; color: white; font-size: 18px;margin-left: 30px;margin-top: -40px">hh:mm</p>
                                <div style="height: 120px; width: 120px; border: 10px solid white; margin-bottom: 20px;border-radius:20px"></div>
                                <h4 style="font-family: 'Poppins'; color: white; font-size: 18px; margin-top:-20px;margin-left:30px">Topic Name</h4>
                                <button style="background-color: red; color: white; font-size: 20px; border: none; padding: 0px 40px; border-radius: 10px;margin-left:500px;margin-top:-100px">Grade</button>
                            </div>
                        </div>
                    '''

                    # Display the HTML div
                    st.markdown(assignment_div, unsafe_allow_html=True)
        else:
            st.warning("Incorrect Username/Password")

    elif choice == "SignUp":
        st.subheader("Create New Account")
        new_user = st.text_input("Username")
        new_password = st.text_input("Password", type='password')

        if st.button("Signup"):
            create_usertable()
            add_userdata(new_user, make_hashes(new_password))
            st.success("You have successfully created a valid Account")
            st.info("Go to Login Menu to login")


if __name__ == '__main__':
    main()
