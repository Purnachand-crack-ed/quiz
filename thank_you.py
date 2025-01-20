import streamlit as st

def main():
    # Get the score from the session state
    score = st.session_state.get('score', 0)
    name = st.session_state.get('name', 'User')

    st.title("Thank You!")
    st.write(f"Thank you, {name}!")
    st.write(f"Your final score is: {score}")
    st.success("Thank you for participating!")

if __name__ == "__main__":
    main()
