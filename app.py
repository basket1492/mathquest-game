import streamlit as st
from google import genai

st.set_page_config(page_title="MathQuest", page_icon="🧮")
st.title("🧮 MathQuest - Pólya Mentor")

# API Kulcs lekérése (Secrets-ből vagy beviteli mezőből)
api_key = st.sidebar.text_input("Gemini API kulcs:", type="password")

if not api_key:
    st.info("Kérlek, add meg a Gemini API kulcsot a bal oldali sávban!")
    st.stop()

# Ügyfél inicializálása az új SDK-val
client = genai.Client(api_key=api_key)

# Session State inicializálás
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "model", "text": "Szia! Milyen matematikai feladaton dolgozol most? Írd le a szövegét!"}
    ]

# Korábbi üzenetek megjelenítése
for msg in st.session_state.messages:
    role = "user" if msg["role"] == "user" else "assistant"
    with st.chat_message(role):
        st.write(msg["text"])

# Beviteli mező (st.chat_input)
if prompt := st.chat_input("Írd ide a válaszod..."):
    # Felhasználó üzenetének mentése és kiírása
    st.session_state.messages.append({"role": "user", "text": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Rendszerutmutató a Pólya-módszerhez
    system_instruction = """
    Egy segítőkész matematikatanár vagy. A célod, hogy Pólya György 4 lépéses módszerével
    (1. Megértés, 2. Terv, 3. Végrehajtás, 4. Visszatekintés) rávezesd a diákot a feladat megoldására.
    SZIGORÚ SZABÁLY: Soha ne mondd ki a végső választ vagy az ismeretlen értékét! 
    Mindig csak egy lépést kérdezz vagy javíts!
    """

    # AI válasz generálása
    with st.chat_message("assistant"):
        with st.spinner("Gondolkodom..."):
            try:
                # Előzmények átadása
                chat_history = []
                for m in st.session_state.messages:
                    chat_history.append({"role": m["role"], "parts": [{"text": m["text"]}]})

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=chat_history,
                    config={"system_instruction": system_instruction}
                )
                
                ai_text = response.text
                st.write(ai_text)
                st.session_state.messages.append({"role": "model", "text": ai_text})
                
            except Exception as e:
                st.error(f"Hiba történt: {e}")
