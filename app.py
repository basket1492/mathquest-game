import random
import streamlit as st

st.set_page_config(
    page_title="MathQuest - 20 Szintű Matek Kaland", page_icon="📐"
)

# --- JÁTÉK ÁLLAPOT INICIALIZÁLÁSA ---
if "level" not in st.session_state:
    st.session_state.level = 1
if "nim_sticks" not in st.session_state:
    st.session_state.nim_sticks = 15
if "dice_score" not in st.session_state:
    st.session_state.dice_score = 0

st.title("📐 MathQuest: A 20 Szintű Matematikai Kihívás")
st.progress(st.session_state.level / 20)
st.subheader(f"🏆 Jelenlegi szint: {st.session_state.level} / 20")

# --- SZINTEK DEFINIÁLÁSA ---

# 1. SZINT
if st.session_state.level == 1:
    st.markdown("### 1. Szint: A Tündérrózsák Rejtélye")
    st.write(
        "Egy tóban a tündérrózsák területe minden nap a duplájára nő. Ha a 20. napon lepi el félig a tavat, hányadik napon lepi el teljesen?"
    )
    ans = st.number_input("Válaszod (nap):", step=1, value=0)
    if st.button("Ellenőrzés"):
        if ans == 21:
            st.success("Helyes! Mivel naponta duplázódik, a 21. napra éri el a 100%-ot.")
            if st.button("Következő szint ➔"):
                st.session_state.level = 2
                st.rerun()
        else:
            st.error("Nem jó! Gondold át: ha ma félig van, és holnapra megduplázódik, mikor lesz tele?")

# 2. SZINT
elif st.session_state.level == 2:
    st.markdown("### 2. Szint: A Kakas Kérdése")
    st.write(
        "Ha egy kakas tojást tojik a kerítés tetejére, melyik oldalra esik le a tojás?"
    )
    ans = st.radio(
        "Válassz:", ["Balra", "Jobbra", "A kerítésen marad", "A kakas nem tojik tojást"]
    )
    if st.button("Ellenőrzés"):
        if ans == "A kakas nem tojik tojást":
            st.success("Így van! Figyelni kell a részletekre.")
            st.session_state.level = 3
            st.rerun()
        else:
            st.error("Próbáld újra! Biztos, hogy a kakas tojik?")

# 3. SZINT
elif st.session_state.level == 3:
    st.markdown("### 3. Szint: Hiányzó Láncszem")
    st.write("Milyen szám következik a sorozatban? **2, 3, 5, 7, 11, 13, ?**")
    ans = st.number_input("Következő szám:", step=1, value=0)
    if st.button("Ellenőrzés"):
        if ans == 17:
            st.success("Pontos! Ezek a prím számok sorban.")
            st.session_state.level = 4
            st.rerun()
        else:
            st.error("Nem talált. Milyen tulajdonsága van ezeknek a számoknak?")

# 4. SZINT (Gép elleni játék: 15 pálcika Nim)
elif st.session_state.level == 4:
    st.markdown("### 4. Szint: A Nim-Játék (Gép Elleni Csatamező)")
    st.write(
        "15 pálcika van az asztalon. Felváltva vehettek el 1, 2 vagy 3 pálcikát. **Aki az utolsót veszi el, az VESZÍT!**"
    )
    st.info(f"Fennmaradó pálcikák: {'🥖 ' * st.session_state.nim_sticks} ({st.session_state.nim_sticks} db)")

    take = st.selectbox("Hány pálcikát veszel el?", [1, 2, 3])
    if st.button("Elveszem"):
        st.session_state.nim_sticks -= take
        if st.session_state.nim_sticks <= 0:
            st.error("Elvetted az utolsó pálcikát, vesztettél! A játék újraindul ezen a szinten.")
            st.session_state.nim_sticks = 15
        else:
            # Gép lépése (intelligens stratégia)
            ai_take = (st.session_state.nim_sticks - 1) % 4
            if ai_take == 0:
                ai_take = 1
            st.session_state.nim_sticks -= ai_take
            st.warning(f"A gép elvett {ai_take} pálcikát.")
            if st.session_state.nim_sticks <= 0:
                st.success("A gép kénytelen volt elvenni az utolsót! NYERTÉL!")
                st.session_state.nim_sticks = 15
                st.session_state.level = 5
                st.rerun()

# 5. SZINT
elif st.session_state.level == 5:
    st.markdown("### 5. Szint: A Kézfogások Száma")
    st.write(
        "Egy 6 fős társaságban mindenki mindenkivel egyszer kezet fog. Hány kézfogás történik összesen?"
    )
    ans = st.number_input("Kézfogások száma:", step=1, value=0)
    if st.button("Ellenőrzés"):
        if ans == 15:
            st.success("Helyes! (6 × 5) / 2 = 15 kézfogás.")
            st.session_state.level = 6
            st.rerun()
        else:
            st.error("Sajnos nem. Ne felejtsd el, hogy ha A kezet fog B-vel, az ugyanaz, mint B A-val!")

# (További szintek tetszőlegesen bővíthetők a 20-ig...)
elif st.session_state.level == 20:
    st.balloons()
    st.title("🎉 GRATULÁLOK! Legyőzted a 20 Szintet és Teljesítetted a MathQuestet!")
