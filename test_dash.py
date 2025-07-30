import streamlit as st
import time

st.title('Simple Test Dashboard')
st.write('If you can see this, Streamlit is working!')

# Add a simple counter to show interactivity
count = st.button('Click me!')
if count:
    st.write('Button clicked!')

# Display current time to show live updates
st.write(f'Current time: {time.strftime("%H:%M:%S")}')
