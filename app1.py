import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Matematika Mentor", page_icon="🧮")
st.title("🧮 Matematikai Feladatmegoldó Mentor")

# 1. API Kulcs beállítása
api_key = st.sidebar.text_input("Gemini API kulcs:", type="password")

if not api_key:
    st.info("Kérlek, add meg az API kulcsot a bal oldali sávban a kezdéshez!")
    st.stop()

genai.configure(api_key=api_key)

# 2. Rendszerinstrukció (Pólya-féle módszer, ne adja meg a végeredményt)
SYSTEM_PROMPT = """
Egy segítőkész matematikatanár vagy. A célod, hogy Pólya György 4 lépéses módszerével
(1. Megértés, 2. Terv, 3. Végrehajtás, 4. Visszatekintés) rávezesd a diákot a feladat megoldására.
SZIGORÚ SZABÁLY: Soha ne mondd ki a végső választ vagy az ismeretlen értékét! 
Mindig csak egy lépést kérdezz vagy javíts, és vezesd a diákot kérdésekkel!
"""

# 3. Modell és Session inicializálás
if "model" not in st.session_state:
    st.session_state.model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=SYSTEM_PROMPT
    )

if "chat" not in st.session_state:
    # Elindítjuk a hálózati chat munkamenetet
    st.session_state.chat = st.session_state.model.start_chat(history=[])

if "messages" not in st.session_state:
    st.session_state.messages = []
    # Kezdő üdvözlés a mentortól
    kezdo_uzenet = "Szia! Milyen matematikai feladaton dolgozol most? Írd le a szövegét!"
    st.session_state.messages.append({"role": "model", "parts": [kezdo_uzenet]})

# 4. Korábbi üzenetek kirajzolása a képernyőre
for message in st.session_state.messages:
    role = "user" if message["role"] == "user" else "assistant"
    with st.chat_message(role):
        st.write(message["parts"][0])

# 5. Beviteli mező (st.chat_input - ez automatikusan kezeli a beküldést és az állapotot!)
if prompt := st.chat_input("Írd ide a válaszod..."):
    
    # Felhasználó üzenetének megjelenítése és mentése
    with st.chat_message("user"):
        st.write(prompt)
    st.session_state.messages.append({"role": "user", "parts": [prompt]})

    # AI válaszának lekérése és megjelenítése
    with st.chat_message("assistant"):
        with st.spinner("Gondolkodom..."):
            try:
                response = st.session_state.chat.send_message(prompt)
                st.write(response.text)
                st.session_state.messages.append({"role": "model", "parts": [response.text]})
            except Exception as e:
                st.error(f"Hiba történt a válaszadás során: {e}")
