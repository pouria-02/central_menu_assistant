import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
import os

# API Key
api_key = os.environ.get("GOOGLE_API_KEY")
MODEL_NAME = "gemini-2.0-flash-exp"
llm = ChatGoogleGenerativeAI(model=MODEL_NAME, api_key=api_key)

# منو
menu = {
    "فست فود": {
        "پیتزا مارگاریتا": "خمیر نازک، سس گوجه‌فرنگی، پنیر موتزارلا، ریحان تازه",
        "برگر کلاسیک": "گوشت گوساله، نان برگر، پنیر چدار، کاهو، گوجه، سس مخصوص",
    },
    "پیش غذا": {
        "سالاد سزار": "کاهو رومی، مرغ گریل‌شده، پنیر پارمزان، کروتون، سس سزار",
    }
}

# دستیار رستوران
def restaurant_assistant(question):
    system_prompt = (
        "تو یه دستیار رستوران هستی و با لحنی صمیمی با مشتری‌ها صحبت می‌کنی. "
        "فقط درباره‌ی غذاهای منوی زیر جواب بده. "
        "اگر سوال ربطی به منو یا مواد تشکیل‌دهنده نداشت، با خوشرویی بگو: "
        "«من فقط درباره‌ی منو می‌تونم کمکت کنم :)»\n\n"
        "اگر کاربر درباره‌ی مواد تشکیل‌دهنده هر غذا پرسید، "
        "با لحن دوستانه درباره اون ماده توضیح بده، خواصش رو بگو و اگر قابل درست کردن در خونه هست، "
        "روش تهیه‌ش رو هم به طور خلاصه توضیح بده.\n\n"
        f"منو:\n{menu}"
    )
    msg = [HumanMessage(content=f"{system_prompt}\n\nسؤال مشتری: {question}")]
    response = llm.invoke(msg)
    return response.content

# ===== UI =====
st.markdown("<h2>🏰 رستوران تاج محل</h2>", unsafe_allow_html=True)

# Tabs برای دسته‌ها
tabs = st.tabs(list(menu.keys()))
for i, category in enumerate(menu.keys()):
    with tabs[i]:
        st.subheader(f"📋 {category}")
        for dish, ingredients in menu[category].items():
            st.markdown(f"- **{dish}**: {ingredients}")

# سوال و جواب AI
st.markdown("---")
st.subheader("💬 سوال از دستیار رستوران")
question = st.text_input("سؤال خود را بنویسید:", key="taj_input")
if question:
    answer = restaurant_assistant(question)
    st.markdown(f"**پاسخ دستیار:** {answer}")