import streamlit as st 
from linkedin_bot import linkedin_search

st.set_page_config(page_title="LinkedIn Connect Bot")

st.title("LinkedIn Connection Automator")
prompt = st.text_input("Enter a role or keyword to search on LinkedIn")

if st.button("Search and Connect"):
    st.write(f"Searching LinkedIn for: '{prompt}'...")
    linkedin_search(prompt)
    st.success("Search done! Now ready to shortlist top 20 profiles.")
