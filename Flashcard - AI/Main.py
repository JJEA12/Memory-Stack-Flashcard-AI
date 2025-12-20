import streamlit as st
from openai import OpenAI
import json

client = OpenAI()

# -------------- PAGE CONFIG --------------
# This makes the layout wider and cleaner
st.set_page_config(page_title="Memory Stack", layout="wide")

# -------------- HEADER --------------
with st.container():
    st.title("Memory Stack 🧠")
    st.subheader("Generate helpful flashcards from your notes or text!")
    st.markdown("---")  # clean separator


# -------------- MAIN LAYOUT --------------
# Left = input + button
# Right = flashcard display area
left, right = st.columns([1, 2], gap="large")

with left:
    text = st.text_area("Test yourself now")
    # Button stays here (right under the input)
    generate = st.button("Generate Flashcards", use_container_width=True)


with right:
    st.markdown("### Flashcards")
   ### flashcard_area = st.container()  # we'll fill this later



# -------------- TABS (FOR FUTURE FEATURES) --------------
tab1, tab2 = st.tabs(["Learn", "Quiz Mode"])




    # -------------- BUTTON ACTION --------------
if generate:

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[ ##there's a role for the system and user, along witht the text input
            #there are parameters that the bot must follow
            {
                "role": "system",
                "content": (
                   # "Create flashcards in a list of JSON objects. "
                    "Each object must have 'question'"# and 'answer' fields."
                )
            },
            {
                "role": "user",
                "content": f"Create flashcards from this text:\n\n{text}"
            }
        ]
    )
    st.write(response.choices[0].message.content)
    #raw_output = response.choices[0].message.content ## it will output response
    #which is just the message and that is just content which is: role of the system followed by 
    #user.
    