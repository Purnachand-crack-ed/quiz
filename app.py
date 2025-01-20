import streamlit as st
import json
import random
import time
import sqlite3
# import smtplib
# from email.mime.text import MIMEText

# Load questions from the JSON file
with open('question.json') as f:
    quiz_data = json.load(f)

# Initialize session state variables
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'selected_questions' not in st.session_state:
    st.session_state.selected_questions = []

# Function to insert user data into the database
def insert_user_data(name, phone, email, marks):
    conn = sqlite3.connect('quiz_results.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO results (name, phone, email, marks)
        VALUES (?, ?, ?, ?)
    ''', (name, phone, email, marks))
    conn.commit()
    conn.close()

# Function to send email
# def send_email(to_email, name, score):
#     subject = "Your Quiz Results"
#     body = f"Hello {name},\n\nThank you for participating in the quiz! Your final score is: {score}.\n\nBest regards,\nQuiz Team"
    
#     msg = MIMEText(body)
#     msg['Subject'] = subject
#     msg['From'] = "your_email@example.com"  # Replace with your email
#     msg['To'] = to_email

#     # Send the email
#     with smtplib.SMTP('smtp.gmail.com', 587) as server:  # Replace with your SMTP server
#         server.starttls()
#         server.login("your_email@example.com", "your_password")  # Replace with your email and password
#         server.send_message(msg)

# Function to check if user already attempted the quiz
def user_attempted_quiz(phone, email):
    conn = sqlite3.connect('quiz_results.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM results WHERE phone = ? AND email = ?', (phone, email))
    result = cursor.fetchone()
    conn.close()
    return result is not None

# Instructions page
if 'name' not in st.session_state:
    st.title("Quiz Instructions")
    st.write("Please follow these instructions to take the quiz:")
    st.write("1. Enter your name, phone number, and email to start the quiz.")
    st.write("2. You will have 7 minutes to complete the quiz.")
    st.write("3. Select one answer for each question.")
    st.write("4. Click the 'Submit' button to submit your answers.")
    st.write("5. After submitting, you will see your score and a thank you message.")
    
    name = st.text_input("Name")
    phone = st.text_input("Phone Number")
    email = st.text_input("Email")
    
    if st.button("Start Quiz"):
        if name and phone and email:
            if user_attempted_quiz(phone, email):
                st.error("You have already attempted this quiz.")
            else:
                st.session_state.name = name
                st.session_state.phone = phone
                st.session_state.email = email
                # Randomly select 10 questions
                st.session_state.selected_questions = random.sample(quiz_data, 10)
                st.session_state.score = 0
                st.session_state.start_time = time.time()  # Start the timer
                st.session_state.timer_started = True  # Flag to indicate timer has started
        else:
            st.error("Please enter your name, phone number, and email.")

# Quiz page
else:
    st.title("Quiz App")
    
    # Timer
    if 'timer_started' in st.session_state and st.session_state.timer_started:
        total_time = 7 * 60  # 7 minutes in seconds
        time_left = total_time - int(time.time() - st.session_state.start_time)

        if time_left > 0:
            minutes, seconds = divmod(time_left, 60)
            st.write(f"Time left: {minutes:02}:{seconds:02}")
        else:
            st.write("Time's up! Submitting the quiz automatically.")
            st.session_state.timer_started = False  # Stop the timer
            st.session_state.submit_quiz = True  # Flag to indicate quiz should be submitted

    # Create a form to hold all questions
    with st.form(key='quiz_form'):
        # Loop through each selected question
        for index, question in enumerate(st.session_state.selected_questions):
            st.subheader(question['question'])
            # Display options as radio buttons
            user_answer = st.radio("Choose an option:", question['options'], key=f"question_{index}")
            # Store user answers in session state
            st.session_state[f'answer_{index}'] = user_answer

        # Add a single submit button
        submit_button = st.form_submit_button("Submit")

        if submit_button or ('submit_quiz' in st.session_state and st.session_state.submit_quiz):
            # Check answers and calculate score
            for index, question in enumerate(st.session_state.selected_questions):
                if st.session_state[f'answer_{index}'] == question['answer']:
                    st.session_state.score += 1

            # Insert user data into the database
            insert_user_data(st.session_state.name, st.session_state.phone, st.session_state.email, st.session_state.score)

            # Display the thank you page directly in the app
            st.write(f"Thank you, {st.session_state.name}!")
            st.write(f"Your final score is: {st.session_state.score}/{len(st.session_state.selected_questions)}")
            st.success("Thank you for participating!")

            # Delay before redirecting to the instructions page
            st.write("You will be redirected to the instructions page in 10 seconds...")
            time.sleep(10)

            # Clear session state to reset the quiz
            for key in list(st.session_state.keys()):
                del st.session_state[key]  
            st.write("Redirecting to the instructions page...")
