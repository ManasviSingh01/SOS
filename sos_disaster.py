# sos_disaster_bot.py

import streamlit as st
import requests
import spacy

# === CONFIGURATION ===
BOT_TOKEN = "7999556918:AAHbLSqEj_85iV2pZ5P309WxUU44w1AYt9Y"  # Replace with your real bot token
CHAT_ID = "1989062103"      # Replace with actual chat ID

# === SEND TO TELEGRAM FUNCTION ===
def send_to_telegram(full_message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": full_message}

    try:
        response = requests.post(url, data=data)
        if response.status_code == 200:
            return True
        else:
            st.error(f"Telegram error: {response.text}")
            return False
    except Exception as e:
        st.error(f"Exception while sending to Telegram: {e}")
        return False

# === LOAD NLP MODEL ===
try:
    nlp = spacy.load("en_core_web_sm")
except:
    st.error("SpaCy model not loaded. Run: python -m spacy download en_core_web_sm")

# === UI CONFIG ===
st.set_page_config(page_title="SOS Reporter", layout="centered")
st.title("🆘 Emergency SOS Reporter")

st.markdown("Fill out the emergency details. Your message will be analysed and sent to the rescue team.")

# === FORM ===
with st.form("sos_form"):
    name = st.text_input("👤 Your Name (optional)")
    location = st.text_input("📍 Location of Incident", placeholder="e.g., Gomti Nagar, Lucknow")
    priority = st.selectbox("🔥 Priority Level", ["Low", "Medium", "High", "Critical 🚨"])
    message = st.text_area("✉️ Describe the Emergency", height=150)
    submit = st.form_submit_button("🚀 Analyse & Send SOS")

# === ON SUBMIT ===
if submit:
    if message.strip() == "" or location.strip() == "":
        st.warning("Please fill in both Location and Message.")
    else:
        # === Combine Message for Telegram ===
        full_msg = f"""🚨 *SOS Emergency Alert* 🚨
👤 Name: {name if name else "Anonymous"}
📍 Location: {location}
🔥 Priority: {priority}
📝 Message: {message}"""

        # Send to Telegram
        sent = send_to_telegram(full_msg)
        if sent:
            st.success("✅ SOS sent to rescue team via Telegram.")
        else:
            st.error("❌ Failed to send to Telegram.")

        # NLP Analysis
        doc = nlp(message)
        st.subheader("📊 Emergency Message Analysis")
        if doc.ents:
            for ent in doc.ents:
                st.markdown(f"- **{ent.text}** → `{ent.label_}`")
        else:
            st.info("No named entities detected in message.")

        st.markdown("---")
        st.markdown("Stay strong 💪 Help is on the way 🚑🚒🚁")
