import streamlit as st
import pandas as pd
import qrcode
from io import BytesIO
from datetime import datetime
import os
import random
import base64

klo_weisheiten = [
    "„Wer lange sitzt, wird nicht schneller fertig.“",
    "„Ein stiller Ort ist nur so still wie sein Benutzer.“",
    "„Der frühe Vogel kann mich mal – ich sitze erst mal.“",
    "„Hier denkt man klarer – manchmal zu klar.“",
    "„Ein König erkennt man an seinem Thron.“",
    "„Wer spült, ist klar im Vorteil.“",
    "„Große Taten brauchen große Stille.“",
    "„Nicht alles was stinkt, ist schlecht.“"
]


def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio autoplay>
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        st.markdown(md, unsafe_allow_html=True)



st.set_page_config(page_title="Klo-Tagebuch Deluxe", page_icon="💩")

DATA_FILE = "klo_tagebuch.csv"

# -----------------------------
# Daten laden oder erstellen
# -----------------------------
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        df = pd.DataFrame(columns=["Name", "Zeitpunkt", "Art", "Kommentar"])
        df.to_csv(DATA_FILE, index=False)
        return df

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

df = load_data()

# -----------------------------
# Header
# -----------------------------
st.title("🚽 Klo‑Tagebuch Deluxe")

st.caption("Willkommen auf dem stillen Örtchen. Bitte hinterlassen Sie nur Erinnerungen, keine Spuren.")

st.write("Trag dich ein und werde Teil der **Toiletten‑Chroniken**.")
st.image("https://www.mein-haustier.de/wp-content/uploads/2021/07/shutterstock_15626023151.jpg")
st.info(random.choice(klo_weisheiten))



# -----------------------------
# QR-Code anzeigen
# -----------------------------
# st.subheader("📱 QR‑Code für das Klo")

# url = "https://klotagebuch-partyset.streamlit.app"  # <- hier deine URL eintragen

# qr = qrcode.make(url)
# buf = BytesIO()
# qr.save(buf, format="PNG")
# st.image(buf.getvalue(), caption="Scanne mich, Happy Birthday to you! 🎉")

# -----------------------------
# Formular für Eintrag
# -----------------------------
st.subheader("✍️ Dein majestätischer Eintrag")

st.write("Bitte beschreibe dein Werk. Sei ehrlich. Sei stolz.")
st.subheader("Wer sitzt gerade auf dem Thron?")

# Session-State initialisieren
if "name" not in st.session_state:
    st.session_state.name = None
if "new_user_mode" not in st.session_state:
    st.session_state.new_user_mode = False

col1, col2, col3 = st.columns(3)

# Buttons
with col1:
    if st.button("Pascal"):
        st.session_state.name = "Pascal"
        st.session_state.new_user_mode = False

with col2:
    if st.button("Marlene"):
        st.session_state.name = "Marlene"
        st.session_state.new_user_mode = False

with col3:
    if st.button("Gast"):
        st.session_state.new_user_mode = True
        st.session_state.name = ""   # leer, damit Textfeld erscheint

# Wenn neuer Nutzer gewählt wurde → Textfeld anzeigen
if st.session_state.new_user_mode:
    st.session_state.name = st.text_input("Bitte gib deinen Namen ein:", st.session_state.name)

# Anzeige
if not st.session_state.name:
    st.info("Bitte wähle einen Namen aus.")
else:
    st.success(f"Ausgewählt: {st.session_state.name}")

with st.form("eintrag_form"):
    
    name = st.session_state.name
    st.subheader("Wer sitzt gerade auf dem Thron?")


    art = st.selectbox(
        "Wie würdest du dein Werk bewerten?",
        [
            "💨 Nur ein Lüftchen",
            "💧 Nur eine kleine Bach",
            "💩 Solide Nummer",
            "🚀 Start einer Rakete",
            "🌋 Vulkanische Aktivität",
            "🥚 Glücks-Ei",
            "🧻 Ich brauche Unterstützung",
            "🤫 Geheimmission – der Geniesser!",
            "👑 Ein königliches Meisterwerk",
            "🧙‍♂️ Magische Überraschung",
            "💩 7 Kringel & eine Spitze – das volle Programm",
            "1️⃣ Lesmeister Special",
            "2️⃣ Ein Weberli",
            "3️⃣ Hecktor, ein Strolle aus dem Bilderbuch!"
        ]
    )
    kommentar = st.text_area("Letzte Worte zu deinem Werk (optional)")
    submitted = st.form_submit_button("Eintragen und Spülen")


if submitted:
    if name.strip() == "":
        st.error("Bitte gib deinen Namen ein. Anonyme Helden gibt es schon genug.")
    else:
        new_entry = {
            "Name": name,
            "Zeitpunkt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Art": art,
            "Kommentar": kommentar
        }
        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
        save_data(df)
        st.success("Dein Eintrag wurde erfolgreich im Porzellanarchiv verewigt!")
        # 🔊 Sound automatisch abspielen
        autoplay_audio("flush.mp3")


# -----------------------------
# Einträge anzeigen
# -----------------------------
st.subheader("📖 Die Chroniken des Porzellanthrons")

if len(df) == 0:
    st.info("Noch keine Einträge. Sei der Pionier dieses stillen Ortes.")
else:
    st.dataframe(df[::-1])