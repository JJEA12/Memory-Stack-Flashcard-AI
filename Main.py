import streamlit as st
from openai import OpenAI
import json

# ----------------------------------
# OPENAI CLIENT
# ----------------------------------
# This creates a reusable client object for making API calls
client = OpenAI()

# ----------------------------------
# PAGE CONFIG
# ----------------------------------
# Must be the FIRST Streamlit command
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
# MAIN LAYOUT
# ----------------------------------
# Left column: input
# Right column: flashcards
left, right = st.columns([1, 2], gap="large")

with left:
    # Text area where users paste notes
    text = st.text_area(
        "Paste your study notes",
        height=250
    )

    # Button triggers AI generation
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

    # Prevent empty submissions
    if not text.strip():
        st.error("Please paste some notes first.")
    else:
        # Call OpenAI to generate structured flashcards
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Create flashcards in a JSON array. "
                        "Each item must be an object with "
                        "'question' and 'answer' keys. "
                        "Return ONLY valid JSON."
                    )
                },
                {
                    "role": "user",
                    "content": f"Create flashcards from this text:\n\n{text}"
                }
            ]
        )

        # Extract model output
        raw_output = response.choices[0].message.content.strip()

        # Remove markdown code fences if the model adds them
        raw_output = raw_output.replace("```json", "").replace("```", "")

        # Attempt to parse JSON
        try:
            flashcards = json.loads(raw_output)
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
                            background:#f9f9f9;
                            border:1px solid #e0e0e0;
                        ">
                            <strong>Q:</strong> {card.get("question", "")}<br><br>
                            <strong>A:</strong> {card.get("answer", "")}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            else:
                st.error(
                    "Flashcards could not be generated. "
                    "Try rewriting your notes or using clearer text."
                )
