import streamlit as st
import google.generativeai as genai
import json

# ----------------------------------
# GEMINI CLIENT
# ----------------------------------
genai.configure(
    api_key=st.secrets["GOOGLE_API_KEY"]
)

model = genai.GenerativeModel("gemini-2.5-flash")

# ----------------------------------
# PAGE CONFIG
# ----------------------------------
st.set_page_config(
    page_title="Memory Stack",
    layout="wide"
)

st.title("Memory Stack 🧠")
st.subheader("Generate helpful flashcards from your notes or text!")
st.markdown("---")

left, right = st.columns([1, 2], gap="large")

with left:
    text = st.text_area("Paste your study notes", height=250)

    generate = st.button(
        "Generate Flashcards",
        use_container_width=True
    )

with right:
    st.markdown("### Flashcards")
    flashcard_area = st.container()

# ----------------------------------
# BUTTON LOGIC
# ----------------------------------
if generate:

    if not text.strip():
        st.error("Please paste some notes first.")
    else:
        response = model.generate_content(
            f"""
            Create flashcards in a JSON array.

            Each item must be an object with:
            - "question"
            - "answer"

            Return ONLY valid JSON.

            Create flashcards from this text:

            {text}
            """
        )

        raw_output = response.text.strip()

        try:
            flashcards = json.loads(raw_output)
        except json.JSONDecodeError:
            flashcards = []

        with flashcard_area:
            if flashcards:
                for card in flashcards:
                    st.markdown(
                        f"""
                        <div style="
                            padding:16px;
                            margin-bottom:12px;
                            border-radius:12px;
                            background:#171717;
                            border:1px solid #e0e0e0;
                        ">
                            <strong>Q:</strong> {card.get("question", "")}<br><br>
                            <strong>A:</strong> {card.get("answer", "")}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            else:
                st.error("Flashcards could not be generated.")
