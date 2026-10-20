import streamlit as st
import google.generativeai as genai

# 1. Az oldal alapbeállításai
st.set_page_config(page_title="Matematika Feladatmegoldó Mentor", page_icon="🧮", layout="centered")

st.title("🧮 Matematikai Feladatmegoldó Mentor")
st.caption("Pólya György gondolkodási lépései alapján")

# 2. Gemini API konfigurálása (Streamlit Secrets-ből vagy beviteli mezőből)
# Tipp: Ha st.secrets["GEMINI_API_KEY"]-t használsz, nem kell kézzel megadni
api_key = st.sidebar.text_input("Gemini API kulcs:", type="password")

if not api_key:
    st.warning("Kérlek, add meg a Gemini API kulcsot a bal oldali sávban a folytatáshoz!")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# 3. Kérdések és feladatok struktúrája (minta kérdéssor)
KERDESEK = [
    {
        "fejezet": "1. Lépés: A feladat megértése",
        "utmutato": "Olvasd el figyelmesen a szöveget! Mik a megadott adatok, és mi az ismeretlen?",
        "kerdes": "Írd le a saját szavaiddal, mit tudunk a feladatban, és mit kell kiszámolnunk!"
    },
    {
        "fejezet": "2. Lépés: Terv készítése",
        "utmutato": "Gondold át a kapcsolatot az adatok és az ismeretlen között!",
        "kerdes": "Milyen összefüggést vagy egyenletet tudsz felírni az adatok alapján?"
    },
    {
        "fejezet": "3. Lépés: A terv végrehajtása",
        "utmutato": "Végezd el a számításokat lépésről lépésre!",
        "kerdes": "Oldd meg a felírt egyenletet! Mutasd meg a számítás lépéseit!"
    },
    {
        "fejezet": "4. Lépés: Visszatekintés (Ellenőrzés)",
        "utmutato": "Vizsgáld meg a kapott eredményt!",
        "kerdes": "Ellenőrizd a kapott értéket az eredeti szövegbe való behelyettesítéssel! Reális a kapott válasz?"
    }
]

# 4. Session State (állapotkezelés) inicializálása
if "aktualis_index" not in st.session_state:
    st.session_state.aktualis_index = 0

if "valaszok" not in st.session_state:
    st.session_state.valaszok = {}

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 5. Alkalmazás logikája
index = st.session_state.aktualis_index

# Ha még van hátra kérdés
if index < len(KERDESEK):
    aktualis_adat = KERDESEK[index]

    # Haladási sáv (Progress bar)
    st.progress((index) / len(KERDESEK))
    st.subheader(f"{aktualis_adat['fejezet']}")
    st.info(aktualis_adat["utmutato"])

    st.markdown(f"**{index + 1}. Kérdés:** {aktualis_adat['kerdes']}")

    # Bevitel mező egyedi kulccsal az aktuális kérdéshez
    felhasznaloi_valasz = st.text_area(
        "A te válaszod:", 
        key=f"input_{index}", 
        height=120,
        placeholder="Írd ide a gondolataidat..."
    )

    col1, col2 = st.columns([1, 4])

    with col1:
        if st.button("Válasz beküldése", type="primary"):
            if felhasznaloi_valasz.strip() == "":
                st.error("Kérlek, írj valamit a válaszmezőbe!")
            else:
                # Válasz elmentése az állapotba
                st.session_state.valaszok[index] = felhasznaloi_valasz
                
                # Mentjük a beszélgetés előzményét AI értékeléshez
                st.session_state.chat_history.append({
                    "kérdés": aktualis_adat["kerdes"],
                    "válasz": felhasznaloi_valasz
                })
                
                # Léptetjük az indexet a következő kérdésre
                st.session_state.aktualis_index += 1
                
                # Újratöltjük a felületet
                st.rerun()

# 6. Összegzés és AI visszajelzés (amikor az összes kérdésre válaszolt a diák)
else:
    st.progress(1.0)
    st.success("🎉 Gratulálok! Végigértél az összes lépésen!")
    st.balloons()

    st.subheader("📋 A válaszaid összefoglalása:")
    for i, q in enumerate(KERDESEK):
        st.write(f"**{q['fejezet']}**")
        st.write(f"*Válasz:* {st.session_state.valaszok.get(i, '-')}")
        st.divider()

    # AI Mentor visszajelzés generálása
    with st.spinner("A mentortanárod áttekinti a megoldásodat..."):
        if "ai_visszajelzes" not in st.session_state:
            prompt = f"""
            Egy matematika tanár vagy. A diák az alábbi lépéseken ment keresztül egy feladat megoldása során (Pólya-féle módszer):
            
            {st.session_state.chat_history}
            
            Kérlek, adj rövid, dicsérő és építő jellegű visszajelzést a diák munkájára! 
            Ha volt benne hiányosság, tegyél fel rávezető kérdést, de ne add meg azonnal a végső választ, ha hibázott!
            """
            
            try:
                response = model.generate_content(prompt)
                st.session_state.ai_visszajelzes = response.text
            except Exception as e:
                st.session_state.ai_visszajelzes = f"Hiba történt az AI visszajelzés során: {e}"

    st.subheader("💬 A Mentor visszajelzése:")
    st.markdown(st.session_state.ai_visszajelzes)

    # Újraindítás gomb
    if st.button("Új feladat kezdése"):
        st.session_state.aktualis_index = 0
        st.session_state.valaszok = {}
        st.session_state.chat_history = []
        if "ai_visszajelzes" in st.session_state:
            del st.session_state.ai_visszajelzes
        st.rerun()
