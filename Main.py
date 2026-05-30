import streamlit as st
import google.generativeai as genai
import json
import re

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

# ----------------------------------
# HEADER
# ----------------------------------
st.title("Memory Stack 🧠")
st.subheader("Generate helpful flashcards from your notes or text!")
st.markdown("---")

# ----------------------------------
# LAYOUT
# ----------------------------------
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
# GENERATION LOGIC
# ----------------------------------
if generate:

    if not text.strip():
        st.error("Please paste some notes first.")
    else:
        response = model.generate_content(
            f"""
            Create flashcards in JSON format ONLY.

            Output must be a JSON array like:
            [
              {{"question": "...", "answer": "..."}}
            ]

            No explanations. No markdown. No backticks.

            Text:
            {text}
            """
        )

        raw_output = response.text.strip()

        # DEBUG (optional but useful)
        #st.write("RAW OUTPUT:", raw_output)

        # -----------------------------
        # CLEAN OUTPUT
        # -----------------------------
        cleaned = raw_output.replace("```json", "").replace("```", "").strip()

        # extract JSON array safely
        match = re.search(r"\[.*\]", cleaned, re.DOTALL)

        flashcards = []

        if match:
            try:
                flashcards = json.loads(match.group())
            except json.JSONDecodeError:
                flashcards = []

        # ----------------------------------
        # DISPLAY FLASHCARDS
        # ----------------------------------
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
                st.error("Flashcards could not be generated. Check RAW OUTPUT above.")
